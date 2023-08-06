import logging
from pathlib import Path

from mimeo.config.mimeo_config import MimeoOutputDetails
from mimeo.consumers import Consumer

logger = logging.getLogger(__name__)


class FileConsumer(Consumer):

    def __init__(self, output_details: MimeoOutputDetails):
        self.directory = output_details.directory_path
        self.output_path_tmplt = f"{self.directory}/{output_details.file_name_tmplt}"
        self.__count = 0

    def consume(self, data: str) -> None:
        logger.fine(f"Consuming data [{data}]")
        if not Path(self.directory).exists():
            logger.info(f"Creating output directory [{self.directory}]")
            Path(self.directory).mkdir(parents=True, exist_ok=True)

        self.__count += 1
        file_name = self.output_path_tmplt.format(self.__count)

        logger.info(f"Writing data into file [{file_name}]")
        with open(file_name, "w") as output_file:
            output_file.write(data)
