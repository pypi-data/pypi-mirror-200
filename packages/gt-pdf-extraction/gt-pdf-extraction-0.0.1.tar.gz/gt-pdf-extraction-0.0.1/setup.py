from setuptools import setup, find_packages

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name="gt-pdf-extraction",
    version="0.0.1",
    author="Guangyu He",
    author_email="guangyu.he@golden-tech.de",
    description="A python pdf extraction package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/guangyuhe/pdf-extraction/src/main/",
    install_requires=[
        "pdfplumber",
        "tabula-py",
        "gy-multiprocessing",
        "pandas",
    ],
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    tests_require=["pytest"]
)
