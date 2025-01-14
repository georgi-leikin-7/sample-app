from setuptools import find_packages, setup

setup(
    name="facade-lib",
    version="1.0",
    description="A common Facade Lib package",
    author="Georgi Leikin",
    author_email="georgi.leikin.7@gmail.com",
    packages=find_packages(),
    install_requires=[
        "boto3==1.35.72; python_version >= '3.8'",
        "loguru==0.7.2; python_version >= '3.5'",
        "pydantic==2.10.5; python_version >= '3.8'",
        "pydantic-core==2.27.2; python_version >= '3.8'",
        "pydantic-settings==2.7.1; python_version >= '3.8'",
    ],
    python_requires=">=3.11",
)
