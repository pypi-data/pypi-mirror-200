from mimeo.config.mimeo_config import MimeoConfig, UnsupportedOutputFormat
from mimeo.generators import Generator, GeneratorUtils, XMLGenerator


class GeneratorFactory:

    XML = "xml"

    @staticmethod
    def get_generator(mimeo_config: MimeoConfig) -> Generator:
        output_format = mimeo_config.output_format
        if output_format == GeneratorFactory.XML:
            return XMLGenerator(mimeo_config)
        else:
            raise UnsupportedOutputFormat(f"Provided format [{output_format}] is not supported!")
