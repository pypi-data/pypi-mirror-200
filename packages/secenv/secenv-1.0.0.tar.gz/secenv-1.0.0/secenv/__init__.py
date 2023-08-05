#!/usr/bin/env python

import argparse
import importlib
import pathlib
import sys
from typing import Dict

import pkg_resources
import yaml

from . import context
from .stores import StoreInterface, fill_secret, read_secret

VERSION = pkg_resources.get_distribution("secenv").version

config = {}
no_config_available = True


def load_config():
    """
    Load the configuration file and converts it from YAML to a Python object.
    """
    global config, no_config_available
    if pathlib.Path(".secenv.yaml").exists():
        config = yaml.load(open(".secenv.yaml", "r"), Loader=yaml.Loader)
    elif pathlib.Path(".secenv.yml").exists():
        config = yaml.load(open(".secenv.yml", "r"), Loader=yaml.Loader)
    else:
        print("Config error: .secenv.yaml not found")
        return

    if config:
        no_config_available = False
    else:
        print("Config error: file is empty")


def parse_args(stores: Dict[str, StoreInterface]) -> argparse.Namespace:
    """
    Parse the arguments provided to the program.

    Args:
        stores (Dict[str, StoreInterface]): A dictionary where the keys are the name of
            the store and the keys are the StoreInterface instantiations

    Returns:
        argparse.Namespace: A dictionary where the keys are the arguments of the program
            and the keys are the associated values
    """
    parser = argparse.ArgumentParser()
    subparsers_group = parser.add_subparsers()
    subparsers = {}

    subparsers["version"] = subparsers_group.add_parser(
        "version", help="get secenv version"
    )

    subparsers["secrets"] = subparsers_group.add_parser(
        "secrets", help="fill secrets in the stores"
    )

    subparsers["contexts"] = subparsers_group.add_parser(
        "contexts", help="list available contexts"
    )

    subparsers["context"] = subparsers_group.add_parser(
        "context", help="generate an environment based on a context"
    )
    subparsers["context"].add_argument("context")
    subparsers["context"].add_argument(
        "-o",
        "--output-format",
        choices=context.available_formats,
        default="shell",
        dest="format",
        help="output format",
    )

    for store in stores:
        if "extends" in config["stores"][store]:
            extended = config["stores"][store]["extends"]
            type = config["stores"][extended]["type"]
        else:
            type = config["stores"][store]["type"]
        subparsers[store] = subparsers_group.add_parser(
            store,
            help=f"query store '{store}' of type '{type}'",
        )
        stores[store].gen_parser(subparsers[store])

    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()

    return parser.parse_args()


def find_stores() -> Dict[str, StoreInterface]:
    """
    Find the stores defined in the configuration object.
    For each found store, instantiate it based on its type.

    Returns:
        Dict[str, StoreInterface]: A dictionary where the keys are the name of the
            stores and the keys are the StoreInterface instantiations

    Raises:
        SystemExit: If the configuration is not valid
    """
    stores = {}
    if "stores" not in config:
        return stores

    for name in config["stores"]:
        infos = config["stores"][name]

        if "extends" in infos:
            extended = infos["extends"]
            if extended not in config["stores"]:
                print("Config error: extended store does not exist:", extended)
                sys.exit(1)
            extended_infos = config["stores"][extended]
            extended_infos.update(infos)
            infos = extended_infos

        try:
            store = importlib.import_module(
                f".stores.{infos['type']}", package="secenv"
            )
        except ModuleNotFoundError:
            print(f"Config error: no store defined as '{infos['type']}'")
            sys.exit(1)
        stores[name] = store.Store(name, infos)

    return stores


def fill_secrets(stores: Dict[str, StoreInterface]) -> None:
    """
    Fill the secrets defined in the configuration object.

    Args:
        stores (Dict[str, StoreInterface]): A dictionary where the keys are the name of
            the stores and the keys are the StoreInterface instantiations
    """
    for secret_config in config["secrets"]:
        if "secret" not in secret_config:
            print("Config error: a secret has no name")
            continue
        secret_name = secret_config["secret"]

        if "store" not in secret_config:
            print(f"Config error: 'store' not found in secret {secret_name}")
            sys.exit(1)

        if secret_config["store"] not in stores:
            print(f"Config error: store '{secret_config['store']}' not found")
            sys.exit(1)

        store = stores[secret_config["store"]]
        secret = {k: v for k, v in secret_config.items() if k not in ["store"]}
        fill_secret(store, secret)


def gen_context(name: str, stores: Dict[str, StoreInterface]) -> Dict[str, str]:
    """
    Generate the context specified in the configuration object.

    Args:
        name (str): Name of the context to generate
        stores (Dict[str, StoreInterface]): A dictionary where the keys are the name of
            the stores and the keys are the StoreInterface instantiations

    Returns:
        Dict[str, str]: A dictionary of variables with their associated values

    Raises:
        SystemExit: If the configuration is not valid
    """
    context_config = config["contexts"][name]
    output = {}

    if context_config is None:
        print(f"Config error: context '{name}' is empty")
        sys.exit(1)

    if "extends" in context_config:
        for extended in context_config["extends"]:
            if extended not in config["contexts"]:
                print(f"Config error: try to extend an unexistent context '{extended}'")
                sys.exit(1)
            if extended == name:
                print("Config error: can't extend a context with itself")
                sys.exit(1)
            extended_context = gen_context(extended, stores)
            output.update(extended_context)

    if "vars" in context_config:
        output.update(context.gen_vars(context_config["vars"], stores))

    if "aws_assume_role" in context_config:
        creds = {}
        creds["key_id"] = context_config["aws_assume_role"]["aws_access_key_id"]
        creds["secret_key"] = context_config["aws_assume_role"]["aws_secret_access_key"]
        creds["role"] = context_config["aws_assume_role"]["role_arn"]

        output.update(context.gen_aws_assume_role(creds, stores))

    return output


def list_contexts() -> str:
    """
    List the contexts specified in the configuration object.

    Returns:
        str: List of contexts separated by newlines
    """
    if "contexts" in config:
        return "\n".join(config["contexts"])
    else:
        return ""


def main():
    if len(sys.argv) == 2 and "version" == sys.argv[1]:
        print(f"secenv version {VERSION}")
        sys.exit(0)

    load_config()
    stores = {} if no_config_available else find_stores()
    args = parse_args(stores)

    # remove empty values and 'type' key
    args = {k: v for k, v in vars(args).items() if k != "type" and v}

    if "secrets" in sys.argv[1]:
        if "secrets" not in config:
            print("Config error: 'secrets' block is not present")
            sys.exit(1)
        fill_secrets(stores)
        return

    elif "context" in sys.argv[1]:
        if sys.argv[1].endswith("s"):
            # secenv contexts
            print(list_contexts())
            return

        else:
            # secenv context <ctx>
            context_name = args["context"]
            if "contexts" not in config or context_name not in config["contexts"]:
                print(f"Config error: context '{context_name}' not found")
                sys.exit(1)
            ctx = gen_context(context_name, stores)
            print(context.format_output(ctx, args["format"]))
            return

    else:
        # retrieving a specific secret
        # TODO: replace sys.argv[1] with something more beautiful
        # like from 'args' directly
        store = stores[sys.argv[1]]
        result = read_secret(store, args)
        print(result)
        return


if __name__ == "__main__":
    main()
