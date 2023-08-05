from typing import Iterable, List, Mapping, Optional, Union
from airflow.models import BaseOperator
from pandas import pandas
from apache.airflow.providers.clickhouse.hooks.ClickhouseHook import ClickHouseHook


class ClickhouseOperator(BaseOperator):
    """

    ClicHouseOperator provide Airflow operator execute query on Clickhouse instance
    @author = amirtaherkhani@outlook.com

    """
    template_fields = ('sql',)
    template_ext = ('.sql',)

    parameters = {
        "client_name":      "airflow-providers-clickhouse",
        "strings_encoding": "utf-8",
        "strings_as_bytes": True
    }

    def __init__(
            self,
            *,
            sql: Union[str, List[str]],
            clickhouse_conn_id: str = 'clickhouse_default',
            parameters: Optional[Union[Mapping, Iterable]] = None,
            settings: Optional[Union[Mapping, Iterable]] = None,
            **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        if parameters:
            self.parameters.update(parameters)
        if settings:
            self.settings.update(settings)
        self.sql = sql
        self.clickhouse_conn_id: str = clickhouse_conn_id
        self.hook = None

    def execute(self, context) -> None:
        self.log.info('Executing: %s', self.sql)
        client = ClickHouseHook(clickhouse_conn_id=self.clickhouse_conn_id)
        self.log.info('Load client: %s', client)
        rows, col_definitions = client.run(
            sql=self.sql, parameters=self.parameters, settings=self.settings, with_column_types=True)
        columns = [column_name for column_name, _ in col_definitions]
        data = pandas.DataFrame(
            rows, columns=columns).to_json(orient='records')
        self.log.debug('Dataframe info : %s', data.info(verbose=True))
        if self.do_xcom_push:
            # An XCom is identified by a key (essentially its name), as well as the task_id and dag_id it came from.
            # They can have any (serializable) value, but they are only designed for small amounts of data;
            # do not use them to pass around large values, like dataframes.
            # DOCS : https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html
            self.xcom_push(context, "query_result", data)
        del data
        return
