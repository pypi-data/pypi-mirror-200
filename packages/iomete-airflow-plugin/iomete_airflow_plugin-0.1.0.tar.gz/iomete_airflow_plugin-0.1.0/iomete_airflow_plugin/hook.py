from airflow import AirflowException
from airflow.hooks.base import BaseHook
from airflow.models import Variable

from iomete_sdk import SparkJobApiClient


class IometeHook(BaseHook):
    def __init__(self, workspace_id):
        super().__init__()
        self.iom_access_token = Variable.get("iomete_access_token")

        self.iom_workspace_id = workspace_id or Variable.get(key="iomete_workspace_id", default_var=None)
        if self.iom_workspace_id is None:
            raise AirflowException(
                "Parameter `workspace_id` should be specified "
                "or defined in Airflow Variables with `iomete_default_workspace_id` key."
            )

        self.iom_client = SparkJobApiClient(
            workspace_id=self.iom_workspace_id,
            api_key=self.iom_access_token,
        )

    def submit_job_run(self, job_id, payload):
        response = self.iom_client.submit_job_run(job_id=job_id, payload=payload)
        return response

    def get_job_run(self, job_id, run_id):
        response = self.iom_client.get_job_run_by_id(job_id=job_id, run_id=run_id)
        return response

    def cancel_job_run(self, job_id, run_id):
        response = self.iom_client.cancel_job_run(job_id=job_id, run_id=run_id)
        return response
