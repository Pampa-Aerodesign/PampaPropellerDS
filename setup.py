import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ppbd", # Replace with your own username
    version="0.0.1",
    author="Pampa Aerodesign",
    author_email="aerodesign@ufrgs.br",
    description="A propeller database for Pampa.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Pampa-Aerodesign/PampaPropellerDB",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = ["beautifulsoup4", "tinydb", "pandas"],
    packages=setuptools.find_packages(where="database_handler"),
    python_requires=">=3.6",
)