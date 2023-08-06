#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author="IOMETE",
    author_email="support@iomete.com",
    python_requires=">=3.7",
    description="An Airflow plugin for interacting with IOMETE platform.",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    name="iomete_airflow_plugin",
    url="https://github.com/iomete/iomete-airflow-plugin",
    version="0.1.0",
    packages=find_packages(
        include=["iomete_airflow_plugin", "iomete_airflow_plugin.*"]
    ),
    entry_points={
        "airflow.plugins": [
            "iomete = iomete_airflow_plugin.plugin:IometePlugin"
        ]
    },
    keywords=['iomete', 'airflow', 'airflow plugin'],
    extras_require={
        'dev': ['black==19.10b0', 'watchdog==0.9.0', 'twine==1.14.0', 'apache-airflow~=2.5.1']
    },
    install_requires=[
        "requests",
        "setuptools~=67.0.0",
        "Flask~=2.2.3",
        "iomete-sdk==1.0.1",
    ],
)
