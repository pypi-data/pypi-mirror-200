
def get_provider_info():
    return {
        "package-name":            "airflow-clickhouse-connect",
        "name":                    "Clickhouse",
        "description":             "Clickhouse provider for Airflow",
        "versions":                [
            "0.2.3"
        ],
        "additional-dependencies": [
            "apache-airflow>=2.2.0", "clickhouse_driver>=0.2.1", "pandas>=1.3.2"
        ],
        "integrations":            [
            {
                "integration-name": "Clickhouse",
                "external-doc-url": "https://github.com/amirtaherkhani/airflow-clickhouse-plugin",
                "tags":             [
                    "service", "clickhouse", "database", "airflow"
                ]
            }
        ],
        "operators":               [
            {
                "integration-name": "Clickhouse",
                "python-modules":   [
                    "apache.airflow.providers.clickhouse.operators.ClickhouseOperator"
                ]
            }
        ],
        "hooks":                   [
            {
                "integration-name": "Clickhouse",
                "python-modules":   [
                    "apache.airflow.providers.clickhouse.hooks.ClickhouseHook"
                ]
            }
        ],
        
        "sensors":                   [
            {
                "integration-name": "Clickhouse",
                "python-modules":   [
                    "apache.airflow.providers.clickhouse.sensors.ClickhouseSensor"
                ]
            }
        ],
        
        "connection-types":        [
            {
                "hook-class-name": "apache.airflow.providers.clickhouse.hooks.ClickhouseHook.ClickHouseHook",
                "connection-type": "clickhouse"
            }
        ]
    }
