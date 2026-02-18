from setuptools import setup, find_packages

setup(
    name="Topsis-Prabhsimrat-102317135",   
    version="1.0.0",
    author="Prabhsimrat Singh",
    author_email="prabhsimrat28112005@gmail.com",  
    description="A Python implementation of TOPSIS method using command line arguments",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas"
    ],
    entry_points={
        "console_scripts": [
            "topsis=topsis_package.topsis:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
