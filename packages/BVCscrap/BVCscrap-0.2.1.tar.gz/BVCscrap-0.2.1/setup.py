import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BVCscrap",
    version="0.2.1",
    author="ANDAM Amine",
    author_email="andamamine83@gmail.com",
    description='Python library to scrape financial data from Casablanca Stock Exchange(Bourse des Valeurs de Casablanca)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/AmineAndam04/BVCscrap',
    keywords=["Web scrapping","financial data","Bourse des Valeurs de Casablanca"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)