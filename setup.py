import os
from setuptools import find_packages, setup

FILE_PATH = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(FILE_PATH, "README.md"), "r") as f:
    description = f.read()

with open(os.path.join(FILE_PATH, "requirements.txt")) as f:
    required = f.read().splitlines()

with open(os.path.join(FILE_PATH, "straw_machine", "__init__.py")) as f:
    __version__= None
    for l in f.read().splitlines():
        if l.startswith("__version__"):
            exec(l)
        break
    if __version__ is None:
        raise RuntimeError("no version specific")

setup(
    name="straw_machine",
    version=__version__,
    author="blizhan",
    author_email="blizhan@icloud.com",
    description="A python making machine of sklearn pipeline",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/blizhan/straw-machine",
    package_dir={"straw_machine": "straw_machine", ".": "./"},
    package_data={
        "": ["*.toml", "*.txt"],
    },
    include_package_data=True,
    packages=find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
)