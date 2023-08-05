from .utils import write, with_tmp_conf

import secenv


@with_tmp_conf
def test_no_context(config):
    config_as_py = {"contexts": {}}
    write(config, config_as_py)

    secenv.load_config()
    ctx = secenv.list_contexts()
    assert ctx == ""


@with_tmp_conf
def test_multiple_context(config):
    config_as_py = {"contexts": {"dev": {}, "prod": {}}}
    write(config, config_as_py)

    secenv.load_config()
    ctx = secenv.list_contexts()
    assert ctx == "dev\nprod"
