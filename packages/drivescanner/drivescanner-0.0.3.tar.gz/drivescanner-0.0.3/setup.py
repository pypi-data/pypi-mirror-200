from setuptools import setup, find_packages
from pathlib import Path

# read the contents of the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="drivescanner",
    version="0.0.3",
    python_requires=">=3.9",
    description="Scan your filesystem to look for files that are a potential GDPR risk",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Wouter van Gils, Wim Verboom, Sem Frankenberg, Steven Goos, Rick Flamand, Jeanine Schoonemann",
    author_email="service@cmotions.nl",
    url="https://dev.azure.com/Cmotions/Packages/_git/DriveScanner",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "textract-plus",
        "spacy",
        "phonenumbers",
        "langdetect",
        "bs4",
        "pypdf2"
    ],
    extras_require={
        "dev": [
            "black",
            "jupyterlab",
            "pytest>=6.2.4",
            "python-dotenv",
            "ipykernel",
            "twine"
        ],
    },
    # files to be shipped with the installation
    # after installation, these can be found with the functions in resources.py
    package_data={
        "drivescanner": [
            "data/*.csv",
            "data/*.txt",
            "notebooks/*tutorial*.ipynb",
        ]
    },
)
