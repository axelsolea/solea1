class WrongVerboseLevel(Exception):
    """Exception raised for wrong verbose level.

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
