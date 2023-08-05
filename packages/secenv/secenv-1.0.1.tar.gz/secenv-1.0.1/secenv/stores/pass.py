import passpy
from . import StoreInterface, cached, ask_secret, SecretNotFoundError


class Store(StoreInterface):
    def __init__(self, name, infos):
        self.name = name
        directory = super().get_from_config(
            name, "directory", infos, default="~/.password-store"
        )
        self.store = passpy.Store(store_dir=directory)

    def gen_parser(self, parser):
        parser.add_argument("secret")

    @cached
    def read_secret(self, secret):
        res = self.store.get_key(secret)
        if res:
            return res
        else:
            raise SecretNotFoundError(self.name, secret)

    def fill_secret(self, secret):
        value = ask_secret(self.name, secret)
        self.store.set_key(secret, value, force=True)
