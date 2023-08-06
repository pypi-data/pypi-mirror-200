import re

from mimeo.exceptions import (IncorrectMimeoConfig, IncorrectMimeoModel,
                              IncorrectMimeoTemplate, InvalidIndent,
                              InvalidVars, MissingRequiredProperty,
                              UnsupportedAuthMethod,
                              UnsupportedOutputDirection,
                              UnsupportedOutputFormat,
                              UnsupportedRequestMethod)
from mimeo.logging import setup_logging

setup_logging()


class MimeoDTO:

    def __init__(self, source: dict):
        self.__source = source

    def __str__(self):
        return str(self.__source)


class MimeoConfig(MimeoDTO):

    OUTPUT_FORMAT_KEY = "output_format"
    OUTPUT_DETAILS_KEY = "output_details"
    OUTPUT_DETAILS_DIRECTION_KEY = "direction"
    OUTPUT_DETAILS_DIRECTORY_PATH_KEY = "directory_path"
    OUTPUT_DETAILS_FILE_NAME_KEY = "file_name"
    OUTPUT_DETAILS_METHOD = "method"
    OUTPUT_DETAILS_PROTOCOL = "protocol"
    OUTPUT_DETAILS_HOST = "host"
    OUTPUT_DETAILS_PORT = "port"
    OUTPUT_DETAILS_ENDPOINT = "endpoint"
    OUTPUT_DETAILS_AUTH = "auth"
    OUTPUT_DETAILS_USERNAME = "username"
    OUTPUT_DETAILS_PASSWORD = "password"
    XML_DECLARATION_KEY = "xml_declaration"
    INDENT_KEY = "indent"
    VARS_KEY = "vars"
    TEMPLATES_KEY = "_templates_"
    TEMPLATES_COUNT_KEY = "count"
    TEMPLATES_MODEL_KEY = "model"
    MODEL_CONTEXT_KEY = "context"
    MODEL_ATTRIBUTES_KEY = "_attrs"
    MODEL_VALUE_KEY = "_value"

    SUPPORTED_OUTPUT_FORMATS = ("xml",)

    def __init__(self, config: dict):
        super().__init__(config)
        self.output_format = MimeoConfig.__get_output_format(config)
        self.output_details = MimeoOutputDetails(self.output_format, config.get(self.OUTPUT_DETAILS_KEY, {}))
        self.xml_declaration = config.get(self.XML_DECLARATION_KEY, False)
        self.indent = MimeoConfig.__get_indent(config)
        self.vars = MimeoConfig.__get_vars(config)
        self.templates = MimeoConfig.__get_templates(config)

    @staticmethod
    def __get_output_format(config):
        output_format = config.get(MimeoConfig.OUTPUT_FORMAT_KEY, "xml")
        if output_format in MimeoConfig.SUPPORTED_OUTPUT_FORMATS:
            return output_format
        else:
            raise UnsupportedOutputFormat(f"Provided format [{output_format}] is not supported!")

    @staticmethod
    def __get_indent(config):
        indent = config.get(MimeoConfig.INDENT_KEY, 0)
        if indent >= 0:
            return indent
        else:
            raise InvalidIndent(f"Provided indent [{indent}] is negative!")

    @staticmethod
    def __get_vars(config):
        variables = config.get(MimeoConfig.VARS_KEY, {})
        if not isinstance(variables, dict):
            raise InvalidVars(f"vars property does not store an object: {variables}")
        for var, val in variables.items():
            if not re.match(r"^[A-Z][A-Z_0-9]*$", var):
                raise InvalidVars(f"Provided var [{var}] is invalid "
                                  "(you can use upper-cased name with underscore and digits, starting with a letter)!")
            if isinstance(val, list) or isinstance(val, dict):
                raise InvalidVars(f"Provided var [{var}] is invalid (you can use ony atomic values)!")
        return variables

    @staticmethod
    def __get_templates(config):
        templates = config.get(MimeoConfig.TEMPLATES_KEY)
        if templates is None:
            raise IncorrectMimeoConfig(f"No templates in the Mimeo Config: {config}")
        elif not isinstance(templates, list):
            raise IncorrectMimeoConfig(f"_templates_ property does not store an array: {config}")
        else:
            return (MimeoTemplate(template) for template in config.get(MimeoConfig.TEMPLATES_KEY))


class MimeoOutputDetails(MimeoDTO):

    FILE_DIRECTION = "file"
    STD_OUT_DIRECTION = "stdout"
    HTTP_DIRECTION = "http"

    REQUEST_POST = "POST"
    REQUEST_PUT = "PUT"

    AUTH_BASIC = "basic"
    AUTH_DIGEST = "digest"

    SUPPORTED_OUTPUT_DIRECTIONS = (STD_OUT_DIRECTION, FILE_DIRECTION, HTTP_DIRECTION)
    SUPPORTED_REQUEST_METHODS = (REQUEST_POST, REQUEST_PUT)
    SUPPORTED_AUTH_METHODS = (AUTH_BASIC, AUTH_DIGEST)
    REQUIRED_HTTP_DETAILS = (MimeoConfig.OUTPUT_DETAILS_HOST,
                             MimeoConfig.OUTPUT_DETAILS_ENDPOINT,
                             MimeoConfig.OUTPUT_DETAILS_USERNAME,
                             MimeoConfig.OUTPUT_DETAILS_PASSWORD)

    def __init__(self, output_format: str, output_details: dict):
        super().__init__(output_details)
        self.direction = MimeoOutputDetails.__get_direction(output_details)
        MimeoOutputDetails.__validate_output_details(self.direction, output_details)
        self.directory_path = MimeoOutputDetails.__get_directory_path(self.direction, output_details)
        self.file_name_tmplt = MimeoOutputDetails.__get_file_name_tmplt(self.direction, output_details, output_format)
        self.method = MimeoOutputDetails.__get_method(self.direction, output_details)
        self.protocol = MimeoOutputDetails.__get_protocol(self.direction, output_details)
        self.host = MimeoOutputDetails.__get_host(self.direction, output_details)
        self.port = MimeoOutputDetails.__get_port(self.direction, output_details)
        self.endpoint = MimeoOutputDetails.__get_endpoint(self.direction, output_details)
        self.auth = MimeoOutputDetails.__get_auth(self.direction, output_details)
        self.username = MimeoOutputDetails.__get_username(self.direction, output_details)
        self.password = MimeoOutputDetails.__get_password(self.direction, output_details)

    @staticmethod
    def __get_direction(output_details):
        direction = output_details.get(MimeoConfig.OUTPUT_DETAILS_DIRECTION_KEY, MimeoOutputDetails.FILE_DIRECTION)
        if direction in MimeoOutputDetails.SUPPORTED_OUTPUT_DIRECTIONS:
            return direction
        else:
            raise UnsupportedOutputDirection(f"Provided direction [{direction}] is not supported!")

    @staticmethod
    def __validate_output_details(direction: str, output_details: dict):
        if direction == MimeoOutputDetails.HTTP_DIRECTION:
            missing_details = []
            for detail in MimeoOutputDetails.REQUIRED_HTTP_DETAILS:
                if detail not in output_details:
                    missing_details.append(detail)
            if len(missing_details) > 0:
                missing_details_str = ', '.join(missing_details)
                raise MissingRequiredProperty(f"Missing required fields is HTTP output details: {missing_details_str}")

    @staticmethod
    def __get_directory_path(direction: str, output_details: dict):
        if direction == MimeoOutputDetails.FILE_DIRECTION:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_DIRECTORY_PATH_KEY, "mimeo-output")

    @staticmethod
    def __get_file_name_tmplt(direction: str, output_details: dict, output_format: str):
        if direction == MimeoOutputDetails.FILE_DIRECTION:
            file_name = output_details.get(MimeoConfig.OUTPUT_DETAILS_FILE_NAME_KEY, "mimeo-output")
            return f"{file_name}-{'{}'}.{output_format}"

    @staticmethod
    def __get_method(direction: str, output_details: dict):
        if direction == MimeoOutputDetails.HTTP_DIRECTION:
            method = output_details.get(MimeoConfig.OUTPUT_DETAILS_METHOD, "POST")
            if method in MimeoOutputDetails.SUPPORTED_REQUEST_METHODS:
                return method
            else:
                raise UnsupportedRequestMethod(f"Provided request method [{method}] is not supported!")

    @staticmethod
    def __get_protocol(direction: str, output_details: dict):
        if direction == MimeoOutputDetails.HTTP_DIRECTION:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_PROTOCOL, "http")

    @staticmethod
    def __get_host(direction: str, output_details: dict):
        if direction == MimeoOutputDetails.HTTP_DIRECTION:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_HOST)

    @staticmethod
    def __get_port(direction: str, output_details: dict):
        if direction == MimeoOutputDetails.HTTP_DIRECTION:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_PORT)

    @staticmethod
    def __get_endpoint(direction: str, output_details: dict):
        if direction == MimeoOutputDetails.HTTP_DIRECTION:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_ENDPOINT)

    @staticmethod
    def __get_auth(direction: str, output_details: dict):
        if direction == MimeoOutputDetails.HTTP_DIRECTION:
            auth =  output_details.get(MimeoConfig.OUTPUT_DETAILS_AUTH, "basic")
            if auth in MimeoOutputDetails.SUPPORTED_AUTH_METHODS:
                return auth
            else:
                raise UnsupportedAuthMethod(f"Provided auth [{auth}] is not supported!")

    @staticmethod
    def __get_username(direction: str, output_details: dict):
        if direction == MimeoOutputDetails.HTTP_DIRECTION:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_USERNAME)

    @staticmethod
    def __get_password(direction: str, output_details: dict):
        if direction == MimeoOutputDetails.HTTP_DIRECTION:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_PASSWORD)


class MimeoTemplate(MimeoDTO):

    def __init__(self, template: dict):
        super().__init__(template)
        MimeoTemplate.__validate_template(template)
        self.count = template.get(MimeoConfig.TEMPLATES_COUNT_KEY)
        self.model = MimeoModel(template.get(MimeoConfig.TEMPLATES_MODEL_KEY))

    @staticmethod
    def __validate_template(template: dict):
        if MimeoConfig.TEMPLATES_COUNT_KEY not in template:
            raise IncorrectMimeoTemplate(f"No count value in the Mimeo Template: {template}")
        if MimeoConfig.TEMPLATES_MODEL_KEY not in template:
            raise IncorrectMimeoTemplate(f"No model data in the Mimeo Template: {template}")


class MimeoModel(MimeoDTO):

    def __init__(self, model: dict):
        super().__init__(model)
        self.root_name = MimeoModel.__get_root_name(model)
        self.root_data = model.get(self.root_name)
        self.context_name = MimeoModel.__get_context_name(model, self.root_name)

    @staticmethod
    def __get_root_name(model: dict) -> str:
        model_keys = [key for key in filter(MimeoModel.__is_not_metadata_key, iter(model))]
        if len(model_keys) == 1:
            return model_keys[0]
        if len(model_keys) == 0:
            raise IncorrectMimeoModel(f"No root data in Mimeo Model: {model}")
        elif len(model_keys) > 1:
            raise IncorrectMimeoModel(f"Multiple root data in Mimeo Model: {model}")

    @staticmethod
    def __is_not_metadata_key(dict_key: str) -> bool:
        return dict_key not in [MimeoConfig.MODEL_CONTEXT_KEY]

    @staticmethod
    def __get_context_name(model: dict, root_name: str) -> str:
        context_name = model.get(MimeoConfig.MODEL_CONTEXT_KEY, root_name)
        if isinstance(context_name, str):
            return context_name
        else:
            raise IncorrectMimeoModel(f"Invalid context name in Mimeo Model (not a string value): {model}")
