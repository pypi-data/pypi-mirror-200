import json
import logging
import shutil
import sys
from glob import glob
from os import listdir, path, remove, rmdir
from pathlib import Path

import pytest

import mimeo.__main__ as MimeoCLI


@pytest.fixture(autouse=True)
def minimum_config():
    return {
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True
                    }
                }
            }
        ]
    }


@pytest.fixture(autouse=True)
def default_config():
    return {
        "output_format": "xml",
        "indent": 4,
        "xml_declaration": True,
        "output_details": {
            "direction": "file",
            "directory_path": "test_mimeo_cli-dir/output",
            "file_name": "output-file"
        },
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True
                    }
                }
            }
        ]
    }


@pytest.fixture(autouse=True)
def setup_and_teardown(default_config, minimum_config):
    # Setup
    Path("test_mimeo_cli-dir").mkdir(parents=True, exist_ok=True)
    with open("test_mimeo_cli-dir/default-config.json", "w") as file:
        json.dump(default_config, file)
    with open("test_mimeo_cli-dir/minimum-config.json", "w") as file:
        json.dump(minimum_config, file)

    yield

    # Teardown
    shutil.rmtree("test_mimeo_cli-dir")
    for filename in glob("mimeo-output/customized-output-file*"):
        remove(filename)
    if path.exists("mimeo-output") and not listdir("mimeo-output"):
        rmdir("mimeo-output")


def test_basic_use():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json"]

    assert not path.exists("test_mimeo_cli-dir/output")

    MimeoCLI.main()

    assert path.exists("test_mimeo_cli-dir/output")
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert path.exists(file_path)

        with open(file_path, "r") as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == '<SomeEntity>\n'
            assert file_content.readline() == '    <ChildNode1>1</ChildNode1>\n'
            assert file_content.readline() == '    <ChildNode2>value-2</ChildNode2>\n'
            assert file_content.readline() == '    <ChildNode3>true</ChildNode3>\n'
            assert file_content.readline() == '</SomeEntity>\n'


def test_custom_short_xml_declaration_false():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json", "-x", "false"]

    assert not path.exists("test_mimeo_cli-dir/output")

    MimeoCLI.main()

    assert path.exists("test_mimeo_cli-dir/output")
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert path.exists(file_path)

        with open(file_path, "r") as file_content:
            assert file_content.readline() == '<SomeEntity>\n'
            assert file_content.readline() == '    <ChildNode1>1</ChildNode1>\n'
            assert file_content.readline() == '    <ChildNode2>value-2</ChildNode2>\n'
            assert file_content.readline() == '    <ChildNode3>true</ChildNode3>\n'
            assert file_content.readline() == '</SomeEntity>\n'


def test_custom_short_xml_declaration_true():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json", "-x", "true"]

    assert not path.exists("test_mimeo_cli-dir/output")

    MimeoCLI.main()

    assert path.exists("test_mimeo_cli-dir/output")
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert path.exists(file_path)

        with open(file_path, "r") as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == '<SomeEntity>\n'
            assert file_content.readline() == '    <ChildNode1>1</ChildNode1>\n'
            assert file_content.readline() == '    <ChildNode2>value-2</ChildNode2>\n'
            assert file_content.readline() == '    <ChildNode3>true</ChildNode3>\n'
            assert file_content.readline() == '</SomeEntity>\n'


def test_custom_long_xml_declaration_false():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json", "--xml-declaration", "false"]

    assert not path.exists("test_mimeo_cli-dir/output")

    MimeoCLI.main()

    assert path.exists("test_mimeo_cli-dir/output")
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert path.exists(file_path)

        with open(file_path, "r") as file_content:
            assert file_content.readline() == '<SomeEntity>\n'
            assert file_content.readline() == '    <ChildNode1>1</ChildNode1>\n'
            assert file_content.readline() == '    <ChildNode2>value-2</ChildNode2>\n'
            assert file_content.readline() == '    <ChildNode3>true</ChildNode3>\n'
            assert file_content.readline() == '</SomeEntity>\n'


def test_custom_long_xml_declaration_true():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json", "--xml-declaration", "true"]

    assert not path.exists("test_mimeo_cli-dir/output")

    MimeoCLI.main()

    assert path.exists("test_mimeo_cli-dir/output")
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert path.exists(file_path)

        with open(file_path, "r") as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == '<SomeEntity>\n'
            assert file_content.readline() == '    <ChildNode1>1</ChildNode1>\n'
            assert file_content.readline() == '    <ChildNode2>value-2</ChildNode2>\n'
            assert file_content.readline() == '    <ChildNode3>true</ChildNode3>\n'
            assert file_content.readline() == '</SomeEntity>\n'


def test_custom_short_indent_non_zero():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json", "-i", "2"]

    assert not path.exists("test_mimeo_cli-dir/output")

    MimeoCLI.main()

    assert path.exists("test_mimeo_cli-dir/output")
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert path.exists(file_path)

        with open(file_path, "r") as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == '<SomeEntity>\n'
            assert file_content.readline() == '  <ChildNode1>1</ChildNode1>\n'
            assert file_content.readline() == '  <ChildNode2>value-2</ChildNode2>\n'
            assert file_content.readline() == '  <ChildNode3>true</ChildNode3>\n'
            assert file_content.readline() == '</SomeEntity>\n'


def test_custom_short_indent_zero():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json", "-i", "0"]

    assert not path.exists("test_mimeo_cli-dir/output")

    MimeoCLI.main()

    assert path.exists("test_mimeo_cli-dir/output")
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert path.exists(file_path)

        with open(file_path, "r") as file_content:
            assert file_content.readline() == "<?xml version='1.0' encoding='utf-8'?>\n"
            assert file_content.readline() == '<SomeEntity>' \
                                              '<ChildNode1>1</ChildNode1>' \
                                              '<ChildNode2>value-2</ChildNode2>' \
                                              '<ChildNode3>true</ChildNode3>' \
                                              '</SomeEntity>'


def test_custom_long_indent_non_zero():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json", "--indent", "2"]

    assert not path.exists("test_mimeo_cli-dir/output")

    MimeoCLI.main()

    assert path.exists("test_mimeo_cli-dir/output")
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert path.exists(file_path)

        with open(file_path, "r") as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == '<SomeEntity>\n'
            assert file_content.readline() == '  <ChildNode1>1</ChildNode1>\n'
            assert file_content.readline() == '  <ChildNode2>value-2</ChildNode2>\n'
            assert file_content.readline() == '  <ChildNode3>true</ChildNode3>\n'
            assert file_content.readline() == '</SomeEntity>\n'


def test_custom_long_indent_zero():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json", "--indent", "0"]

    assert not path.exists("test_mimeo_cli-dir/output")

    MimeoCLI.main()

    assert path.exists("test_mimeo_cli-dir/output")
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert path.exists(file_path)

        with open(file_path, "r") as file_content:
            assert file_content.readline() == "<?xml version='1.0' encoding='utf-8'?>\n"
            assert file_content.readline() == '<SomeEntity>' \
                                              '<ChildNode1>1</ChildNode1>' \
                                              '<ChildNode2>value-2</ChildNode2>' \
                                              '<ChildNode3>true</ChildNode3>' \
                                              '</SomeEntity>'


def test_custom_short_output_direction():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json", "-o", "stdout"]

    assert not path.exists("test_mimeo_cli-dir/output")

    MimeoCLI.main()

    assert not path.exists("test_mimeo_cli-dir/output")


def test_custom_long_output_direction():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json", "--output", "stdout"]

    assert not path.exists("test_mimeo_cli-dir/output")

    MimeoCLI.main()

    assert not path.exists("test_mimeo_cli-dir/output")


def test_custom_output_direction_does_not_throw_error_when_output_details_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json", "-o", "stdout"]

    try:
        MimeoCLI.main()
    except KeyError:
        assert False


def test_custom_short_output_directory_path():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json", "-d", "test_mimeo_cli-dir/customized-output"]

    assert not path.exists("test_mimeo_cli-dir/output")
    assert not path.exists("test_mimeo_cli-dir/customized-output")

    MimeoCLI.main()

    assert not path.exists("test_mimeo_cli-dir/output")
    assert path.exists("test_mimeo_cli-dir/customized-output")
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/customized-output/output-file-{i}.xml"
        assert path.exists(file_path)

        with open(file_path, "r") as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == '<SomeEntity>\n'
            assert file_content.readline() == '    <ChildNode1>1</ChildNode1>\n'
            assert file_content.readline() == '    <ChildNode2>value-2</ChildNode2>\n'
            assert file_content.readline() == '    <ChildNode3>true</ChildNode3>\n'
            assert file_content.readline() == '</SomeEntity>\n'


def test_custom_long_output_directory_path():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json", "--directory", "test_mimeo_cli-dir/customized-output"]

    assert not path.exists("test_mimeo_cli-dir/output")
    assert not path.exists("test_mimeo_cli-dir/customized-output")

    MimeoCLI.main()

    assert not path.exists("test_mimeo_cli-dir/output")
    assert path.exists("test_mimeo_cli-dir/customized-output")
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/customized-output/output-file-{i}.xml"
        assert path.exists(file_path)

        with open(file_path, "r") as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == '<SomeEntity>\n'
            assert file_content.readline() == '    <ChildNode1>1</ChildNode1>\n'
            assert file_content.readline() == '    <ChildNode2>value-2</ChildNode2>\n'
            assert file_content.readline() == '    <ChildNode3>true</ChildNode3>\n'
            assert file_content.readline() == '</SomeEntity>\n'


def test_custom_output_directory_path_does_not_throw_error_when_output_details_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json", "-d", "test_mimeo_cli-dir/customized-output"]

    try:
        MimeoCLI.main()
    except KeyError:
        assert False


def test_custom_short_output_file_name():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json", "-f", "customized-output-file"]

    assert not path.exists("test_mimeo_cli-dir/output")

    MimeoCLI.main()

    assert path.exists("test_mimeo_cli-dir/output")
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/customized-output-file-{i}.xml"
        assert path.exists(file_path)
        assert not path.exists(f"test_mimeo_cli-dir/output/output-file-{i}.xml")

        with open(file_path, "r") as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == '<SomeEntity>\n'
            assert file_content.readline() == '    <ChildNode1>1</ChildNode1>\n'
            assert file_content.readline() == '    <ChildNode2>value-2</ChildNode2>\n'
            assert file_content.readline() == '    <ChildNode3>true</ChildNode3>\n'
            assert file_content.readline() == '</SomeEntity>\n'


def test_custom_long_output_file_name():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json", "--file", "customized-output-file"]

    assert not path.exists("test_mimeo_cli-dir/output")

    MimeoCLI.main()

    assert path.exists("test_mimeo_cli-dir/output")
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/customized-output-file-{i}.xml"
        assert path.exists(file_path)
        assert not path.exists(f"test_mimeo_cli-dir/output/output-file-{i}.xml")

        with open(file_path, "r") as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == '<SomeEntity>\n'
            assert file_content.readline() == '    <ChildNode1>1</ChildNode1>\n'
            assert file_content.readline() == '    <ChildNode2>value-2</ChildNode2>\n'
            assert file_content.readline() == '    <ChildNode3>true</ChildNode3>\n'
            assert file_content.readline() == '</SomeEntity>\n'


def test_custom_output_file_name_does_not_throw_error_when_output_details_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json", "-f", "customized-output-file"]

    try:
        MimeoCLI.main()
    except KeyError:
        assert False


def test_logging_mode_default():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json"]
    logger = logging.getLogger("mimeo")

    MimeoCLI.main()

    assert logger.getEffectiveLevel() == logging.INFO


def test_logging_mode_silent():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json", "--silent"]
    logger = logging.getLogger("mimeo")

    MimeoCLI.main()

    assert logger.getEffectiveLevel() == logging.WARNING


def test_logging_mode_debug():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json", "--debug"]
    logger = logging.getLogger("mimeo")

    MimeoCLI.main()

    assert logger.getEffectiveLevel() == logging.DEBUG


def test_logging_mode_fine():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json", "--fine"]
    logger = logging.getLogger("mimeo")

    MimeoCLI.main()

    assert logger.getEffectiveLevel() == logging.FINE
