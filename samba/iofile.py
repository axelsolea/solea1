import os


class IoFile:
    """
    Utility class for file input/output operations.

    Provides static methods for:
    - Checking the existence of a file or directory.
    - Creating a file with specified content.
    - Reading the contents of a file.
    - Creating a directory if a specified configuration file exists.
    - Deleting a directory.

    Attributes:
        None

    Methods:
        check_exist(name: str) -> bool:
            Checks if the specified file exists and is readable.

        create_file(name: str, content: str = "") -> bool:
            Creates a file with the specified name and optional content.

        read_file(name: str) -> str:
            Reads the contents of the specified file.

        create_dir(name: str) -> bool:
            Creates a directory with the specified name if a configuration
            file named 'logging_config.json' exists.

        delete_dir(name: str) -> bool:
            Deletes the specified directory.

    Usage:
        # Example usage of IoFile class methods
        if IoFile.check_exist('example.txt'):
            print("File exists and is readable.")
        else:
            print("File does not exist or is not readable.")

        if IoFile.create_file('example.txt', 'Hello, world!'):
            print("File created successfully.")
        else:
            print("Failed to create file.")

        content = IoFile.read_file('example.txt')
        print("File content:", content)

        if IoFile.create_dir('example_dir'):
            print("Directory created successfully.")
        else:
            print("Failed to create directory.")

        if IoFile.delete_dir('example_dir'):
            print("Directory deleted successfully.")
        else:
            print("Failed to delete directory.")
    """
    @staticmethod
    def check_exist(name: str) -> bool:
        """
        Check if the specified file exists and is readable.

        Args:
            name (str): The name of the file to check.

        Returns:
            bool: True if the file exists and is readable, False otherwise.
        """
        filepath = os.path.join(os.getcwd(), name)
        if not os.access(filepath, os.R_OK):
            return False

        return os.path.isfile(filepath)

    @staticmethod
    def create_file(name: str, content="") -> bool:
        """
        Create a file with the specified name and optional content.

        Args:
            name (str): The name of the file to create.
            content (str, optional): The content to write to the file. Defaults to "".

        Returns:
            bool: True if the file is created successfully, False otherwise.
        """
        filepath = os.path.join(os.getcwd(), name)
        if not IoFile.check_exist(filepath):
            return False

        with open(filepath, 'w') as f:
            f.write(content)
            return True

    @staticmethod
    def read_file(name: str) -> str:
        """
        Read the contents of the specified file.

        Args:
            name (str): The name of the file to read.

        Returns:
            str: The contents of the file.
        """
        filepath = os.path.join(os.getcwd(), name)
        if not IoFile.check_exist(filepath):
            return ""

        with open(filepath, 'r') as f:
            return f.read()

    @staticmethod
    def create_dir(name: str) -> bool:
        """
        Create a directory with the specified name if a configuration
        file named 'logging_config.json' exists.

        Args:
            name (str): The name of the directory to create.

        Returns:
            bool: True if the directory is created successfully, False otherwise.
        """
        if not IoFile.check_exist('logging_config.json'):
            return False

        filepath = os.path.join(os.getcwd(), name)
        if not os.path.exists(filepath):
            os.makedirs(filepath)
            return True
        else:
            return False

    @staticmethod
    def delete_dir(name: str) -> bool:
        """
        Deletes the specified directory.

        Args:
            name (str): The name of the directory to delete.

        Returns:
            bool: True if the directory is deleted successfully, False otherwise.
        """
        filepath = os.path.join(os.getcwd(), name)
        if os.path.exists(filepath):
            os.rmdir(filepath)
            return True
        else:
            return False

if __name__ == "__main__":
    # Test IoFile class methods
    example_file = "example.txt"
    example_dir = "example_dir"

    # Checking file existence
    if IoFile.check_exist(example_file):
        print("File exists and is readable.")
    else:
        print("File does not exist or is not readable.")

    # Creating a file
    if IoFile.create_file(example_file, 'Hello, world!'):
        print("File created successfully.")
    else:
        print("Failed to create file.")

    # Reading file content
    content = IoFile.read_file(example_file)
    print("File content:", content)

    # Creating a directory
    if IoFile.create_dir(example_dir):
        print("Directory created successfully.")
    else:
        print("Failed to create directory.")

    # Deleting a directory
    if IoFile.delete_dir(example_dir):
        print("Directory deleted successfully.")
    else:
        print("Failed to delete directory.")


if __name__ == "__main__":
    # Test IoFile class methods
    example_file = "example.txt"
    example_dir = "example_dir"

    # Checking file existence
    if IoFile.check_exist(example_file):
        print("File exists and is readable.")
    else:
        print("File does not exist or is not readable.")

    # Creating a file
    if IoFile.create_file(example_file, 'Hello, world!'):
        print("File created successfully.")
    else:
        print("Failed to create file.")

    # Reading file content
    content = IoFile.read_file(example_file)
    print("File content:", content)

    # Creating a directory
    if IoFile.create_dir(example_dir):
        print("Directory created successfully.")
    else:
        print("Failed to create directory.")

    # Deleting a directory
    if IoFile.delete_dir(example_dir):
        print("Directory deleted successfully.")
    else:
        print("Failed to delete directory.")
