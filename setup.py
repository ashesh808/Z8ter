from pathlib import Path
from setuptools import setup, find_packages

README = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="z8ter",
    version="0.1.0",
    description="SSR-first Python web framework with file-based views, tiny"
    "CSR islands, and decorator-driven APIs (Starlette + Jinja2).",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ashesh808/Z8ter",
    author="Ashesh Nepal",
    license="MIT",
    packages=find_packages(exclude=(
        "tests", "tests.*", "examples", "examples.*"
        )),
    include_package_data=True,
    python_requires=">=3.11",
    install_requires=[
        "starlette>=0.47,<1.0",
        "Jinja2>=3.1,<4.0",
    ],
    entry_points={"console_scripts": ["z8=z8ter.cli:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: AsyncIO",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
