import cssutils
from PIL import Image

from io import BytesIO
import urllib.request, urllib.parse, urllib.error
import re
import sys
import os.path
import argparse


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--input", action="append", dest="input_css_list",
                    help="URL of the input css. Can be passed multiple times.")
  parser.add_argument("-o", "--css-output", action="store", dest="css_output",
                    help="Path of the css output css")
  parser.add_argument("-O", "--image-output", action="store",
                    dest="image_output", help="Path of the image output")
  options = parser.parse_args()

  css_dict = dict()
  img_dict = dict()
  sheet_list = []

  # parse all css and gather all images
  for input_css in options.input_css_list:
    base = os.path.dirname(input_css)
    css_content = urllib.request.urlopen(input_css).read()

    def read_image(url):
      if urllib.parse.splittype(url)[0] is None:
        url = '%s/%s' % (base, url)
      # XXX handle 404
      print("  downloading", url)
      return Image.open(BytesIO(urllib.request.urlopen(url).read()))

    print("processing", input_css)
    sheet = cssutils.parseString(css_content)

    extract_img_re = re.compile(r'url\([\'\"]*([^\'\"]*)[\'\"]*\)')

    for rule in sheet:
      if rule.type == rule.STYLE_RULE:
        for prop in rule.style:
          if prop.name == 'background-image':
            if 'url' in prop.value:
              img_url = extract_img_re.match(prop.value).groups()[0]
              if img_url == 'blank.gif':
                continue
              img_dict[img_url] = read_image(img_url)
              css_dict[rule.selectorText] = 1

    sheet_list.append(sheet)

  # build the image
  total_width = max((img.size[0] for img in img_dict.values()))
  total_height = sum((img.size[1] for img in img_dict.values()))

  big_image = Image.new(
          mode='RGBA',
          size=(total_width, total_height),)

  img_offset_dict = dict()
  offset = 0
  for url, img in img_dict.items():
    width, height = img.size
    big_image.paste(img, (0, offset))
    img_offset_dict[url] = dict(offset=-offset,
                                height=height,
                                width=width,
                                img_url=url)
    offset += height

  # replace the image references and write a full css
  new_css_text_list = []
  for sheet in sheet_list:
    # TODO: calculate the "images" part based on urls differences
    full_img_url = "url(images/%s)" % (os.path.basename(options.image_output))

    for rule in sheet:
      if rule.type == rule.STYLE_RULE:
        for prop in rule.style:
          if prop.name == 'background-image':
            if 'url' in prop.value:
              position = rule.style.getProperty('background-position', normalize=True)
              if position:# and position.value not in ('left', 'top left'):
                print("WARNING ignoring complex background-position %s for %s" % (
                  position.cssText, rule.cssText))
                continue
              img_url = extract_img_re.match(prop.value).groups()[0]
              if img_url == 'blank.gif':
                continue
              rule.style['background-image'] = full_img_url
              img_pos = img_offset_dict[img_url]
              rule.style['background-position'] = "0px %(offset)spx" % img_pos
              rule.style['width'] = "%(width)spx" % img_pos
              rule.style['height'] = "%(height)spx" % img_pos
    new_css_text_list.append(sheet.cssText)

  with open(options.css_output, "wb") as f:
    for css_text in new_css_text_list:
      f.write(css_text)

  big_image.save(options.image_output)
