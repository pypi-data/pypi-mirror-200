import pytest

from mimeo import utils
from mimeo.exceptions import ResourceNotFound


def test_get_resource_existing():
    with utils.get_resource("logging.yaml") as resource:
        assert resource.name.endswith("resources/logging.yaml")


def test_get_resource_non_existing():
    with pytest.raises(ResourceNotFound) as err:
        utils.get_resource("non-existing-file.yaml")

    assert err.value.args[0] == "No such resource: [non-existing-file.yaml]"
