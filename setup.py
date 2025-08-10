from setuptools import setup, find_packages

setup(
    name="z8ter",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "starlette",
        "jinja2",
    ],
    entry_points={
        "console_scripts": [
            "z8=z8ter.cli:run",
        ],
    },
)
