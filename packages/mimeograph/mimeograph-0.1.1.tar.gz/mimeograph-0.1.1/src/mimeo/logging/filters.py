from logging import DEBUG, INFO, Filter, LogRecord


class RegularFilter(Filter):

    def filter(self, record: LogRecord):
        return record.levelno >= INFO


class DetailedFilter(Filter):

    def filter(self, record: LogRecord):
        return record.levelno <= DEBUG
