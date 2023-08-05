from .utils import with_tmp_conf, write, skip_unimplemented_test

import secenv
import pytest


@with_tmp_conf
def test_raw_variable(config):
    config_as_py = {
        "contexts": {
            "dev": {
                "vars": {
                    "VAR": "value",
                }
            }
        }
    }
    write(config, config_as_py)

    secenv.load_config()
    env = secenv.gen_context("dev", {})
    assert "VAR" in env and env["VAR"] == {"sensitive": True, "value": "value"}


@skip_unimplemented_test
@with_tmp_conf
def test_aws_assume_role(config):
    config_as_py = {
        "contexts": {
            "dev": {
                "aws_assume_role": {
                    "aws_access_key_id": "TODO",
                    "aws_secret_access_key": "TODO",
                    "role_arn": "TODO",
                }
            }
        }
    }
    write(config, config_as_py)

    ...


@with_tmp_conf
def test_null_context(config):
    config_as_txt = """
    contexts:
      dev:
    """
    config.write(config_as_txt)
    config.flush()

    secenv.load_config()
    with pytest.raises(SystemExit):
        secenv.gen_context("dev", {})


@with_tmp_conf
def test_empty_context(config):
    config_as_py = {"contexts": {"dev": {}}}
    write(config, config_as_py)

    secenv.load_config()
    env = secenv.gen_context("dev", {})
    assert env == {}


@with_tmp_conf
def test_extends(config):
    config_as_py = {
        "contexts": {
            "default": {"vars": {"VAR": "value"}},
            "dev": {"extends": ["default"]},
        }
    }
    write(config, config_as_py)

    secenv.load_config()
    env = secenv.gen_context("dev", {})
    assert "VAR" in env and env["VAR"] == {"value": "value", "sensitive": True}


@with_tmp_conf
def test_extends_and_overwrite(config):
    config_as_py = {
        "contexts": {
            "default": {"vars": {"VAR": "value"}},
            "dev": {"extends": ["default"], "vars": {"VAR": "dev-value"}},
        }
    }
    write(config, config_as_py)

    secenv.load_config()
    env = secenv.gen_context("dev", {})
    assert "VAR" in env and env["VAR"] == {"value": "dev-value", "sensitive": True}


@with_tmp_conf
def test_extends_multiple_times(config):
    config_as_py = {
        "contexts": {
            "ctx1": {"vars": {"VAR": "value1"}},
            "ctx2": {"vars": {"VAR": "value2"}},
            "ctx3": {"vars": {"VAR": "value3"}},
            "dev": {"extends": ["ctx1", "ctx2", "ctx3"]},
        }
    }
    write(config, config_as_py)

    secenv.load_config()
    env = secenv.gen_context("dev", {})
    assert "VAR" in env and env["VAR"] == {"sensitive": True, "value": "value3"}


@with_tmp_conf
def test_extends_multiple_times_and_overwrite(config):
    config_as_py = {
        "contexts": {
            "ctx1": {"vars": {"VAR": "value1"}},
            "ctx2": {"vars": {"VAR": "value2"}},
            "ctx3": {"vars": {"VAR": "value3"}},
            "dev": {"extends": ["ctx1", "ctx2", "ctx3"], "vars": {"VAR": "dev-value"}},
        }
    }
    write(config, config_as_py)

    secenv.load_config()
    env = secenv.gen_context("dev", {})
    assert "VAR" in env and env["VAR"] == {"value": "dev-value", "sensitive": True}
