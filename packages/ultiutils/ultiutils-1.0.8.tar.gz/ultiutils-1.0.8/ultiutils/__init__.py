from ultiutils.ultimain import *
import requests
from packaging import version
class __version__:
  __newest__ = requests.get( "https://pypi.python.org/pypi/ultiutils/json").json()['info']['version']
  __current__ = open('ver.txt').read()
print(f'ultiutils ver {__version__.__current__}')
if version.parse(__version__.__newest__) > version.parse(__version__.__current__):
  print('ultiutils may be outdated')
  print(f'newest version is: {__version__.__newest__}, you are running {__version__.__current__}')