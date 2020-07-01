css-spriter
===========

Rewrite a CSS to use CSS-Sprites.
Takes the URL of one or multiple CSS as input, download all images, rewrite CSS
and produce a CSS and a merged image as output.

This only supports images as ``background-image:``.

Example usage::
  
  ./bin/cssspriter -i http://localhost/devel.css -o full.css -O full.png
