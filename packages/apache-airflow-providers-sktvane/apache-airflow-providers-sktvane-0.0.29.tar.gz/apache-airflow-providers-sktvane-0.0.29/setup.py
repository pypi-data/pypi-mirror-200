import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apache-airflow-providers-sktvane",
    version="0.0.29",
    author="aidp",
    author_email="aidp@sktai.io",
    description="apache-airflow-providers-sktvane",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["airflow", "sktvane"],
    url="https://github.com/sktaiflow/sktvane-airflow-providers",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires="apache-airflow",
    python_requires=">=3.9",
)
