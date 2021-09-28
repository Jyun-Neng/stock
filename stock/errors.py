class StockError(Exception):

    def __init__(self, message) -> None:
        module_name = self.__class__.__module__
        class_name = self.__class__.__name__
        error_msg = f'{message} ({module_name}.{class_name})'
        super().__init__(error_msg)


class InvalidHttpsReqError(StockError):
    """
    This error is raised when HTTPS request is failed.
    """

    def __init__(self, message) -> None:
        super().__init__(message)


class InvalidQuarterError(StockError):
    """
    This error is raised when given quarter is out of range.
    """

    def __init__(self, message) -> None:
        super().__init__(message)


class InvalidFileError(StockError):
    """
    This error is raised when the file is not exist or is not a file.
    """

    def __init__(self, message) -> None:
        super().__init__(message)


class StockDataKeyError(StockError):
    """
    This error is raised when accessing the daily stock data with invalid key.

    The valid keys in the daily stock data are:
    {"date":, "trading_vol":, "turnover": "opening":, "hi":, "lo":, "closing":,
     "transactions":}
    """

    def __init__(self, message) -> None:
        valid_keys_msg = " The valid keys are - \"date\", \"trading_vol\", " \
                "\"turnover\", \"opening\", \"hi\", \"lo\", \"closing\", " \
                "\"transactions\""
        super().__init__(message + valid_keys_msg)
