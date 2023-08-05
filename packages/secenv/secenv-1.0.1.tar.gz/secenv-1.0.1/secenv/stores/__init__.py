import argparse
import os
from abc import ABC, abstractmethod
from ..utils import gen_uid, yes_no, SecretNotFoundError


EnvPrefix = "SECENV"

cached_secrets = {}


def cached(fn):
    def inner(*args, **kwargs):
        store = fn.__module__.replace("secenv.stores.", "")

        cache_key = gen_uid(store, kwargs)

        if cache_key in cached_secrets:
            return cached_secrets[cache_key]

        result = fn(*args, **kwargs)
        cached_secrets[cache_key] = result

        return result

    return inner


def read_secret(store, args):
    key = None
    if "key" in args:
        key = args["key"]
        del args["key"]

    secret = store.read_secret(**args)
    if key:
        return store.filter(secret, key)
    else:
        return secret


def fill_secret(store, secret):
    secret_already_exists = False
    try:
        secret_without_keys = {k: v for k, v in secret.items() if k != "keys"}
        if store.read_secret(**secret_without_keys):
            secret_already_exists = True
    except SecretNotFoundError:
        pass

    if secret_already_exists and not yes_no(
        f"Secret '{secret['secret']}' already exists in store '{store.name}', overwrite?"
    ):
        return

    store.fill_secret(**secret)


def ask_secret(store, name, key=""):
    ask_str = f"Value for secret '{name}' in store '{store}'"
    if key:
        ask_str += f" (key: '{key}')"
    ask_str += "? "

    res = input(ask_str)

    while res.startswith("file:"):
        filename = res[5:].strip()
        if not os.path.exists(filename):
            print("File doesn't exist:", filename)
            res = input(ask_str)
            continue
        if not os.path.isfile(filename):
            print("This is not a file:", filename)
            res = input(ask_str)
            continue

        with open(filename, "r") as f:
            res = f.read()

    return res


class StoreInterface(ABC):
    @abstractmethod
    def __init__(self, name: str, infos: dict) -> None:
        """Init the store, check the provided keys, and create possible client"""
        pass

    def get_from_config(self, store: str, value: str, infos: dict, default=None) -> str:
        if value not in infos and f"{EnvPrefix}_{store}_{value}" not in os.environ:
            if default is None:
                raise Exception(
                    f"Config error: '{value}' is required in store '{store}'"
                    f" or {EnvPrefix}_{store}_{value} in env"
                )
            else:
                return default
        return infos.get(value, os.getenv(f"{EnvPrefix}_{store}_{value}"))

    @abstractmethod
    def gen_parser(self, parser: argparse.ArgumentParser) -> None:
        """Generate the parser that reads the arguments and options"""
        pass

    @abstractmethod
    def read_secret(self, secret: str) -> str:
        """Read a secret from the desired password store"""
        pass
