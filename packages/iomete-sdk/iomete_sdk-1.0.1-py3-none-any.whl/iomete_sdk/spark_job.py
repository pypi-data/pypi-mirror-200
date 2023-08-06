import json
import logging
from dataclasses import dataclass

import requests

SPARK_JOB_ENDPOINT = "/api/v1/workspaces/{workspace_id}/spark-jobs"


@dataclass
class ClientError(Exception):
    status: int
    content: dict

    def __str__(self):
        return self.__repr__()


@dataclass
class SparkJobApiClient:
    logger = logging.getLogger('SparkJobApiClient')

    workspace_id: str
    api_key: str
    base_url: str = None
    spark_job_endpoint: str = None

    def __post_init__(self):
        controller_host = self._get_controller_host()
        self.logger.debug(f"Controller host: {controller_host}")

        self.base_url = f"https://{self._get_controller_host()}"
        self.spark_job_endpoint = self.base_url + SPARK_JOB_ENDPOINT.format(workspace_id=self.workspace_id)

    def _get_controller_host(self):
        result = self._call_api(
            method="GET", url=f"https://account.iomete.com/api/v1/workspaces/{self.workspace_id}/info")
        return result["controller_endpoint"]

    def _call_api(self, method: str, url: str, payload: dict = None, ):
        try:
            headers = {
                "Content-Type": "application/json",
                "X-API-TOKEN": self.api_key
            }

            response = requests.request(method=method, url=url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP Error: {e}")
            self.logger.info(f"Response content: {response.content}")

            json_content = json.loads(response.content)
            raise ClientError(status=response.status_code, content=json_content)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request Exception: {e}")
            raise

    def create_job(self, payload: dict):
        return self._call_api(method="POST", url=self.spark_job_endpoint, payload=payload)

    def update_job(self, job_id: str, payload: dict):
        return self._call_api(method="PUT", url=f"{self.spark_job_endpoint}/{job_id}", payload=payload)

    def get_jobs(self):
        return self._call_api(method="GET", url=self.spark_job_endpoint)

    def get_job_by_id(self, job_id: str):
        return self._call_api(method="GET", url=f"{self.spark_job_endpoint}/{job_id}")

    def delete_job_by_id(self, job_id: str):
        return self._call_api(method="DELETE", url=f"{self.spark_job_endpoint}/{job_id}")

    def get_job_runs(self, job_id: str):
        return self._call_api(method="GET", url=f"{self.spark_job_endpoint}/{job_id}/runs")

    def submit_job_run(self, job_id: str, payload: dict):
        return self._call_api(method="POST", url=f"{self.spark_job_endpoint}/{job_id}/runs", payload=payload)

    def cancel_job_run(self, job_id: str, run_id: str):
        return self._call_api(method="DELETE", url=f"{self.spark_job_endpoint}/{job_id}/runs/{run_id}")

    def get_job_run_by_id(self, job_id: str, run_id: str):
        return self._call_api(method="GET", url=f"{self.spark_job_endpoint}/{job_id}/runs/{run_id}")

    def get_job_run_logs(self, job_id: str, run_id: str):
        return self._call_api(method="GET", url=f"{self.spark_job_endpoint}/{job_id}/runs/{run_id}/logs")

    def get_job_run_metrics(self, job_id: str, run_id: str):
        return self._call_api(method="GET", url=f"{self.spark_job_endpoint}/{job_id}/runs/{run_id}/metrics")
