import os
import shutil


class FileManager:
    """
    FileManager class for managing file operations within a specified directory.

    This class provides methods for:
    - Checking the existence of a file or directory.
    - Creating a file with specified content.
    - Reading the contents of a file.
    - Creating a directory if it does not already exist.
    - Deleting a directory.
    - Deleting a file.

    Attributes:
        directory (str): The directory path where file operations will be performed.

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
    """

    def __init__(self, directory: str):
        """
        Initialize the FileManager object with the specified directory.

        Args:
            directory (str): The directory path where file operations will be performed.
        """
        self.directory: str = directory

    def check_exist(self, name):
        """
        Check if the specified file or directory exists.

        Args:
            name (str): The name of the file or directory to check.

        Returns:
            bool: True if the file or directory exists, False otherwise.
        """
        return os.path.exists(os.path.join(self.directory, name))

    def create_file(self, name, content=""):
        """
        Create a file with the specified name and optional content.

        Args:
            name (str): The name of the file to create.
            content (str, optional): The content to write to the file. Defaults to "".

        Returns:
            bool: True if the file is created successfully, False otherwise.
        """
        file_path = os.path.join(self.directory, name)

        if not self.check_exist(name):
            with open(file_path, 'w') as f:
                f.write(content)
            return True
        else:
            return False

    def read_file(self, name):
        """
        Read the contents of the specified file.

        Args:
            name (str): The name of the file to read.

        Returns:
            str: The contents of the file.
        """
        file_path = os.path.join(self.directory, name)

        if self.check_exist(name):
            with open(file_path, 'r') as f:
                return f.read()
        else:
            return ""

    def create_dir(self, name: str = "") -> bool:
        """
        Create a directory with the specified name if it does not already exist.

        If no name is provided, the method will attempt to create a directory in the root directory specified by `self.directory`.

        Args:
            name (str, optional): The name of the directory to create. Defaults to "".

        Returns:
            bool: True if the directory is created successfully or already exists, False otherwise.
        """
        if not name:
            dir_path = self.directory
        else:
            dir_path = os.path.join(self.directory, name)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            return True
        else:
            return False
    
    def delete_dir(self, name: str = "") -> bool:
        """
        Deletes the specified directory.

        If no name is provided, the method will attempt to delete the root directory specified by `self.directory`.

        Args:
            name (str, optional): The name of the directory to delete. Defaults to "".

        Returns:
            bool: True if the directory is deleted successfully, False otherwise.
        """
        if not name:
            dir_path = self.directory
        else:
            dir_path = os.path.join(self.directory, name)

        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            return True
        else:
            return False
    
    def delete_file(self, name):
        """
        Deletes the specified file.

        Args:
            name (str): The name of the file to delete.

        Returns:
            bool: True if the file is deleted successfully, False otherwise.
        """
        file_path = os.path.join(self.directory, name)

        try:
            os.remove(file_path)
            return True
        except FileNotFoundError:
            return False


if __name__ == "__main__":
    # Création de l'objet FileManager pour le répertoire /tmp/share
    file_manager = FileManager("/tmp/share")

    # Vérification de l'existence du répertoire /tmp/share
    if file_manager.check_exist(''):
        print("Directory '/tmp/share' exists.")
    else:
        print("Directory '/tmp/share' does not exist.")
    
    # Suppression du répertoire /tmp/share
    if file_manager.create_dir(''):
        print("Directory '/tmp/share' created successfully.")
    else:
        print("Failed to create directory '/tmp/share'.")


    # Création du fichier /tmp/share/test.txt avec le contenu "test de oem 1"
    if file_manager.create_file('test.txt', 'test de oem 1'):
        print("File '/tmp/share/test.txt' created successfully.")
    else:
        print("Failed to create file '/tmp/share/test.txt'.")

    # Vérification de l'existence du fichier /tmp/share/test.txt
    if file_manager.check_exist('test.txt'):
        print("File '/tmp/share/test.txt' exists.")
    else:
        print("File '/tmp/share/test.txt' does not exist.")

    # Lecture du fichier /tmp/share/test.txt
    content = file_manager.read_file('test.txt')
    print("File content:", content)

    # Suppression du fichier /tmp/share/test.txt
    if file_manager.delete_file('test.txt'):
        print("File '/tmp/share/test.txt' deleted successfully.")
    else:
        print("Failed to delete file '/tmp/share/test.txt'.")

    # Suppression du répertoire /tmp/share
    if file_manager.delete_dir(''):
        print("Directory '/tmp/share' deleted successfully.")
    else:
        print("Failed to delete directory '/tmp/share'.")

