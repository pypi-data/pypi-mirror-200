from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="humanfriendlyduration",
    version="1.0.0",
    author="Umar Lawal",
    author_email="pyomerhrr@gmail.com",
    description="A simple Python package for converting seconds to human-friendly duration strings.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/omerhrr/humanfriendlyduration",
    packages=["humanfriendlyduration"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

