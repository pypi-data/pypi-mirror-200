import src.op_secrets_backend.op_secrets_backend as op_secrets_backend
from airflow.models import BaseOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryGetDataOperator

def test_extendoperator(mocker):
    print("sida check")
    test_class = op_secrets_backend.extendoperator(BigQueryGetDataOperator, task_id="test_get_data_from_bq_test_1",
            dataset_id='access_control',
            table_id='conncection_mapping',
            max_results=100,
            gcp_conn_id="sida_test_1")
    assert test_class.gcp_conn_id == "sida_test_1"


def test_extendoperator_execute(mocker):
    print("sida check")
    test_class = op_secrets_backend.extendoperator(BigQueryGetDataOperator, task_id="test_get_data_from_bq_test_1",
            dataset_id='access_control',
            table_id='conncection_mapping',
            max_results=100,
            gcp_conn_id="sida_test_1")
    print(list(test_class.__dict__.keys()))
    assert test_class.gcp_conn_id == "sida_test_1"

