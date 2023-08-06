from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="samplr",
    version="1.0.0",
    author="ROSHAKA",
    author_email="dan@roshaka.io",
    description="A simple decorator for returning a small sample of items from a list.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/roshaka/samplr",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)