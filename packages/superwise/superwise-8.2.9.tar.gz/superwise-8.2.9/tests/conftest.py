from http import HTTPStatus

import jwt
import pytest
import requests
from _pytest.monkeypatch import MonkeyPatch
from cryptography.hazmat.primitives.asymmetric import rsa
from google.cloud import storage
from google.oauth2 import service_account
from requests import Response

from superwise import Client
from superwise import Superwise
from superwise.utils.storage.internal_storage.aws import AWSInternalStorage
from superwise.utils.storage.internal_storage.azure import AzureInternalStorage
from superwise.utils.storage.internal_storage.gcs import GCSInternalStorage
from superwise.utils.storage.internal_storage.internal_storage import CloudProvider
from superwise.utils.storage.internal_storage.internal_storage import InternalStorage

monkey_patch = MonkeyPatch()


@pytest.fixture(scope="function")
def mock_gcp_internal_bucket(monkeypatch):
    monkeypatch.setattr(
        GCSInternalStorage,
        "_exchange_jwt_for_access_token",
        lambda *args, **kwargs: "access token",
    )

    monkeypatch.setattr(GCSInternalStorage, "_is_cloud_token_active", lambda *args, **kwargs: True)
    monkeypatch.setattr(GCSInternalStorage, "_put_in_storage", lambda *args, **kwargs: "gs://somepath")


@pytest.fixture(scope="function")
def mock_refresh_internal_bucket_token(monkeypatch):
    def mock_refresh_aws(self, *args, **kwargs):
        self._cloud_token = {
            "url": "https://test.s3.amazonaws.com/",
            "fields": {
                "key": "landing/test.csv",
                "AWSAccessKeyId": "asdasdasdasd",
                "x-amz-security-token": "adasdasdasd",
                "signature": "asdasd=",
            },
        }

    def mock_refresh_general(self, *args, **kwargs):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self._cloud_token = jwt.encode({"payload": "aaaaa"}, private_key, algorithm="RS256")

    monkeypatch.setattr(InternalStorage, "_refresh_cloud_token", mock_refresh_general)

    monkeypatch.setattr(AWSInternalStorage, "_refresh_cloud_token", mock_refresh_aws)


@pytest.fixture(scope="function")
def mock_azure_internal_bucket(monkeypatch):
    put_response = Response()
    put_response.status_code = HTTPStatus.OK
    monkeypatch.setattr(AzureInternalStorage, "_is_cloud_token_active", lambda *args, **kwargs: True)
    put_response = Response()
    put_response.status_code = 200
    monkeypatch.setattr(requests, "put", lambda *args, **kwargs: put_response)


@pytest.fixture(scope="function")
def mock_get_token(monkeypatch):
    def _mock_token(self):
        return {
            "expires": "Thu, 29 Sep 2022 08:00:41 GMT",
            "expiresIn": 86400,
            "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlkYmRlNzNkIn0.eyJzdWIiOiI0NGE4ODc3YS0yOWJhLTQ2NTYtOGY1OC1lMTQzYTM4MTQ5MTMiLCJlbWFpbCI6InN3X3Rlc3RzQHN1cGVyd2lzZS5haSIsInVzZXJNZXRhZGF0YSI6eyJvbmJvYXJkaW5nIjp0cnVlfSwidGVuYW50SWQiOiJ0ZXN0cyIsInJvbGVzIjpbIlVzZXIiXSwicGVybWlzc2lvbnMiOlsiZmUuc2VjdXJlLndyaXRlLnVzZXJBcGlUb2tlbnMiLCJmZS5zZWN1cmUuZGVsZXRlLnVzZXJBcGlUb2tlbnMiLCJmZS5zZWN1cmUucmVhZC51c2VyQXBpVG9rZW5zIiwiZmUuc2VjdXJlLnJlYWQudGVuYW50QXBpVG9rZW5zIl0sIm1ldGFkYXRhIjp7fSwiY3JlYXRlZEJ5VXNlcklkIjoiZTAyNGE1ZTItNzZkMS00N2YyLWE2NWUtMDViMTFjNzI2MDZlIiwidHlwZSI6InVzZXJBcGlUb2tlbiIsInVzZXJJZCI6ImUwMjRhNWUyLTc2ZDEtNDdmMi1hNjVlLTA1YjExYzcyNjA2ZSIsImF1ZCI6IjlkYmRlNzNkLWViODktNGMxMC05ZDY1LTYwNTI1ZGE0ZDlkNiIsImlzcyI6ImZyb250ZWdnIiwiaWF0IjoxNjY0MzUyMDQxLCJleHAiOjE2NjQ0Mzg0NDF9.UWEqljuU1txF5VDVIqJO8zDY10myPuYqIwx72ClriJh4fAW84jypeDoopVfD01kKHeZDGwJ9YmlGmc6rwQij7YPjXvMRlBSWdshz-2qM7rhY8IOuSBUsW-GgS9BUTKL14K1vbpZ6rLpTEJNoeAoIUKxztynbXhAZVEci78Q_bM29Bs-urSHrzy_hu0hrzAjDKyNkHkNB0DYLiqf03SzyuJDNlj-fvcXp0EaIeqT1FOcpSeJqPgJ57JXrsxg8o_IwZsN-AR_aGdb-zyw0hVwJCzF1wNWMUROo-o2yFBVBwlbh4PMBQkkTA0hiNNqMPI7rA45c2NVicok_e0bi6ZlYkA",
            "refreshToken": "26323edd-8551-422b-99b6-353c76139359",
        }

    monkeypatch.setattr(Client, "get_token", _mock_token)


@pytest.fixture
def mock_gcp_client(monkeypatch):
    parametrized_mock_gcp_client(1000)


def parametrized_mock_gcp_client(size):
    class GCSClient:
        def __init__(self, *args, **kwargs):
            self.name = "test"
            self.size = size

        def bucket(self, bucket_name):
            return GCSClient()

        def get_blob(self, file_name):
            return GCSClient()

        def blob(self, file_name):
            return GCSClient()

        def download_as_string(self):
            return "asdasdaas"

        def upload_from_string(self, data):
            return None

    monkey_patch.setattr(service_account.Credentials, "from_service_account_info", lambda *args, **kwargs: "")
    monkey_patch.setattr(storage, "Client", lambda *args, **kwargs: GCSClient())


# running in all cloud providers environments
@pytest.fixture(scope="function", params=[provider.value for provider in CloudProvider])
def mock_admin_settings(monkeypatch, request):
    settings = {
        "file_upload_settings": {
            "cloud_provider": request.param,
            "azure_account_name": "test",
            "azure_container_name": "test",
            "gcs_bucket_name": "test",
            "s3_bucket_name": "test",
        }
    }
    monkeypatch.setattr(Superwise, "_get_admin_settings", lambda *args, **kwargs: settings)


@pytest.fixture(scope="function")
def sw(
    mock_admin_settings,
    mock_get_token,
    mock_refresh_internal_bucket_token,
    mock_gcp_internal_bucket,
    mock_azure_internal_bucket,
):
    return Superwise(client_id="test", secret="test")
