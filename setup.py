
from setuptools import setup, find_packages

with open('./README.rst') as f:
  long_description = f.read()

setup(name='cssspriter',
      description='CSS Sprites generator',
      keywords='css sprite',
      version='0.2.2',
      url='https://github.com/perrinjerome/cssspriter',
      license='GPL',
      author='Jérome Perrin',
      packages=find_packages(),
      install_requires=['Pillow', 'cssutils'],
      entry_points=dict(console_scripts=
              'cssspriter=cssspriter:main'),
      long_description=long_description,
      long_description_content_type='text/x-rst',
)
