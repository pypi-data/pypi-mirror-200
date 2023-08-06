"""
Manual:
    1. Increment version;
    2. Run: python3 setup.py sdist bdist_wheel
    3. Run: twine upload dist/*
"""

import setuptools
from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

with open("README.md", "r") as fh:
    long_description = fh.read()

pfile = Project(chdir=False).parsed_pipfile
print(pfile)
install_requires = convert_deps_to_pip(pfile['packages'], r=False)

setuptools.setup(
    name="bonbon",
    version="1.1.4",
    author="Binyan",
    author_email="lbyxiafei@gmail.com",
    description="A utility library to help with data processing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lbyxiafei/bonbon",
    install_requires=install_requires,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
