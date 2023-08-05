import boto3
import pandas as pd
import pytest
import requests
from _pytest.monkeypatch import MonkeyPatch

from project_root import PROJECT_ROOT
from superwise.models.dataset import Dataset
from superwise.utils.exceptions import SuperwiseDatasetFailureError
from superwise.utils.exceptions import SuperwiseFileTooLargeError
from superwise.utils.exceptions import SuperwiseTimeoutError
from tests.conftest import parametrized_mock_gcp_client

monkey_patch = MonkeyPatch()


@pytest.fixture
def mock_boto_client():
    parametrized_mock_boto_client(1000)


def parametrized_mock_boto_client(file_size):
    class BotoClient:
        def __init__(self, *args, **kwargs):
            pass

        def get_object(self, *args, **kwargs):
            class ObjectResposne:
                def read(self):
                    return "blablabla"

            return dict(Body=ObjectResposne())

        def head_object(self, *args, **kwargs):
            return {"ContentLength": file_size}

    monkey_patch.setattr(boto3, "client", lambda *args, **kwargs: BotoClient())


@pytest.fixture
def mock_post_response(monkeypatch):
    post_response = requests.Response()
    post_response._content = (
        b'{ "id" : "123" ,"status" : "summarized", "project_id": 1, "name": "test", "files": ' b'"test.csv"}'
    )
    post_response.status_code = 201
    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: post_response)


@pytest.fixture
def mock_file_uploaded_post_response(monkeypatch):
    post_response = requests.Response()
    post_response._content = (
        b'{ "id" : "123" ,"status" : "file_uploaded", "project_id": 1, "name": "test", "files": ' b'"test.csv"}'
    )
    post_response.status_code = 201
    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: post_response)


@pytest.fixture
def mock_get_response(monkeypatch):
    get_response = requests.Response()
    get_response._content = (
        b'{ "id" : "123" ,"status" : "summarized", "project_id": 1, "name": "test", "files": ' b'"test.csv"}'
    )
    get_response.status_code = 200
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: get_response)


@pytest.fixture
def mock_failed_get_response(monkeypatch):
    get_response = requests.Response()
    get_response._content = (
        b'{ "id" : "123" ,"status" : "failed", "status_reason": "internal_error", "project_id": 1, "name": "test", "files": '
        b'"test.csv"}'
    )
    get_response.status_code = 200
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: get_response)


@pytest.fixture
def mock_not_finished_get_response(monkeypatch):
    get_response = requests.Response()
    get_response._content = (
        b'{ "id" : "123" ,"status" : "inferring_roles", "project_id": 1, "name": "test", "files": ' b'"test.csv"}'
    )
    get_response.status_code = 200
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: get_response)


@pytest.fixture
def files():
    return ["gs://bucket/test.csv", "s3://bucket/test.csv", f"{PROJECT_ROOT}/tests/resources/dataset/test.csv"]


@pytest.fixture
def basic_dataset(files):
    return Dataset(name="test", files=files, project_id=1)


@pytest.fixture
def dataframe_dataset(files):
    df = pd.read_csv(f"{PROJECT_ROOT}/tests/resources/dataset/test.csv")
    return Dataset.generate_dataset_from_dataframe(name="test", dataframe=df, project_id=1)


def test_create_dataset_default_params(
    sw, mock_gcp_client, files, basic_dataset, mock_boto_client, mock_get_response, mock_post_response
):
    new_dataset = sw.dataset.create(basic_dataset)

    assert new_dataset.status == "summarized"
    assert new_dataset.id == "123"
    assert new_dataset.project_id == 1
    assert new_dataset.name == "test"
    assert new_dataset.files == "test.csv"


def test_create_dataset_dataframe(
    sw, mock_gcp_client, files, dataframe_dataset, mock_boto_client, mock_get_response, mock_post_response
):
    new_dataset = sw.dataset.create(dataframe_dataset)

    assert new_dataset.status == "summarized"
    assert new_dataset.id == "123"
    assert new_dataset.project_id == 1
    assert new_dataset.name == "test"
    assert new_dataset.files == "test.csv"


def test_create_dataset_on_failure_raise(
    sw, mock_gcp_client, files, basic_dataset, mock_boto_client, mock_failed_get_response, mock_post_response
):
    with pytest.raises(SuperwiseDatasetFailureError) as e:
        sw.dataset.create(basic_dataset)

    assert (
        e.value.args[0] == f"Dataset creation failed for ID '123'. "
        f"got status: 'failed', with reason: 'internal_error'"
    )


def test_create_dataset_on_failure_ignore(
    sw, mock_gcp_client, files, basic_dataset, mock_boto_client, mock_failed_get_response, mock_post_response
):
    new_dataset = sw.dataset.create(basic_dataset, on_failure="ignore")

    assert new_dataset.status == "failed"
    assert new_dataset.id == "123"
    assert new_dataset.project_id == 1
    assert new_dataset.name == "test"
    assert new_dataset.files == "test.csv"


def test_create_dataset_do_not_wait_until_complete(
    sw, mock_gcp_client, files, basic_dataset, mock_boto_client, mock_get_response, mock_post_response
):
    new_dataset = sw.dataset.create(basic_dataset, wait_until_complete=False)

    assert new_dataset.status == "summarized"
    assert new_dataset.id == "123"
    assert new_dataset.project_id == 1
    assert new_dataset.name == "test"
    assert new_dataset.files == "test.csv"


def test_create_dataset_time_out(
    sw, mock_gcp_client, files, basic_dataset, mock_boto_client, mock_not_finished_get_response, mock_post_response
):
    with pytest.raises(SuperwiseTimeoutError) as e:
        sw.dataset.create(basic_dataset, timeout_seconds=1)

    assert (
        e.value.args[0] == "Timed out while waiting for dataset with ID: '123' to be in one of "
        f"the statuses ['summarized', 'failed'], "
        f"got status: 'inferring_roles', with reason: '<unknown reason>'"
    )


def test_create_dataset_on_timeout_ignore(
    sw,
    mock_gcp_client,
    files,
    basic_dataset,
    mock_boto_client,
    mock_not_finished_get_response,
    mock_file_uploaded_post_response,
):
    new_dataset = sw.dataset.create(basic_dataset, timeout_seconds=1, on_failure="ignore")

    assert new_dataset.status == "file_uploaded"
    assert new_dataset.id == "123"
    assert new_dataset.project_id == 1
    assert new_dataset.name == "test"
    assert new_dataset.files == "test.csv"


def test_create_dataset_single_file_too_large(
    sw, basic_dataset, mock_boto_client, mock_get_response, mock_post_response
):
    parametrized_mock_gcp_client(160000000)

    with pytest.raises(SuperwiseFileTooLargeError) as e:
        sw.dataset.create(basic_dataset)

    assert e.value.args[0] == "File 'gs://bucket/test.csv' is too large: (160.0 MB), maximum size allowed is 100.0 MB"


def test_create_dataset_total_size_too_large(sw, basic_dataset, mock_get_response, mock_post_response):
    parametrized_mock_gcp_client(100000000)
    parametrized_mock_boto_client(60000000)

    with pytest.raises(SuperwiseFileTooLargeError) as e:
        sw.dataset.create(basic_dataset)

    assert (
        e.value.args[0] == "The *total* size of the files: ['gs://bucket/test.csv', 's3://bucket/test.csv'] "
        "is too large: (160.0 MB), maximum size allowed is 100.0 MB"
    )
