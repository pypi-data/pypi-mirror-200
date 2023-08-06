import setuptools

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="testforPPshare",
    version='0.2.5',
    author="zemengchuan",
    author_email="zemengchuan@gmail.com",
    license="MIT",
    description=
    "PPtest is a utility for crawling historical and Real-time Quotes data of marco data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zemengchuan/PPtest",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests", "pandas", "openpyxl", "python-Levenshtein", "fuzzywuzzy"
    ],
    keywords=["macro", "webcrawler", "data"],
    package_data={"": ["*.py", "*.xlsx"]},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)