import os
import time
import uuid

import pytest as pytest

from iomete_sdk import SparkJobApiClient, ClientError

TEST_TOKEN = os.environ.get("TEST_TOKEN")
WORKSPACE_ID = "pceh7-816"

SPARK_VERSION = "3.2.1"


def random_job_name():
    return f"test-job-{uuid.uuid4().hex}"


@pytest.fixture
def create_payload() -> dict:
    return {
        "name": random_job_name(),
        "template": {
            "spark_version": SPARK_VERSION,
            "main_application_file": "local:///opt/spark/examples/jars/spark-examples_2.12-3.2.1-iomete.jar",
            "main_class": "org.apache.spark.examples.SparkPi",
            "arguments": ["10"]
        }
    }


@pytest.fixture
def job_client():
    return SparkJobApiClient(
        workspace_id=WORKSPACE_ID,
        api_key=TEST_TOKEN,
    )


def test_create_job_without_name_raise_400(job_client, create_payload):
    payload_without_name = {}

    with pytest.raises(ClientError) as err:
        response = job_client.create_job(payload=payload_without_name)

    assert err.value.status == 400
    assert err.value.content["error_code"] == "BAD_INPUT"
    assert "Name cannot be blank" in err.value.content["error_message"]


def test_create_job_successful(job_client, create_payload):
    response = job_client.create_job(payload=create_payload)

    assert response["name"] == create_payload["name"]
    assert response["workspace_id"] == WORKSPACE_ID
    assert response["id"] is not None

    # clean up
    job_client.delete_job_by_id(job_id=response["id"])


def test_update_job(job_client, create_payload):
    # create job
    job_create_response = job_client.create_job(payload=create_payload)

    cron_schedule = "0 0 */1 * *"

    # update job
    update_payload = job_create_response.copy()
    update_payload["schedule"] = cron_schedule
    job_update_response = job_client.update_job(job_id=job_create_response["id"], payload=update_payload)

    assert job_update_response["schedule"] == cron_schedule
    assert job_update_response["job_type"] == "SCHEDULED"
    assert job_update_response["name"] == job_create_response["name"]
    assert job_update_response["workspace_id"] == job_create_response["workspace_id"]
    assert job_update_response["id"] == job_create_response["id"]

    # clean up
    job_client.delete_job_by_id(job_id=job_update_response["id"])


def test_get_jobs(job_client):
    response = job_client.get_jobs()

    assert len(response["items"]) > 0

    job = response["items"][0]
    assert job["workspace_id"] == WORKSPACE_ID
    assert job["id"] is not None


def test_get_job_by_id(job_client, create_payload):
    # create job
    job = job_client.create_job(payload=create_payload)

    # check job is created
    response = job_client.get_job_by_id(job_id=job["id"])

    assert response["item"] is not None
    assert response["permissions"] is not None

    job = response["item"]
    assert job["workspace_id"] == WORKSPACE_ID
    assert job["name"] == create_payload["name"]
    assert job["id"] is not None

    # clean up
    job_client.delete_job_by_id(job_id=job["id"])


def test_delete_job_by_id(job_client, create_payload):
    # create job
    job = job_client.create_job(payload=create_payload)

    # check job is created
    response = job_client.get_job_by_id(job_id=job["id"])
    assert response["item"]["name"] == create_payload["name"]

    # delete job
    job_client.delete_job_by_id(job_id=job["id"])

    # check job is deleted
    with pytest.raises(ClientError) as err:
        job_client.get_job_by_id(job_id=job["id"])
    assert err.value.status == 404
    assert err.value.content["error_code"] == "NOT_FOUND"


def test_get_job_runs(job_client, create_payload):
    # create job
    job = job_client.create_job(payload=create_payload)

    # check job is created
    response = job_client.get_job_runs(job_id=job["id"])

    # should be empty run list
    assert response == []

    # clean up
    job_client.delete_job_by_id(job_id=job["id"])


def test_submit_job_run(job_client, create_payload):
    # create job
    job = job_client.create_job(payload=create_payload)

    # submit job run
    response = job_client.submit_job_run(job_id=job["id"], payload={})

    run_id = response["id"]

    assert run_id is not None
    assert response["job_id"] == job["id"]

    # sleep 5 seconds before cleaning up
    time.sleep(5)

    # clean up
    job_client.cancel_job_run(job_id=job["id"], run_id=run_id)
    job_client.delete_job_by_id(job_id=job["id"])
