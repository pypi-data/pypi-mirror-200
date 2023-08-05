from .utils import with_tmp_dir, with_tmp_conf

import secenv


@with_tmp_dir
def test_no_config():
    secenv.load_config()
    assert secenv.no_config_available


@with_tmp_conf
def test_empty_config(config):
    config.flush()
    secenv.load_config()
    assert secenv.no_config_available
