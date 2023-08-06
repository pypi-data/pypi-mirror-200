from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="PyBlueprintMaker",
    version="0.1.2",
    author="Patricia Mejia",
    author_email="contact@patimejia.com",
    description="Python-based tool that helps you create organized project directories or structures. It uses best practices and incorporates fixtures, pytest, and the Python Standard Library to ensure the quality of the project's organization and structure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/patimejia/PyBlueprintMaker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    keywords="project-scaffolding project-structure python-project-template python-project-generator best-practices pytest fixtures python-standard-library code-quality project-management",

    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        "console_scripts": [
            "PyBlueprintMaker=src.main:main",
        ],
    },
)
