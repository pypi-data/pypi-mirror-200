# this is a library used by dag users
from airflow.secrets import BaseSecretsBackend

import requests
import os
import json
import logging

log = logging.getLogger(__name__)


class OpSecretsBackend(BaseSecretsBackend):
    def get_connection(self, conn_id: str):  # conn_id here is OP connection name
        from airflow.models.taskinstance import _CURRENT_CONTEXT
        from airflow.configuration import ensure_secrets_loaded
        from airflow.exceptions import AirflowNotFoundException

        if _CURRENT_CONTEXT is None or len(_CURRENT_CONTEXT) == 0:
            raise Exception("failed to get _CURRENT_CONTEXT")
        run_id = _CURRENT_CONTEXT[0]["dag_run"].run_id
        dag_id = _CURRENT_CONTEXT[0]["dag_run"].dag_id
        id = _CURRENT_CONTEXT[0]["dag_run"].id
        AC_URL = os.getenv('AC_URL')
        param_values = {
            'run_id': run_id,
            'dag_id': dag_id,
            'id': id,
            'user_connection_name': conn_id,
        }
        url = AC_URL + "/airflow-connection-id"
        log.info("check connection in AC")
        response = requests.get(url, params=param_values)
        if response is None or response.status_code != 200:
            raise Exception("Cannot connect with AC")
        result = json.loads(response.text)
        print(result)
        if result[0] == 200:  # if user is sending a conn_name to get conn
            for secrets_backend in ensure_secrets_loaded():
                type_check_result = isinstance(secrets_backend, OpSecretsBackend)
                if type_check_result is False:
                    try:
                        conn = secrets_backend.get_connection(conn_id=result[1])
                        if conn:
                            return conn
                    except Exception:
                        log.exception(
                            "Unable to retrieve connection from secrets backend (%s). "
                            "Checking subsequent secrets backend.",
                            type(secrets_backend).__name__,
                        )

            raise AirflowNotFoundException(f"The conn_id `{result[1]}` isn't defined")
        else:  # assume user is sending a conn_id directly
            log.info("check connection in other backends")
            for secrets_backend in ensure_secrets_loaded():
                type_check_result = isinstance(secrets_backend, OpSecretsBackend)
                if type_check_result is False:
                    try:
                        conn = secrets_backend.get_connection(conn_id=conn_id)
                        if conn:
                            return conn
                    except Exception:
                        log.exception(
                            "Unable to retrieve connection from secrets backend (%s). "
                            "Checking subsequent secrets backend.",
                            type(secrets_backend).__name__,
                        )
            raise AirflowNotFoundException(
                result[1] + f" and conn_id `{conn_id}` isn't defined"
            )


def extendoperator(class_type, **kargs):
    class ExtendedClassOperator(class_type):
        """
        in the template field list, define the fields which
        need to be rendered by jinja template.
        In the code, on the top of
        BigQueryGetDataOperator's template_field list,
        we add 'ac_id', 'ac_run_id' and 'ac_dag_id'
        to the list. Then when we call the
        new class ExtendedBigQueryGetDataOperator,
        we can use jinja template syntax to pass
        dag related values to those three fields.
        """

        # template_fields will decide while
        # fields should be rendered by Jinja template
        def __init__(self, **kwargs) -> None:
            super().__init__(**kwargs)
            self.conn_name = kwargs['gcp_conn_id']

        def get_connection_id(self, id, run_id, dag_id):
            AC_URL = os.getenv('AC_URL')  # OP_AC_URL
            param_values = {
                'run_id': run_id,
                'dag_id': dag_id,
                'id': id,
                'user_connection_name': self.conn_name,
            }
            url = AC_URL + "/airflow-connection-id"
            r = requests.get(url, params=param_values)
            connection_result = json.loads(r.text)
            return connection_result[1]

        # continue the work in parent class
        # BigQueryGetDataOperator's method execute()

        def execute(self, context):
            self.gcp_conn_id = self.get_connection_id(
                context["dag_run"].id,
                context["dag_run"].run_id,
                context["dag_run"].dag_id,
            )
            super().execute(context)

    task = ExtendedClassOperator
    return task(**kargs)
