import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py2md",
    version="0.0.5",
    author="Xero64",
    author_email="xero64@gmail.com",
    description="Run python code in jupyter to generate markdown reports.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Xero64/py2md",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
