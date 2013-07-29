from setuptools import setup

setup(name='cssspriter',
      description='CSS Sprites generator',
      keywords='css sprite',
      version='0.1',
      url='',
      license='GPL',
      author='Jérome Perrin',
      install_requires=['PIL', 'cssutils'],
      entry_points=dict(console_scripts=
              'cssspriter=cssspriter:main'),
)
