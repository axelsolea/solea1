import os
from dataclasses import dataclass

@dataclass
class Logger:
    """
    Logger class for simple log file management.

    Attributes:
        _dir (str): Directory of the script or module.
        _path (str): Full path to the log file.
        _nb_log (int): Number of log entries.

    Methods:
        emptyFile(): Empties the log file.
        writeFile(status: str, message: str): Writes a log entry with the provided status and message.
        readFile() -> str: Reads the content of the log file.
        testFile() -> bool: Tests the Logger by writing log entries, reading the file, and performing checks on the content.
        deleteFile(): Deletes the log file.

    Initialize the Logger instance.

    Args:
        path (str): The path to the log file. If `absolut_path` is False, it's treated as a relative path.
        absolut_path (bool, optional): If True (default), `path` is treated as an absolute path. If False,
            it's treated as a relative path to the directory of the script or module.

    Examples:
        # Using an absolute path
        log = Logger("/path/to/log.log")

        # Using a relative path
        log = Logger("relative/log.log", absolut_path=False)
    """


    def __init__(self, path: str, absolut_path: bool = True):
        if absolut_path:
            self._path: str = path
        else:
            self._dir: str = os.path.dirname(__file__)
            self._path: str = os.path.join(self._dir, path)
        self._nb_log: int = 0

    
    def emptyFile(self) -> None:
        """
        Empties the content of the log file.
        """
        with open(self._path, 'w'):
            pass


    def writeFile(self, status: str, message: str) -> None:
        """
        Writes a log entry with the given status and message.

        Args:
            status (str): The status of the log entry (e.g., INFO, ERROR).
            message (str): The log message.
        """
        with open(self._path, 'a') as file:
            file.write(f"{status}: {message}\n")
        self._nb_log += 1


    def readFile(self) -> str:
        """
        Reads the content of the log file.

        Returns:
            str: The content of the log file.
        """
        with open(self._path, 'r') as file:
            data: str = file.read()
        return data
    
    def testFile(self) -> bool:
        """
        Test if the file can be write into

        Returns:
            bool: True if it possible otherwise False
        """
        self.writeFile("INFO", "Test log entry 1")
        self.writeFile("ERROR", "Test log entry 2")
        content: str = self.readFile()

        if "INFO" in content and "ERROR" in content:
            return True
        else:
            return False

    def deleteFile(self) -> None:
        """
        Deletes the log file.
        """
        if os.path.exists(self._path):
            os.remove(self._path)
            print(f"File: {self._path} deleted...OK")
        else:
            print(f"File: {self._path} not found...")
