import pathlib
from setuptools import setup
import os
# clear files
os.system('rm dist/* && rmdir build/*')
# bump version
ver = open('ver.txt', 'r').read()
ver = ver.split('.')
ver.reverse()
print(int(ver[0]) >= 10)
print(int(ver[1]) >= 10)
ver[0] = str(int(ver[0]) + 1)
if int(ver[0]) >= 10:
  ver[0] = str(0)
  ver[1] = str(int(ver[1]) + 1)
if int(ver[1]) >= 10:
  ver[1] = str(0)
  ver[2] = str(int(ver[2]) + 1)
ver.reverse()
open('ultiutils/ver.txt', 'w').write(f'{".".join(ver)}')
# Get the  current path
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()
# This call to setup() does all the work
setup(
    name="ultiutils",
    version=f'{".".join(ver)}',
    description="utilites module to make coding in python just wayyy faster",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/maverick-dev-55/Ultiutils",
    author="toxikdevswastaken",
    author_email="pypi@toxik.cf",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["ultiutils"],
    include_package_data=True,
    install_requires=["requests"],
)
os.system('twine check dist/* > check.txt')
check = open('check.txt', 'r').read()
if check.count('PASSED') == 2:
  os.system('twine upload --disable-progress-bar  --skip-existing --non-interactive dist/*')
else:
  print('ERROR: tests not passed')
  exit()

open('ver.txt', 'w').write(f'{".".join(ver)}')