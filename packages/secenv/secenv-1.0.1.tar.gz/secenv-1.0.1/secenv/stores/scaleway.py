import base64
import json
import requests

from . import StoreInterface, ask_secret, cached, SecretNotFoundError


class Store(StoreInterface):
    def __init__(self, name, infos):
        self.name = name
        region = super().get_from_config(name, "region", infos)
        self.project_id = super().get_from_config(name, "project_id", infos)
        self.token = super().get_from_config(name, "token", infos)

        self.base_url = (
            f"https://api.scaleway.com/secret-manager/v1alpha1/regions/{region}"
        )

    def _get(self, url) -> str:
        if not url.startswith("/"):
            url = "/" + url
        ret = requests.get(self.base_url + url, headers={"X-Auth-Token": self.token})
        return ret.text

    def _post(self, url, data) -> str:
        if not url.startswith("/"):
            url = "/" + url
        ret = requests.post(
            self.base_url + url, headers={"X-Auth-Token": self.token}, json=data
        )
        return ret.text

    def _name_to_uid(self, secret):
        ret = json.loads(self._get(f"secrets-by-name/{secret}"))
        if "type" in ret and ret["type"] == "not_found":
            raise Exception(f"Secret '{secret}' not found in store '{self.name}'")
            # raise SecretNotFoundError
        return ret["id"]

    def gen_parser(self, parser):
        parser.add_argument("secret")
        parser.add_argument("--key")

    @cached
    def read_secret(self, secret) -> str:
        uid = self._name_to_uid(secret)
        ret = self._get(f"secrets/{uid}/versions/latest/access")
        ret = json.loads(ret)
        if "type" in ret and ret["type"] == "not_found":
            raise SecretNotFoundError(self.name, secret)
        return base64.b64decode(ret["data"]).decode()

    def filter(self, secret, key):
        return json.loads(secret)[key]

    def fill_secret(self, secret, keys=[]):
        if keys:
            values = {}
            for key in keys:
                values[key] = ask_secret(self.name, secret, key)
            secret_value = json.dumps(values)
        else:
            secret_value = ask_secret(self.name, secret)

        try:
            uid = self._name_to_uid(secret)
        except Exception:
            # except SecretNotFoundError:
            ret = self._post(
                "secrets", {"name": secret, "project_id": self.project_id, "tags": []}
            )
            uid = json.loads(ret)["id"]

        url = f"secrets/{uid}/versions"
        data = {"data": base64.b64encode(secret_value.encode()).decode()}
        self._post(url, data)
