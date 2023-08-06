from setuptools import setup, find_packages
import pathlib
import mmap_ninja_dataframe

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="mmap_ninja_dataframe",
    version=mmap_ninja_dataframe.__version__,
    description="mmap_ninja_dataframe: Memory mapped data structures",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/microlib-org/mmap_ninja_dataframe",
    author="Hristo Vrigazov",
    author_email="hvrigazov@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["mmap_ninja", "numpy"],
)
