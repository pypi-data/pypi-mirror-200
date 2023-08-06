from typing.io import TextIO

from mimeo.exceptions import ResourceNotFound

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

from mimeo import resources as data


def get_resource(resource_name: str) -> TextIO:
    try:
        return pkg_resources.open_text(data, resource_name)
    except FileNotFoundError:
        raise ResourceNotFound(f"No such resource: [{resource_name}]")
