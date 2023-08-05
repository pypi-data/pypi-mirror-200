# SecEnv

`secenv` is an utility tool to list, read and fill secrets from multiple stores.
It also defines contexts, and generates the associated environment values.

The end-user documentation is available [on the official website](https://secenv.keltio.fr).
This document is indented to cover the technical documentation for current and future developers.

- [SecEnv](#secenv)
  - [Contributors](#contributors)
  - [Code of conduct](#code-of-conduct)
  - [Repository structure](#repository-structure)
  - [`make` commands](#make-commands)
  - [Running](#running)
  - [Testing](#testing)
  - [Git flow](#git-flow)
  - [Development](#development)
    - [Adding a store](#adding-a-store)
      - [Caching retrieved secrets](#caching-retrieved-secrets)
      - [Default config value](#default-config-value)
      - [Key-value store inside a secret](#key-value-store-inside-a-secret)
  - [Adding an output format for contexts](#adding-an-output-format-for-contexts)


## Contributors

Because an open-source project can't live without a community, we would like to thank our dear contributors.
Thank you so much:

- Valentin Merlo, @valentin137


## Code of conduct

This project uses Python 3.7+.
It is indented using Black.

The philosophy of `secenv` is to keep it simple.
It means we don't want to add *fancy* functionalities that require a lot of maintenance, but instead we want to focus on useful and reliable features.

The codebase aims to be easy to read, easy to understand, easy to debug, easy to improve, easy to maintain.

When modifications are made to the codebase, please wonder if the statement above is still respected.


## Repository structure

The `secenv` codebase is designed around the different functionalities.
Here is the global structure of the repository:


```
./
│   > Docs are handled by Docusaurus
├── docs/ -> .docusaurus/docs/
├── .docusaurus/
│
│   > General files
├── CHANGELOG.md
├── LICENSE
├── Makefile
├── README.md
│
│   > Sources
├── pyproject.toml
├── secenv/
├── setup.py
└── tests/
```

The `./secenv` directory contains the actual code, and is arranged as this:

```
./secenv/
│   > Entrypoint
├── __init__.py
│
│   > Context generation and output
├── context.py
├── contexts/
│
│   > Stores definition
├── stores/
│
│   > Utils functions
└── utils.py
```


## `make` commands

The project is managed using a Makefile.
To list the available commands, run:

```
$ make help
Usage: make <target>

Installation
  install-local    Install secenv as a local package
  install-test     Install secenv from TestPyPI
  install          Install secenv from PyPI
  uninstall        Uninstall secenv

Package
  dist             Generate wheel package for PyPI
  check            Check package with twine
  upload-test      Upload the package to TestPyPI
  upload           Upload the package to PyPI

Documentation
  docs-preview     Generate a live preview of the docs
  docs-bump        Create a new version of the documentation
  docs-publish     Publish the docs

Release
  changelog        Update the changelog with the changes since the last tag
  bump-version     Compute the new version and update files accordingly
  git-publish      Create a new tag/commit and push it

Utils
  deps             Install test & build dependencies
  tests            Run the unit tests
  clean            Remove build and dist files
  docker-node      Run a Node:latest image with '-v $pwd:/app -p 3000'
  docker-python    Run a Python:$VERSION image with '-v $pwd:/app'
```


## Running

To install the required dependencies for development, run:

```sh
# Install deps
make deps
# Install local package
make install-local
```

The program entrypoint is located in `secenv.__init__:main`.


## Testing

PyTest handles the different tests.
To perform all the tests, run:

```
make tests
```

Before submitting changes to `secenv`, please ensure all the tests pass.


## Git flow

The development flow of `secenv` is designed around branches.
Each branch should follow this nomenclature:

- Bug fixes: `fix/<bug-to-fix>`
- Features: `feature/<feature-to-add>`
- Chore (docs, unit tests, refactoring...): `chore/<thing-to-modify>`
- Tests: `test/<thing-to-test>`
  > The `test/.*` branches are not meant to be merged.

The pull requests must be named after the branch.
In example, if the branch is `feature/add-useful-thing`, name the PR: *Feature: add useful thing*.
The names of the PRs are used to determine the version bump, so name them carefully.

If the modified code causes breaking changes, the commit message **MUST** contain a line like this:

```
This is the commit message.

This is the commit body...

BREAKING CHANGE:
Explain what breaks, how, why.
Explain how to migrate to the new behavior and/or new configuration
```

> The parser will accept anything matching '^BREAK' in the commit message.

Everything starting from the line containing *BREAKING CHANGE* will be included in the Changelog.


## Development


### Adding a store

The stores are defined in the `secenv/stores` directory. They implement the `StoreInterface` defined in `__init__.py`.

The stores must implement all of the methods defined in the interface, otherwise the program will crash at some point.

It is a good practice to have a look at the other stores to understand how to deal with the parser, the arguments, and how to deal with the secrets themselves.

First, read the code of the `env` store to understand how to implement the different methods.
Then, read the code of the `vault` store to understand secrets' filtering using a key, and how to use arguments.
The `pass` store uses default arguments, read its code to understand how it works.

To summarize, here is the link between the constructor of a store, and its definition in the configuration file:

```py
# ./secenv/stores/mystore.py

class Store(StoreInterface):
    def __init__(self, name, infos):
        self.name = name
        self.url = super().get_from_config(
            name, "url", infos, default="https://vault.example.com"
        )
        self.token = super().get_from_config(name, "token", infos)
        ...
```

```yaml
stores:
  my_store_in_config:
    type: mystore
    token: S3CR3T_T0K3N
    url: https://vault.custom.domain.tld
    # `url` defaults to 'https://vault.example.com' if it's not provided
```

It is also possible to configure the parameters on the new store by using `SECENV_<store_name>_<parameter>`.
This behavior doesn't require more configuration than defining the store.


#### Caching retrieved secrets

A cache mechanism is available when retrieving the secrets.
It is enabled by adding the `@cached` decorator available in the `stores` module to the `Store.read_secret` function.

In example:

```py
from . import StoreInterface, cached

class Store(StoreInterface):
    @cached
    def read_secret(self, secret) -> str:
        ...
```

When a secret is retrieved, its result is stored in a map so when it is retrieved again, the request is not performed and the value is read from the map instead.


#### Default config value

The `StoreInterface.get_from_config` function permits to read a value from the config file, or from the environment directly.
This function takes an optional argument, `default`.

If the wanted value is in neither the config file, nor the environment, then the `default` value is returned if one is provided.
If there is no `default` value, then an exception is raised.


#### Key-value store inside a secret

If the secret can be a key-value store, a `--key` option can be added to the parser (see AWS and Vault stores as they implement this).
The new store must provide a `Store.filter(secret, key)` function.


## Adding an output format for contexts

The output is computed in the `./secenv/context.py` file.
A list of the available formats is defined at the beginning of the file.

To make a new format available, add an `if` statement in the `format_output` function.
The secrets are stored in the `context` parameter.

Here is the format of this parameter:

```py
context: Dict[str, Dict[str, str]]

context = {
    "my_secret" = {
        "value" = "my_value"
        "sensitive" = True
    }
}
```

The `context["my_secret"]["sensitive"]` option can be used to mask the output value.
It is used in the `github_actions` output format.

The `escape` function is available to escape the quotes and dollar signs.

During the formatting, the values must be appended to the `output` array, with one value per line.
At the end of the function, the output is modified so all the elements are joined using a new line.

Here is a full example of an output format:

```py
def format_output(context, format):
    output = []
    ...
    if format == "debug":
        for k, v in context.items():
            output.append(f"key = {k}, value (escaped) = {escape(v['value'])}")
    ...
```
