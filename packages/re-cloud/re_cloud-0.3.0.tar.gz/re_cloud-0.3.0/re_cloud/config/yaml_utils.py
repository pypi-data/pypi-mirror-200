import yaml

try:
    from yaml import CLoader as Loader, CSafeLoader as SafeLoader, CDumper as Dumper
except ImportError:
    from yaml import Loader, SafeLoader, Dumper  # type: ignore  # noqa: F401


def load_yaml_from_text(contents):
    try:
        return yaml.load(contents, Loader=SafeLoader)
    except (yaml.scanner.ScannerError, yaml.YAMLError) as e:
        error = str(e)

        raise ValueError(error)
