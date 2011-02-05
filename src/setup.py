__author__="emre"
__date__ ="$05.Feb.2011 14:16:14$"

from setuptools import setup,find_packages

setup (
  name = 'teleskop',
  version = '0.1',
  packages = ('teleskop',),

  # Declare your packages' dependencies here, for eg:
  install_requires=['PIL>=1'],

  # Fill in these to make your Egg ready for upload to
  # PyPI
  author = 'emre',
  author_email = '',

  summary = 'Queued image resizer',
  url = 'https://github.com/aladagemre/teleskop',
  license = 'GPL v3',
  long_description= 'Queued image resizer',

  # could also include long_description, download_url, classifiers, etc.

  
)