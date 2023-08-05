from setuptools import setup
import setuptools

def readme():
    with open("README.md", "r") as fh:
        return fh.read()

setup(
    name='CleanSinhala',
    version='0.1.5',
    description='This will provide similar function "NLTK" "WordNetLemmatizer" module to "Sinhala" words',
    author= 'Chanaka Gunarathna',
    # url = 'https://github.com/ChanakaErangaGunarathna/Sinhala_Word_Simpliy',
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['sinhala', 'clean word'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)