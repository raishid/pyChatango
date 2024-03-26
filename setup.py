from setuptools import setup, find_packages

setup(
    name="pyChatango",
    version="0.1",
    packages=find_packages(),
    description="Send messages to Chatango chatrooms",
    author="Raishid",
    author_email="raishidavid@gmail.com",
    url="https://github.com/raishid/pyChatango",
    install_requires=[
        "playwright",
    ],
)
