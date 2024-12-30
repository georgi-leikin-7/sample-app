from setuptools import find_packages, setup

setup(
    name="facade-lib",
    version="1.0",
    description="A common Facade Lib package",
    author="Georgi Leikin",
    author_email="georgi.leikin.7@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pydantic==2.9.2; python_version >= '3.8'",
        "pydantic-settings==2.6.1; python_version >= '3.8'",
    ],
    python_requires=">=3.11",
)
