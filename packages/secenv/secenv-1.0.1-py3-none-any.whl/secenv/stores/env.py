import os
from . import StoreInterface, cached, ask_secret, SecretNotFoundError


class Store(StoreInterface):
    def __init__(self, name, infos):
        self.name = name

    def gen_parser(self, parser):
        parser.add_argument("secret")

    @cached
    def read_secret(self, secret):
        res = os.getenv(secret)
        if res:
            return res
        else:
            raise SecretNotFoundError(self.name, secret)

    def fill_secret(self, secret):
        os.environ[secret] = ask_secret(self.name, secret)
