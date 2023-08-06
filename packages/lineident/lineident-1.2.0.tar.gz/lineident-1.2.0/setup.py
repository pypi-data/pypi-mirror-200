from setuptools import setup, find_packages

with open("README.md", "r") as r:
    desc = r.read()

setup(
    name="lineident",
    version="1.2.0",
    author="5f0",
    url="https://github.com/5f0ne/lineident",
    description="Searches files line by line for given words",
    classifiers=[
        "Operating System :: OS Independent ",
        "Programming Language :: Python :: 3 ",
        "License :: OSI Approved :: MIT License "
    ],
    license="MIT",
    long_description=desc,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    include_package_data=True,
    install_requires=[
        "hash_calc"
    ],
     entry_points={
        "console_scripts": [
            "lineident = lineident.__main__:main"
        ]
    }
)
