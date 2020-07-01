from setuptools import setup

setup(name='cssspriter',
      description='CSS Sprites generator',
      keywords='css sprite',
      version='0.2.0',
      url='',
      license='GPL',
      author='Jérome Perrin',
      install_requires=['Pillow', 'cssutils'],
      entry_points=dict(console_scripts=
              'cssspriter=cssspriter:main'),
)
