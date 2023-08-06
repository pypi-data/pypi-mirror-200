
from distutils.core import setup

with open('./README.md', 'r') as fh:
  long_description = fh.read()

setup(
  name = 'text-equivalences',         # How you named your package folder (MyLib)
  packages = ['text_equivalences'],   # Chose the same as "name"
  version = '0.1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Rule based language modeling',   # Give a short description about your library
  long_description = long_description,
  long_description_content_type= 'text/markdown',
  license_files = ('LICENSE.txt',),
  author = 'Alexandre Felipe',                   # Type in your name
  author_email = 'o.alexandre.felipe@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/o-alexandre-felipe/text-equivalences',   # Provide either the link to your github or to your website
  keywords = ['FST', 'Transducers', 'Regular Expression', 'Text normalization', 'graph', 'language model'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
