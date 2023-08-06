from setuptools import setup
import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setup(
    name='testKuldeep',
    version='0.0.7',
    description='testing databricks',
    author= 'Kuldeep Rathore',
    #url = 'https://github.com/Spidy20/PyMusic_Player',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['python', 'databricks'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['testKuldeep'],
    package_dir={'':'src'},
	install_requires = [
        'pyspark',
        'DButils',
    ]
)