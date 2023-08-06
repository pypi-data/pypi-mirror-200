import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi (if you dont need delete it)
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# you need to change all these
VERSION = '1.0.0'
DESCRIPTION = 'Generating nomograms of logistic regression models'
LONG_DESCRIPTION = 'PyNG is a python pacakge for generating nomograms of logistic regression models with model coefficients and variables ranges'

setup(
    name="simpleNomo",
    version=VERSION,
    author="Haoyang Hong",
    author_email="haoyanghong@link.cuhk.edu.cn",
    description=DESCRIPTION,
    url='https://github.com/Hhy096/nomogram',
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    license='MIT',
    
    keywords=['python', 'nomogram', 'logistic regression'])