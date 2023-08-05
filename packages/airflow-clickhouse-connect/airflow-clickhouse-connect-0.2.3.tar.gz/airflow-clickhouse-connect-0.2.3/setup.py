﻿from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='airflow-clickhouse-connect',
    version='0.2.3',
    url='https://github.com/amirtaherkhani/airflow-clickhouse-plugin',
    project_urls={
        "Bug Tracker": "https://github.com/amirtaherkhani/airflow-clickhouse-plugin/issues",
    },
    license='Apache License 2.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    author='Amir taherkhani',
    author_email='amirtaherkhani@outlook.com',
    description='Apache Airflow providers for Yandex Clickhouse Database',
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "apache_airflow_provider": [
            "provider_info=apache.__init__:get_provider_info"
        ]
    },
    packages=['apache',
              'apache.airflow',
              'apache.airflow.providers',
              'apache.airflow.providers.clickhouse',
              'apache.airflow.providers.clickhouse.hooks',
              'apache.airflow.providers.clickhouse.operators'
              ],
    install_requires=['apache-airflow>=2.0', 'clickhouse_driver>=0.2.1', 'pandas>=1.3.2'],
    keywords=['clickhouse', 'airflow', 'providers', 'database', 'ClickhouseHook', 'ClickhouseOperator'],
    include_package_data=True,
    python_requires=">=3.8"
)
