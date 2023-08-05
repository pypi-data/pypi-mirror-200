import boto3
import json
import os
from . import EnvPrefix, StoreInterface, cached, ask_secret, SecretNotFoundError


# This dictionary is used to store the ARN of a secret given its name.
_secrets_arns = {}


class Store(StoreInterface):
    def __init__(self, name, infos):
        self.name = name

        region = super().get_from_config(name, "region", infos)
        key_id = super().get_from_config(name, "access_key_id", infos)
        secret_access_key = super().get_from_config(name, "secret_access_key", infos)

        client = boto3.client(
            "secretsmanager",
            region_name=region,
            aws_access_key_id=key_id,
            aws_secret_access_key=secret_access_key,
        )

        if "assume_role" in infos or f"{EnvPrefix}_{name}_assume_role" in os.environ:
            session = boto3.Session(
                aws_access_key_id=key_id,
                aws_secret_access_key=secret_access_key,
            )
            sts_client = session.client("sts")

            arn = super().get_from_config(name, "assume_role", infos)
            role = sts_client.assume_role(RoleArn=arn, RoleSessionName="SecEnvSession")
            creds = role["Credentials"]
            key_id = creds["AccessKeyId"]
            secret_access_key = creds["SecretAccessKey"]
            token = creds["SessionToken"]
            client = boto3.client(
                "secretsmanager",
                region_name=region,
                aws_access_key_id=key_id,
                aws_secret_access_key=secret_access_key,
                aws_session_token=token,
            )

        self.client = client

    def gen_parser(self, parser):
        parser.add_argument("secret")
        parser.add_argument("--key")

    @cached
    def read_secret(self, secret) -> str:
        search_result = self.client.list_secrets(
            MaxResults=2,
            Filters=[
                {"Key": "name", "Values": [secret]},
            ],
            SortOrder="asc",
        )["SecretList"]

        while search_result and search_result[-1]["Name"] != secret:
            search_result.pop()

        if len(search_result) == 0:
            raise SecretNotFoundError(self.name, secret)

        value = self.client.get_secret_value(
            SecretId=search_result[-1]["ARN"],
        )

        _secrets_arns[secret] = value["ARN"]
        return value["SecretString"]

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

        if secret in _secrets_arns:
            # Update secret
            arn = _secrets_arns[secret]

            self.client.update_secret(
                SecretId=arn,
                SecretString=secret_value,
            )
        else:
            # Create secret
            self.client.create_secret(
                Name=secret,
                SecretString=secret_value,
            )
