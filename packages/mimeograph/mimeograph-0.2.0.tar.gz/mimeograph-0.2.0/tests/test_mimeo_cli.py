import json
import logging
import shutil
import sys
from base64 import b64encode
from glob import glob
from http import HTTPStatus
from os import listdir, path, remove, rmdir
from pathlib import Path

import pytest
import responses
from responses import matchers

import mimeo.__main__ as MimeoCLI
from mimeo.exceptions import (EnvironmentNotFound, EnvironmentsFileNotFound,
                              MissingRequiredProperty)


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
def http_config():
    return {
        "output_details": {
            "direction": "http",
            "method": "POST",
            "protocol": "http",
            "host": "localhost",
            "port": 8080,
            "endpoint": "/document",
            "auth": "digest",
            "username": "admin",
            "password": "admin"
        },
        "_templates_": [
            {
                "count": 1,
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
def http_default_envs():
    return {
        "default": {
            "protocol": "https",
            "host": "11.111.11.111",
            "port": 8000,
            "auth": "basic",
            "username": "custom-username",
            "password": "custom-password"
        }
    }


@pytest.fixture(autouse=True)
def http_custom_envs():
    return {
        "custom": {
            "protocol": "https",
            "host": "11.111.11.111",
            "port": 8000,
            "auth": "basic",
            "username": "custom-username",
            "password": "custom-password"
        }
    }


@pytest.fixture(autouse=True)
def setup_and_teardown(minimum_config, default_config, http_config, http_default_envs, http_custom_envs):
    # Setup
    Path("test_mimeo_cli-dir").mkdir(parents=True, exist_ok=True)
    with open("test_mimeo_cli-dir/minimum-config.json", "w") as file:
        json.dump(minimum_config, file)
    with open("test_mimeo_cli-dir/default-config.json", "w") as file:
        json.dump(default_config, file)
    with open("test_mimeo_cli-dir/http-config.json", "w") as file:
        json.dump(http_config, file)
    with open("mimeo.envs.json", "w") as file:
        json.dump(http_default_envs, file)
    with open("custom-mimeo-envs-file.json", "w") as file:
        json.dump(http_custom_envs, file)

    yield

    # Teardown
    shutil.rmtree("test_mimeo_cli-dir")
    remove("mimeo.envs.json")
    remove("custom-mimeo-envs-file.json")
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


def test_custom_output_direction_does_not_throw_key_error_when_output_details_does_not_exist():
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


def test_custom_output_directory_path_does_not_throw_key_error_when_output_details_does_not_exist():
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


def test_custom_output_file_name_does_not_throw_key_error_when_output_details_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json", "-f", "customized-output-file"]

    try:
        MimeoCLI.main()
    except KeyError:
        assert False


@responses.activate
def test_custom_short_output_http_host():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json", "-H", "198.168.1.1"]

    responses.add(responses.POST, "http://198.168.1.1:8080/document", json={"success": True}, status=HTTPStatus.OK)
    MimeoCLI.main()
    # would throw a ConnectionError when any request call doesn't match registered mocks


@responses.activate
def test_custom_long_output_http_host():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json", "--http-host", "198.168.1.1"]

    responses.add(responses.POST, "http://198.168.1.1:8080/document", json={"success": True}, status=HTTPStatus.OK)
    MimeoCLI.main()
    # would throw a ConnectionError when any request call doesn't match registered mocks


def test_custom_output_http_host_does_not_throw_key_error_when_output_details_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json", "-o", "http", "-H", "198.168.1.1"]

    try:
        MimeoCLI.main()
    except MissingRequiredProperty:
        assert True
    except KeyError:
        assert False


@responses.activate
def test_custom_short_output_http_port():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json", "-p", "8081"]

    responses.add(responses.POST, "http://localhost:8081/document", json={"success": True}, status=HTTPStatus.OK)
    MimeoCLI.main()
    # would throw a ConnectionError when any request call doesn't match registered mocks


@responses.activate
def test_custom_long_output_http_port():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json", "--http-port", "8081"]

    responses.add(responses.POST, "http://localhost:8081/document", json={"success": True}, status=HTTPStatus.OK)
    MimeoCLI.main()
    # would throw a ConnectionError when any request call doesn't match registered mocks


def test_custom_output_http_port_does_not_throw_key_error_when_output_details_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json", "-o", "http", "-p", "8081"]

    try:
        MimeoCLI.main()
    except MissingRequiredProperty:
        assert True
    except KeyError:
        assert False


@responses.activate
def test_custom_short_output_http_endpoint():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json", "-E", "/v2/document"]

    responses.add(responses.POST, "http://localhost:8080/v2/document", json={"success": True}, status=HTTPStatus.OK)
    MimeoCLI.main()
    # would throw a ConnectionError when any request call doesn't match registered mocks


@responses.activate
def test_custom_long_output_http_endpoint():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json", "--http-endpoint", "/v2/document"]

    responses.add(responses.POST, "http://localhost:8080/v2/document", json={"success": True}, status=HTTPStatus.OK)
    MimeoCLI.main()
    # would throw a ConnectionError when any request call doesn't match registered mocks


def test_custom_output_http_endpoint_does_not_throw_key_error_when_output_details_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json", "-o", "http", "-E", "/v2/document"]

    try:
        MimeoCLI.main()
    except MissingRequiredProperty:
        assert True
    except KeyError:
        assert False


@responses.activate
def test_custom_short_output_http_username():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json", "--http-auth", "basic", "-U", "custom-user"]

    responses.add(
        responses.POST,
        "http://localhost:8080/document",
        json={"success": True},
        status=HTTPStatus.OK,
        match=[matchers.header_matcher({'Authorization': _generate_authorization("custom-user", "admin")})]
    )
    MimeoCLI.main()
    # would throw a ConnectionError when any request call doesn't match registered mocks


@responses.activate
def test_custom_long_output_http_username():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json", "--http-auth", "basic", "--http-user", "custom-user"]

    responses.add(
        responses.POST,
        "http://localhost:8080/document",
        json={"success": True},
        status=HTTPStatus.OK,
        match=[matchers.header_matcher({'Authorization': _generate_authorization("custom-user", "admin")})]
    )
    MimeoCLI.main()
    # would throw a ConnectionError when any request call doesn't match registered mocks


def test_custom_output_http_username_does_not_throw_key_error_when_output_details_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json", "-o", "http", "-U", "custom-user"]

    try:
        MimeoCLI.main()
    except MissingRequiredProperty:
        assert True
    except KeyError:
        assert False


@responses.activate
def test_custom_short_output_http_password():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json", "--http-auth", "basic", "-P", "custom-password"]

    responses.add(
        responses.POST,
        "http://localhost:8080/document",
        json={"success": True},
        status=HTTPStatus.OK,
        match=[matchers.header_matcher({'Authorization': _generate_authorization("admin", "custom-password")})]
    )
    MimeoCLI.main()
    # would throw a ConnectionError when any request call doesn't match registered mocks


@responses.activate
def test_custom_long_output_http_password():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "--http-auth", "basic",
                "--http-password", "custom-password"]

    responses.add(
        responses.POST,
        "http://localhost:8080/document",
        json={"success": True},
        status=HTTPStatus.OK,
        match=[matchers.header_matcher({'Authorization': _generate_authorization("admin", "custom-password")})]
    )
    MimeoCLI.main()
    # would throw a ConnectionError when any request call doesn't match registered mocks


def test_custom_output_http_password_does_not_throw_key_error_when_output_details_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json", "-o", "http", "-P", "custom-password"]

    try:
        MimeoCLI.main()
    except MissingRequiredProperty:
        assert True
    except KeyError:
        assert False


@responses.activate
def test_custom_long_output_http_method():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json", "--http-method", "PUT"]

    responses.add(responses.PUT, "http://localhost:8080/document", json={"success": True}, status=HTTPStatus.OK)
    MimeoCLI.main()
    # would throw a ConnectionError when any request call doesn't match registered mocks


def test_custom_output_http_method_does_not_throw_key_error_when_output_details_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json", "-o", "http", "--http-method", "PUT"]

    try:
        MimeoCLI.main()
    except MissingRequiredProperty:
        assert True
    except KeyError:
        assert False


@responses.activate
def test_custom_long_output_http_protocol():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json", "--http-protocol", "https"]

    responses.add(responses.POST, "https://localhost:8080/document", json={"success": True}, status=HTTPStatus.OK)
    MimeoCLI.main()
    # would throw a ConnectionError when any request call doesn't match registered mocks


def test_custom_output_http_protocol_does_not_throw_key_error_when_output_details_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json", "-o", "http", "--http-protocol", "https"]

    try:
        MimeoCLI.main()
    except MissingRequiredProperty:
        assert True
    except KeyError:
        assert False


@responses.activate
def test_custom_long_output_http_auth():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json", "--http-auth", "basic"]

    responses.add(
        responses.POST,
        "http://localhost:8080/document",
        json={"success": True},
        status=HTTPStatus.OK,
        match=[matchers.header_matcher({'Authorization': _generate_authorization("admin", "admin")})]
    )
    MimeoCLI.main()
    # would throw a ConnectionError when any request call doesn't match registered mocks


def test_custom_output_http_auth_does_not_throw_key_error_when_output_details_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json", "-o", "http", "--http-auth", "basic"]

    try:
        MimeoCLI.main()
    except MissingRequiredProperty:
        assert True
    except KeyError:
        assert False


@responses.activate
def test_custom_short_env():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json", "-e", "default"]

    responses.add(
        responses.POST,
        "https://11.111.11.111:8000/document",
        json={"success": True},
        status=HTTPStatus.OK,
        match=[matchers.header_matcher({'Authorization': _generate_authorization("custom-username", "custom-password")})]
    )
    MimeoCLI.main()
    # would throw a ConnectionError when any request call doesn't match registered mocks


@responses.activate
def test_custom_long_env():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json", "--http-env", "default"]

    responses.add(
        responses.POST,
        "https://11.111.11.111:8000/document",
        json={"success": True},
        status=HTTPStatus.OK,
        match=[matchers.header_matcher({'Authorization': _generate_authorization("custom-username", "custom-password")})]
    )
    MimeoCLI.main()
    # would throw a ConnectionError when any request call doesn't match registered mocks


@responses.activate
def test_custom_env_file():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "--http-envs-file", "custom-mimeo-envs-file.json",
                "-e", "custom"]

    responses.add(
        responses.POST,
        "https://11.111.11.111:8000/document",
        json={"success": True},
        status=HTTPStatus.OK,
        match=[matchers.header_matcher({'Authorization': _generate_authorization("custom-username", "custom-password")})]
    )
    MimeoCLI.main()
    # would throw a ConnectionError when any request call doesn't match registered mocks


def test_custom_env_file_does_throw_error_when_file_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "--http-envs-file", "non-existing-environments-file.json",
                "-e", "custom"]

    with pytest.raises(EnvironmentsFileNotFound) as err:
        MimeoCLI.main()

    assert err.value.args[0] == "Environments file not found [non-existing-environments-file.json]"


def test_custom_env_does_not_throw_key_error_when_output_details_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json", "-o", "http", "-e", "default"]

    try:
        MimeoCLI.main()
    except MissingRequiredProperty:
        assert True
    except KeyError:
        assert False


def test_custom_env_does_throw_error_when_environment_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json", "-o", "http", "-e", "non-existing"]

    with pytest.raises(EnvironmentNotFound) as err:
        MimeoCLI.main()

    assert err.value.args[0] == "No such env [non-existing] in environments file [mimeo.envs.json]"


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


def _generate_authorization(username: str, password: str):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'
