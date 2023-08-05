from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.2'
DESCRIPTION = 'View Elmo Visualizer Camera Utilities'
LONG_DESCRIPTION = 'A package that allows to build view, record, capture, drawing and sticky notes to visualizer camera feed.'

# Setting up
setup(
    name="elmovisualizer-APP",
    version=VERSION,
    author="VeeKay Consultancy Services",
    author_email="<veekayit@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python', 'opencv-python-headless', 'numpy', 'PyQt5'],
    keywords=['visualizer', 'elmo'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",        
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
