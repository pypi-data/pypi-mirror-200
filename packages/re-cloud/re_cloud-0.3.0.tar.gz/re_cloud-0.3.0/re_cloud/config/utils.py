import os
from typing import Dict, Any
from re_cloud.config.system import load_file_contents_as_string
from re_cloud.config.yaml_utils import load_yaml_from_text
from re_cloud.flags import RE_DATA_CONFIG_DIR
import click


def read_re_data_config(config_dir=None) -> Dict[str, Any]:
    """
    Parses the re_data config file and returns the details.
    """
    # We priortize the config_dir argument over the RE_DATA_CONFIG_DIR environment variable
    config_file = os.path.join(config_dir or RE_DATA_CONFIG_DIR, "re_data.yml")

    if not os.path.isfile(config_file):
        raise click.ClickException(
            "re_data config file not found at {}".format(config_file)
        )
    try:
        contents = load_file_contents_as_string(config_file, strip=False)
        yaml_content = load_yaml_from_text(contents)
        return yaml_content
    except Exception as e:
        msg = str(e)
        raise click.ClickException(msg)
