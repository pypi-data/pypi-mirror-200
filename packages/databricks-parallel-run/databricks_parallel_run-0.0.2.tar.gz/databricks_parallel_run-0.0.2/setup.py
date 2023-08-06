from setuptools import setup
import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setup(
    name='databricks_parallel_run',
    version='0.0.2',
    description='Run databricks notebooks in parallel',
    author= 'Kuldeep Rathore',
    #url = 'https://github.com/Spidy20/PyMusic_Player',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['python', 'databricks', 'notebook', 'databricks parallel run', 'databricks parallel notebook run', 'paralle processing'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['databricks_parallel_run'],
    package_dir={'':'src'}
)