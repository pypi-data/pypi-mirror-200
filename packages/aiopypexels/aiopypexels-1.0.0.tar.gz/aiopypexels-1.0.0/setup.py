import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiopypexels",  # This is the name of the package
    version="1.0.0",  # The initial release version
    author="ggindinson",  # Full name of the author
    description="An asynchronous wrapper for Pexels API based on aiohttp, which additionally allows to download photos in any of avaliable resolutions.",
    # Long description read from the the readme file
    long_description=long_description,
    long_description_content_type="text/markdown",
    # List of all python modules to be installed
    packages=setuptools.find_packages(),
    keywords=["pexels", "api", "photos"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # Information to filter the project on PyPi website
    python_requires=">=3.6",  # Minimum version requirement of the package
    # Directory of the source code of the package
    install_requires=[
        "aiohttp",
        "dacite",
        "aiocfscrape",
    ],  # Install other dependencies if any
)
