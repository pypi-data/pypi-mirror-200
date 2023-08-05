import os
from .utils import with_tmp_conf, write
import secenv


@with_tmp_conf
def test_format_dotenv(config):
    config_as_py = {"contexts": {"dev": {"vars": {"VAR": "value"}}}}
    write(config, config_as_py)

    secenv.load_config()
    ctx = secenv.gen_context("dev", [])
    output = secenv.context.format_output(ctx, "dotenv")
    assert output == "VAR='value'"


@with_tmp_conf
def test_format_shell(config):
    config_as_py = {"contexts": {"dev": {"vars": {"VAR": "value"}}}}
    write(config, config_as_py)

    secenv.load_config()
    ctx = secenv.gen_context("dev", [])
    output = secenv.context.format_output(ctx, "shell")
    assert output == "export VAR='value'"


@with_tmp_conf
def test_format_github_actions_masked(config):
    config_as_py = {"contexts": {"dev": {"vars": {"VAR": "value"}}}}
    write(config, config_as_py)

    secenv.load_config()
    ctx = secenv.gen_context("dev", [])
    output = secenv.context.format_output(ctx, "github_actions")
    assert output == "echo 'VAR=value' >> $GITHUB_ENV\necho '::add-mask::value'"


@with_tmp_conf
def test_format_github_actions_not_masked(config):
    config_as_txt = """
    stores:
      local:
        type: env
    contexts:
      dev:
        vars:
          VAR:
            store: local
            secret: _SECENV_GH_NM_VAR
            sensitive: false
    """
    config.write(config_as_txt)
    config.flush()

    os.environ["_SECENV_GH_NM_VAR"] = "value"
    secenv.load_config()
    stores = secenv.find_stores()
    ctx = secenv.gen_context("dev", stores)
    output = secenv.context.format_output(ctx, "github_actions")
    assert output == "echo 'VAR=value' >> $GITHUB_ENV"
