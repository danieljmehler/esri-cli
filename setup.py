from setuptools import setup, find_packages

setup(
    name="esri-services-api",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["requests>=2.25.0"],
    extras_require={"test": ["pytest>=6.0.0"]},
    entry_points={
        "console_scripts": [
            "esri-cli=cli:main",
        ],
    },
)