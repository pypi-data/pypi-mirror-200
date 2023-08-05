import subprocess
from . import StoreInterface, cached, SecretNotFoundError


class Store(StoreInterface):
    def __init__(self, name, infos):
        self.name = name
        # self.url = super().get_from_config(name, "url", infos)
        # self.user = super().get_from_config(name, "user", infos)
        # self.password = super().get_from_config(name, "password", infos)

    def gen_parser(self, parser):
        parser.add_argument("secret")

    @cached
    def read_secret(self, secret) -> str:
        result = subprocess.run(["rbw", "get", secret], capture_output=True)
        if result.returncode != 0:
            stderr = result.stderr.strip().decode("utf-8")
            if "no entry found" in stderr:
                raise SecretNotFoundError(self.name, secret)
            raise Exception(
                f"bitwarden store '{self.name}': rbw error during execution: {stderr}"
            )
        return result.stdout.strip().decode("utf-8")

    def fill_secret(self, secret):
        raise Exception("Can't write secrets to Bitwarden for now.")
