import os


class IoFile:
    """
    Utility class for file input/output operations.

    Provides static methods for:
    - Checking the existence of a file or directory.
    - Creating a file with specified content.
    - Reading the contents of a file.
    - Creating a directory if it does not already exist.
    - Deleting a directory.
    - Deleting a file.

    Attributes:
        None

    Methods:
        check_exist(name: str) -> bool:
            Checks if the specified file or directory exists.

        create_file(name: str, content: str = "") -> bool:
            Creates a file with the specified name and optional content.

        read_file(name: str) -> str:
            Reads the contents of the specified file.

        create_dir(name: str) -> bool:
            Creates a directory with the specified name if it does not already exist.

        delete_dir(name: str) -> bool:
            Deletes the specified directory.

        delete_file(name: str) -> bool:
            Deletes the specified file.

    Usage:
        # Example usage of IoFile class methods
        if IoFile.check_exist('example.txt'):
            print("File or directory exists.")
        else:
            print("File or directory does not exist.")

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

        if IoFile.delete_file('example.txt'):
            print("File deleted successfully.")
        else:
            print("Failed to delete file.")
    """

    @staticmethod
    def check_exist(name: str) -> bool:
        """
        Check if the specified file or directory exists.

        Args:
            name (str): The name of the file or directory to check.

        Returns:
            bool: True if the file or directory exists, False otherwise.
        """
        return os.path.exists(name)

    @staticmethod
    def create_file(name: str, content: str = "") -> bool:
        """
        Create a file with the specified name and optional content.

        Args:
            name (str): The name of the file to create.
            content (str, optional): The content to write to the file. Defaults to "".

        Returns:
            bool: True if the file is created successfully, False otherwise.
        """
        if not IoFile.check_exist(name):
            with open(name, 'w') as f:
                f.write(content)
            return True
        else:
            return False

    @staticmethod
    def read_file(name: str) -> str:
        """
        Read the contents of the specified file.

        Args:
            name (str): The name of the file to read.

        Returns:
            str: The contents of the file.
        """
        if IoFile.check_exist(name):
            with open(name, 'r') as f:
                return f.read()
        else:
            return ""

    @staticmethod
    def create_dir(name: str) -> bool:
        """
        Create a directory with the specified name if it does not already exist.

        Args:
            name (str): The name of the directory to create.

        Returns:
            bool: True if the directory is created successfully or already exists, False otherwise.
        """
        if not os.path.exists(name):
            os.makedirs(name)
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
        if os.path.exists(name):
            os.rmdir(name)
            return True
        else:
            return False

    @staticmethod
    def delete_file(name: str) -> bool:
        """
        Deletes the specified file.

        Args:
            name (str): The name of the file to delete.

        Returns:
            bool: True if the file is deleted successfully, False otherwise.
        """
        try:
            os.remove(name)
            return True
        except FileNotFoundError:
            return False


if __name__ == "__main__":
    # Test IoFile class methods
    example_file = "/tmp/share/test.txt"
    example_dir = "/tmp/share"

    # Creating a directory
    if IoFile.create_dir(example_dir):
        print(f"Directory {example_dir} created successfully.")
    else:
        print(f"Failed to create directory: {example_dir}")

    # Creating a file
    if IoFile.create_file(example_file, 'Hello, world!'):
        print(f"File {example_file} created successfully.")
    else:
        print(f"Failed to create file: {example_file}")

    # Checking file existence
    if IoFile.check_exist(example_file):
        print(f"File {example_file} exists and is readable.")
    else:
        print(f"File {example_file} does not exist or is not readable.")

    # Reading file content
    content = IoFile.read_file(example_file)
    print("File content:", content)

    # Deleting the file
    if IoFile.delete_file(example_file):
        print(f"File {example_file} deleted successfully.")
    else:
        print(f"Failed to delete file: {example_file}")

    # Deleting the directory
    if IoFile.delete_dir(example_dir):
        print(f"Directory {example_dir} deleted successfully.")
    else:
        print(f"Failed to delete directory: {example_dir}")
