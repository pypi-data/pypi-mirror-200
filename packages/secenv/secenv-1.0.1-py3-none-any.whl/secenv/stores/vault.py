import hvac
import hvac.exceptions
from . import StoreInterface, ask_secret, cached, SecretNotFoundError


class Store(StoreInterface):
    def __init__(self, name, infos):
        self.name = name
        self.url = super().get_from_config(name, "url", infos)
        self.token = super().get_from_config(name, "token", infos)
        self.client = hvac.Client(url=self.url, token=self.token)

    def gen_parser(self, parser):
        parser.add_argument("secret")
        parser.add_argument("--key")
        parser.add_argument("--engine")

    @cached
    def read_secret(self, secret, engine=""):
        try:
            read_response = self.client.secrets.kv.read_secret_version(
                path=secret, mount_point=engine
            )
        except hvac.exceptions.InvalidPath as e:
            if "route entry not found" in str(e.text):
                raise SecretNotFoundError(self.name, secret)
            raise Exception(f"vault store '{self.name}': error during execution: {e}")

        return read_response

    def filter(self, secret, key):
        return secret["data"]["data"][key]

    def fill_secret(self, secret, engine="", keys=[]):
        if keys:
            values = {}
            for key in keys:
                values[key] = ask_secret(self.name, secret, key)
            secret_value = values
        else:
            secret_value = {secret: ask_secret(self.name, secret)}

        self.client.secrets.kv.create_or_update_secret(
            path=secret, mount_point=engine, secret=secret_value
        )
