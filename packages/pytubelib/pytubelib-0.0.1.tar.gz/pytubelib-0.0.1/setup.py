import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytubelib",
    version="0.0.1",
    author="xXBlackDev9010Xx",
    author_email="tecnoblue9010@gmail.com",
    description="PyTubeLib is a tool for interacting with the YouTube Data v3 API using Python. With PyTubeLib, you can search for channels and videos using keywords, get details about specific channels and videos, and search for the latest videos from a channel. The class is designed to handle common API errors and returns results in JSON format for easy processing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xXBlackDev9010Xx/PyTubeLib",
    packages=setuptools.find_packages(),
    install_requires=[
        'google-api-python-client',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'colors-terminal'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)