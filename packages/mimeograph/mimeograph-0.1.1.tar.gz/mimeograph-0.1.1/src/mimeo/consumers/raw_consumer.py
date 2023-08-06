from mimeo.consumers import Consumer


class RawConsumer(Consumer):

    def consume(self, data: str) -> None:
        print(data)
