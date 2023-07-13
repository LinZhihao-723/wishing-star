class FrequentRequestRateException(Exception):
    """
    This class represents the exception where the requests are sent in a
    frequent rate higher than capacity.
    """

    def __init__(self, message: str):
        """
        Initializes the Exception.

        :param message: Error message associated with the exception.
        """
        self.message: str = message

    def __str__(self) -> str:
        return f"Error: {self.message}"
