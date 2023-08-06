import setuptools
from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

VERSION = '0.0.2'
DESCRIPTION = 'Data Analysis and  Visualization Functions'
LONG_DESCRIPTION = 'The modules include functions that might be useful in general cases for data analysis ' \
                   'and data visualization. '

# Setting up
setup(
    name="pydataanalysis",
    version=VERSION,
    license="MIT",
    author="Tamer Samara",
    author_email="tamer.samara@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=["Pandas", "Statsmodels", "Seaborn", "Matplotlib", "SciPy", "NumPy", "Scikit-learn"],
    keywords=['python', 'data science', 'eda', 'data preprocessing', 'data analysis', 'machine learning'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)