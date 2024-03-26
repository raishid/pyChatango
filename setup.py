from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="pychatango-dev",
    version="0.1.1",
    packages=find_packages(),
    description="Send messages to Chatango chatrooms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Raishid",
    author_email="raishidavid@gmail.com",
    url="https://github.com/raishid/pyChatango",
    install_requires=[
        "playwright",
    ],
)
