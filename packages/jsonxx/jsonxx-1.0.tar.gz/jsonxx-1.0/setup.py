import pathlib
from setuptools import setup
from re import findall

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding="utf-8")

VERSION = findall(r"__version__ = '(.*)'",
                  (HERE / "jsonxx/__init__.py").read_text())[0]

# This call to setup() does all the work
setup(
    name="jsonxx",
    version=VERSION,
    description="Python json extended.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="SPRAVEDLIVO",
    author_email="admin@spravedlivo.dev",
    license="AGPLv3",
    packages=["jsonxx"],
    python_requires='>=3.10',
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    include_package_data=True
)
