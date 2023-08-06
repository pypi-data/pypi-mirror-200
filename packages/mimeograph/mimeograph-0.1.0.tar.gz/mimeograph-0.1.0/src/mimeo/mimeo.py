from mimeo.config.mimeo_config import MimeoConfig
from mimeo.consumers import ConsumerFactory
from mimeo.generators import GeneratorFactory


class Mimeograph:

    def __init__(self, mimeo_config: MimeoConfig):
        self.mimeo_config = mimeo_config
        self.__generator = GeneratorFactory.get_generator(self.mimeo_config)
        self.__consumer = ConsumerFactory.get_consumer(self.mimeo_config)

    def produce(self):
        for data in self.__generator.generate(self.mimeo_config.templates):
            data_str = self.__generator.stringify(data, self.mimeo_config)
            self.__consumer.consume(data_str)
