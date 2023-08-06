import sys
from pathlib import Path
from typing import Dict

import setuptools

HERE = Path(__file__).resolve().parent

try:
    import pointy

except ImportError:
    sys.path.insert(0, str(HERE))


def long_description() -> str:
    path = HERE / "README.md"

    with path.open("r", encoding="utf-8") as fp:
        return fp.read()


def read_about() -> Dict[str, str]:
    import pointy.__about__ as about

    return {
        "version": about.__version__,
        "name": about.__name__,
        "description": about.__description__,
        "author": about.__author__,
        "author_email": about.__author_email__,
        "url": about.__url__
    }


setuptools.setup(
    long_description=long_description(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": str(HERE)},
    packages=["pointy"],
    python_requires=">=3.8",
    **read_about()
)
