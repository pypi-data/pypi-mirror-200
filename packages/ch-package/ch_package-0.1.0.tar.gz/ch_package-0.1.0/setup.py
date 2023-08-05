from setuptools import setup
import setuptools

def readme():
    with open("README.md", "r") as fh:
        return fh.read()

setup(
    name='ch_package',
    version='0.1.0',
    description='This will provide similar function "NLTK" "WordNetLemmatizer" module to "Sinhala" words',
    author= 'Chanaka Gunarathna',
    # url = 'https://github.com/ChanakaErangaGunarathna/Sinhala_Word_Simpliy',
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_dir={'':'src'},
    keywords=['sinhala', 'clean word'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)