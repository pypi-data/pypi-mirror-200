from typing import Any, Dict, Optional
import yaml
import os
from re_cloud.constants import ARTEFACTS
import click

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader


def get_project_root(kwargs):
    return (
        os.getcwd()
        if not kwargs.get("project_dir")
        else os.path.abspath(kwargs["project_dir"])
    )


def safe_load(content) -> Optional[Dict[str, Any]]:
    return yaml.load(content, Loader=SafeLoader)


def get_all_files_in_dir(upload_path):
    files_to_exclude = {".DS_Store"}
    file_paths = []
    for dirpath, _, filenames in os.walk(upload_path):
        relative_path = dirpath.replace(f"{upload_path}", "")
        relative_file_names = [
            os.path.join(relative_path, file_name)
            for file_name in filenames
            if file_name not in files_to_exclude
        ]
        file_paths.extend(relative_file_names)

    return file_paths


def get_files_by_type(upload_path, upload_type):
    file_paths = get_all_files_in_dir(upload_path)
    for artefact in ARTEFACTS[upload_type]:
        if artefact not in file_paths:
            raise click.ClickException(
                "No expected file {} found in {}".format(artefact, upload_path)
            )

    return ARTEFACTS[upload_type]
