from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.10'
DESCRIPTION = "Windows-10-Toast-Notifications without pywin32 dependency"

# Setting up
setup(
    name="win10ctypestoast",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/win10ctypestoast',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['Pillow', 'pystray'],
    keywords=['ctypes', 'windows', 'toast'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['Pillow', 'pystray'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*