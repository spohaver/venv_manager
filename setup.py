from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="venv-manager",
    version="1.0.0",
    author="spohaver",
    author_email="your-email@example.com",
    description="A comprehensive Python virtual environment manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spohaver/venv-manager",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "venv-manager=venv_manager:main",
        ],
    },
    include_package_data=True,
)
