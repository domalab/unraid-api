from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="unraid_api",
    version="0.1.0",
    author="Ruaan Deysel",
    author_email="ruaan.deysel@gmail.com",
    description="A Python API for Unraid server management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/domalab/unraid-api",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "asyncssh>=2.13.1",
        "pydantic>=1.10.7",
        "aiohttp>=3.8.4",
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.1",
            "pytest-asyncio>=0.21.0",
            "black>=23.3.0",
            "isort>=5.12.0",
            "mypy>=1.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "unraid_api=unraid_api.cli:main",
        ],
    },
)