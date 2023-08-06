import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apache-airflow-providers-sktvane",
    version="0.0.23",
    author="aidp",
    author_email="aidp@sktai.io",
    description="apache-airflow-providers-sktvane",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sktaiflow/sktvane-airflow-providers",
    packages=setuptools.find_packages(),
    classifier=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
