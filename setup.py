import os
from setuptools import setup
import pdfhacker.py

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = "Pdfhacker",
    version = "1.0",
    author = "Nivethithan",
    author_email = "nivethithan@gmail.com",
    description = "Get business insights from your documents instantly",
    license = "BSD",
    url = "https://github.com/PrinceIcyflame/pdfhacker",
    install_requires=required,
)

if __name__ == "__main__":
    execfile('pdfhacker.py')
