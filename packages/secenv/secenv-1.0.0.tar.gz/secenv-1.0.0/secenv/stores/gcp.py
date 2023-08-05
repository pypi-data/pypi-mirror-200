import os
import google.api_core.exceptions
from google.cloud import secretmanager
from . import StoreInterface, cached, ask_secret, SecretNotFoundError


def _setup_creds(fn):
    def inner(*args, **kwargs):
        # args[0] == self
        creds = args[0]._creds
        if creds:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds
        res = fn(*args, **kwargs)
        if creds:
            del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
        return res

    return inner


class Store(StoreInterface):
    def __init__(self, name, infos):
        self._existing_secrets = {}

        self.name = name
        self.project_id = super().get_from_config(name, "project_id", infos)

        # https://cloud.google.com/docs/authentication/provide-credentials-adc#local-key
        # To use service account keys,
        # the library looks for the `GOOGLE_APPLICATION_CREDENTIALS`
        # environment value.
        self._creds = super().get_from_config(
            name, "google_application_credentials", infos, default=""
        )

        self.client = secretmanager.SecretManagerServiceClient()

    def gen_parser(self, parser):
        parser.add_argument("secret")

    @cached
    @_setup_creds
    def read_secret(self, secret) -> str:
        parent = f"projects/{self.project_id}"
        name = f"{parent}/secrets/{secret}/versions/latest"

        try:
            secret_obj = self.client.access_secret_version(request={"name": name})
        except google.api_core.exceptions.NotFound:
            raise SecretNotFoundError(self.name, secret)

        self._existing_secrets[secret] = True
        return secret_obj.payload.data.decode()

    def fill_secret(self, secret):
        secret_value = ask_secret(self.name, secret)

        if secret not in self._existing_secrets:
            self.client.create_secret(
                request={
                    "parent": f"projects/{self.project_id}",
                    "secret_id": secret,
                    "secret": {"replication": {"automatic": {}}},
                }
            )
            self._existing_secrets[secret] = True

        name = f"projects/{self.project_id}/secrets/{secret}"
        self.client.add_secret_version(
            request={
                "parent": name,
                "payload": {"data": secret_value.encode()},
            }
        )
