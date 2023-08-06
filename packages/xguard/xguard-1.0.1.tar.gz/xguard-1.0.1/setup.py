from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="xguard",
    version="1.0.1",
    author="John Gitahi",
    author_email="gitahi109@gmail.com",
    description="xguard, yet another guard clauses libary",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/johngitahi/xguard",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='guard clause',
    python_requires=">=3.6",
)

