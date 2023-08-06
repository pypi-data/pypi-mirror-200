from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nsaphx", 
    version="0.0.1",
    author="Naeem Khoshnevis",
    author_email="nkhoshnevis@g.harvard.edu",
    maintainer="Naeem Khoshnevis",
    maintainer_email = "nkhoshnevis@g.harvard.edu",
    description="nsaphx is a Python package for causal inference studies using the potential outcome framework. It offers a flexible and extensible framework to apply computational instructions to input data, including exposure, outcome, and confounders. The package uses directed acyclic graphs and database storage for efficient computation and storage.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NSAPH-Software/nsaphx",
    license="MIT",
    packages=find_packages(exclude=['docs*', 'tests*', 'scripts*',
                                    'notebooks*']),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    python_requires='>=3.7',
)
