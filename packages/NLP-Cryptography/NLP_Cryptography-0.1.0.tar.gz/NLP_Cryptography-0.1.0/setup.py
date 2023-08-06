from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="NLP_Cryptography",
    version="0.1.0",
    description="NLP Cryptography",
    author="Ammar",
    author_email="sleeping4cat@gmail.com",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        # list of classifiers (metadata) for your package
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
