
from setuptools import find_packages, setup

setup(
    name="Awa2",
    version="1.1.1",
    author="XiangQinxi",
    description="Simple Setup",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3",
    packages=find_packages(where='.'),
    install_requires=["rich", "pick", "toml", "build", "setuptools", "twine"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
        