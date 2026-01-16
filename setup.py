"""Setup configuration for UrbanComply utility data validation."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="urbancomply-validation",
    version="1.0.0",
    author="UrbanComply",
    description="Utility data validation script for LL84/33 benchmarking compliance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NickAiNYC/UrbanComply",
    py_modules=["check_utility_data"],
    python_requires=">=3.10",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "check-utility-data=check_utility_data:main",
        ],
    },
)
