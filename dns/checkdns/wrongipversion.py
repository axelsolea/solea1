class WrongIpVersion(Exception):
    """Exception raised for wrong IP version.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self, message: str):
        """
        Initialize the exception.

        Args:
            message (str): Explanation of the error.
        """
        super().__init__(message)
