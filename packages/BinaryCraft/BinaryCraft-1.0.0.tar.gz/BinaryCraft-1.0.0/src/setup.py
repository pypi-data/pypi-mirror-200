from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="BinaryCraft",
    version="1.0.0",
    author="ayyandurai",
    author_email="ayyanduraiayyandurai345@gmail.com",
    description="A Python script to convert files to binary format and back",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["binary_converter"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
