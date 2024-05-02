class PermissionError(Exception):
    """
    Exception raised when attempting to access a file or directory that does not exist.

    Attributes:
        *args: Additional arguments (optional).
    """

    def __init__(self, *args: object) -> None:
        """
        Initializes a new instance of the ErrorFileNotFound exception.

        Args:
            *args: Additional arguments (optional).
        """
        super().__init__(*args)
