import os
import base64
import json
import pytest
import secenv
import unittest.mock as mock
from moto import mock_secretsmanager

from .utils import with_tmp_conf, skip_unimplemented_test, write

# Secrets not found
from azure.core.exceptions import ResourceNotFoundError as AzureSecretNotFoundError
from google.api_core.exceptions import NotFound as GCPSecretNotFoundError
from hvac.exceptions import InvalidPath as VaultSecretNotFoundError


Object = lambda **kwargs: type("Object", (), kwargs)


@with_tmp_conf
@mock.patch("google.cloud.secretmanager.SecretManagerServiceClient", return_value=())
def test_store_extend(config, _):
    config_as_py = {
        "stores": {
            "store1": {
                "type": "gcp",
                "project_id": "my-project-id",
            },
            "store2": {"extends": "store1"},
        }
    }
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()

    # Asserting only for one store type, and for the shared values
    # for the other stores, the result is the same.
    assert stores["store1"].__class__ == stores["store2"].__class__
    assert stores["store1"].project_id == stores["store2"].project_id  # type: ignore
    assert stores["store1"]._creds == stores["store2"]._creds  # type: ignore


@with_tmp_conf
def test_store_extend_unexistent(config):
    config_as_py = {"stores": {"store": {"extends": "not_existing"}}}
    write(config, config_as_py)

    secenv.load_config()
    with pytest.raises(SystemExit):
        secenv.find_stores()


@with_tmp_conf
@mock.patch(
    "azure.keyvault.secrets.SecretClient.get_secret",
    return_value=Object(value="AzureSecretValue"),
)
def test_store_azure_secret_exists(config, _):
    config_as_py = {"stores": {"azure": {"type": "azure", "key_vault": "vault"}}}
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    secret = secenv.read_secret(stores["azure"], {"secret": "AzureSecretName"})
    assert secret == "AzureSecretValue"


@with_tmp_conf
@mock.patch(
    "azure.keyvault.secrets.SecretClient.get_secret",
    side_effect=AzureSecretNotFoundError(),
)
def test_store_azure_secret_not_exists(config, _):
    config_as_py = {"stores": {"azure": {"type": "azure", "key_vault": "vault"}}}
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    with pytest.raises(Exception):
        secenv.read_secret(stores["azure"], {"secret": "AzureSecretNameNotExist"})


@with_tmp_conf
@mock_secretsmanager()
def test_store_aws_secret_exists(config):
    # Create fake secret
    import boto3

    client = boto3.client("secretsmanager", region_name="eu-west-3")
    client.create_secret(Name="AWSSecretName", SecretString="AWSSecretValue")

    # And perform test
    config_as_py = {
        "stores": {
            "aws": {
                "type": "aws",
                "region": "eu-west-3",
                "access_key_id": "access_key_id",
                "secret_access_key": "secret_access_key",
            }
        }
    }
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    secret = secenv.read_secret(stores["aws"], {"secret": "AWSSecretName"})
    assert secret == "AWSSecretValue"


@with_tmp_conf
@mock_secretsmanager()
def test_store_aws_secrets_with_same_prefix(config):
    # Create fake secrets
    import boto3

    client = boto3.client("secretsmanager", region_name="eu-west-3")
    client.create_secret(Name="AWSSecretName", SecretString="AWSSecretValue")
    client.create_secret(Name="AWSSecretNameSuffix", SecretString="NotThisOne")
    client.create_secret(Name="PrefixAWSSecretName", SecretString="NotThisOne")

    # And perform test
    config_as_py = {
        "stores": {
            "aws": {
                "type": "aws",
                "region": "eu-west-3",
                "access_key_id": "access_key_id",
                "secret_access_key": "secret_access_key",
            }
        }
    }
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    secret = secenv.read_secret(stores["aws"], {"secret": "AWSSecretName"})
    assert secret == "AWSSecretValue"


@with_tmp_conf
@mock_secretsmanager()
def test_store_aws_secret_not_exists(config):
    config_as_py = {
        "stores": {
            "aws": {
                "type": "aws",
                "region": "eu-west-3",
                "access_key_id": "access_key_id",
                "secret_access_key": "secret_access_key",
            }
        }
    }
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    with pytest.raises(Exception):
        secenv.read_secret(stores["aws"], {"secret": "AWSSecretNameNotExist"})


@with_tmp_conf
@mock.patch(
    "subprocess.run", return_value=Object(stdout=b"BitwardenSecretValue", returncode=0)
)
def test_store_bitwarden_secret_exists(config, _):
    config_as_py = {"stores": {"bitwarden": {"type": "bitwarden"}}}
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    secret = secenv.read_secret(stores["bitwarden"], {"secret": "BitwardenSecretName"})
    assert secret == "BitwardenSecretValue"


@with_tmp_conf
@mock.patch("subprocess.run", return_value=Object(stderr=b"NotFound", returncode=1))
def test_store_bitwarden_secret_not_exists(config, _):
    config_as_py = {"stores": {"bitwarden": {"type": "bitwarden"}}}
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    with pytest.raises(Exception):
        secenv.read_secret(
            stores["bitwarden"], {"secret": "BitwardenSecretNameNotExist"}
        )


@with_tmp_conf
def test_store_env_secret_exists(config):
    config_as_py = {"stores": {"local": {"type": "env"}}}
    write(config, config_as_py)

    os.environ["VAR"] = "value"

    secenv.load_config()
    stores = secenv.find_stores()
    secret = secenv.read_secret(stores["local"], {"secret": "VAR"})
    assert secret == "value"


@with_tmp_conf
def test_store_env_secret_not_exists(config):
    config_as_py = {"stores": {"local": {"type": "env"}}}
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    with pytest.raises(Exception):
        secenv.read_secret(stores["local"], {"secret": "NEVER_GONNA_GIVE_YOU_UP"})


@with_tmp_conf
@mock.patch("passpy.Store", return_value=Object(get_key=lambda _: "PassSecretValue"))
def test_store_pass_secret_exists(config, _):
    config_as_py = {"stores": {"pass": {"type": "pass"}}}
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    secret = secenv.read_secret(stores["pass"], {"secret": "PassSecretName"})
    assert secret == "PassSecretValue"


@with_tmp_conf
@mock.patch("passpy.Store", return_value=Object(get_key=lambda _: None))
def test_store_pass_secret_not_exists(config, _):
    config_as_py = {"stores": {"pass": {"type": "pass"}}}
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    with pytest.raises(Exception):
        secenv.read_secret(stores["pass"], {"secret": "PassSecretNameNotExist"})


@with_tmp_conf
@mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    return_value=Object(
        access_secret_version=lambda **s: Object(payload=Object(data=b"GCPSecretValue"))
        if s["request"]["name"] == "projects/p/secrets/GCPSecretName/versions/latest"
        else None
    ),
)
def test_store_gcp_secret_exists(config, _):
    config_as_py = {"stores": {"gcp": {"type": "gcp", "project_id": "p"}}}
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    secret = secenv.read_secret(stores["gcp"], {"secret": "GCPSecretName"})
    assert secret == "GCPSecretValue"


@with_tmp_conf
@mock.patch(
    "google.cloud.secretmanager.SecretManagerServiceClient",
    return_value=Object(
        access_secret_version=lambda _: Object(
            side_effect=GCPSecretNotFoundError("secret")
        )
    ),
)
def test_store_gcp_secret_not_exists(config, _):
    config_as_py = {"stores": {"gcp": {"type": "gcp", "project_id": "pnf"}}}
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    with pytest.raises(Exception):
        secenv.read_secret(stores["gcp"], {"secret": "GCPSecretNameNotFound"})


@with_tmp_conf
@mock.patch(
    "requests.get",
    return_value=Object(
        text=json.dumps({"data": base64.b64encode(b"SWSecretValue").decode(), "id": 1})
    ),
)
def test_store_scaleway_secret_exists(config, _):
    config_as_py = {
        "stores": {
            "scaleway": {
                "type": "scaleway",
                "region": "r",
                "project_id": "p",
                "token": "t",
            }
        }
    }
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    secret = secenv.read_secret(stores["scaleway"], {"secret": "SWSecretName"})
    assert secret == "SWSecretValue"


@with_tmp_conf
@mock.patch(
    "requests.get",
    return_value=Object(text=json.dumps({"type": "not_found", "id": 42})),
)
def test_store_scaleway_secret_not_exists(config, _):
    config_as_py = {
        "stores": {
            "scaleway": {
                "type": "scaleway",
                "region": "r",
                "project_id": "p",
                "token": "t",
            }
        }
    }
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    with pytest.raises(Exception):
        secenv.read_secret(stores["scaleway"], {"secret": "SWSecretNameNotFound"})


@with_tmp_conf
@mock.patch(
    "hvac.Client",
    return_value=Object(
        secrets=Object(kv=Object(read_secret_version=lambda **_: "VaultSecretValue"))
    ),
)
def test_store_vault_secret_exists(config, _):
    config_as_py = {"stores": {"vault": {"type": "vault", "url": "u", "token": "t"}}}
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    secret = secenv.read_secret(stores["vault"], {"secret": "VaultSecretName"})
    assert secret == "VaultSecretValue"


@with_tmp_conf
@mock.patch(
    "hvac.Client",
    return_value=Object(
        secrets=Object(
            kv=Object(
                # Python doesn't accept this: `lambda _: raise Exception`
                # so let's make some really pythonic stuff
                read_secret_version=lambda **_: (_ for _ in ()).throw(
                    VaultSecretNotFoundError
                )
            )
        )
    ),
)
def test_store_vault_secret_not_exists(config, _):
    config_as_py = {"stores": {"vault": {"type": "vault", "url": "u", "token": "t"}}}
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    with pytest.raises(Exception):
        secenv.read_secret(stores["scaleway"], {"secret": "VaultSecretNameNotFound"})
