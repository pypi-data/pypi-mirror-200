"""
PyCrawlerX - A Python Path Crawling Tool for Windows
"""
import re
import os
import sys
import subprocess

class PyCrawlerX:
    """
    PyCrawlerX - A Python Path Crawling Tool for Windows

    Note:
        You can Ignore the directories, files and extensions by adding them in the
        IGNORE_DIRS, IGNORE_FILES and IGNORE_EXTENSIONS list.
    """

    __IGNORE_DIRS = ['env', 'venv', '__pycache__']
    __IGNORE_FILES = ['__init__.py', 'setup.py']
    __IGNORE_DIRS_PATTERN = [r'\d{8}_\d{6}']
    __IGNORE_EXTENSIONS = ['.pyc', '.pyo', '.txt']

    def __init__(self):
        """
        Initialize the class.
        """
        self.path_ = None
        self.content = {}
        self.clean_content = {}
        self.curr_files_count = 0
        self.curr_dirs_count = 0

    def __is_dir_of_file(self, dir_or_file: str) -> None:
        """
        Check if the given path is a file.

        Args:
            dir_or_file (str): The path of the file or directory.

        Returns:
            None
        """
        self.curr_files_count += os.path.isfile(dir_or_file)
        self.curr_dirs_count += os.path.isdir(dir_or_file)

    def __is_valid_content(self, dir_or_file: str) -> bool:
        """
        Check if the given directory or file is valid.

        Args:
            dir_or_file (str): The path of the file or directory.

        Returns:
            bool: True if the given directory or file is valid, False otherwise.
        """
        if dir_or_file in self.__IGNORE_DIRS or dir_or_file in self.__IGNORE_FILES:
            return False
        for each_externsion in self.__IGNORE_EXTENSIONS:
            if dir_or_file.endswith(each_externsion):
                return False
        for pattern in self.__IGNORE_DIRS_PATTERN:
            if re.match(pattern, dir_or_file):
                return False
        return True

    def __clean_name(self, dir_or_file: str) -> str:
        """
        Clean the name of the file or directory.

        Args:
            dir_or_file (str): The path of the file or directory.

        Returns:
            str: The cleaned name of the file or directory.
        """
        if os.path.isfile(os.path.join(self.path_, dir_or_file)):
            # Remove the extension of the file and return the name.
            __file_name = os.path.splitext(os.path.basename(dir_or_file))[0]
            return str(__file_name).replace("_", " ").capitalize()
        return str(os.path.basename(dir_or_file)).replace("_", " ").capitalize()

    def __clean_file_name_ind(self, file_path: str) -> str:
        """
        Clean the name of the file only.

        Args:
            file_path (str): The path of the file.

        Returns:
            str: The cleaned name of the file.
        """
        if os.path.isfile(file_path):
            # Remove the extension of the file and return the name.
            __file_name = os.path.splitext(os.path.basename(file_path))[0]
            return str(__file_name).replace("_", " ").capitalize()

    def __execute_file(self, file_path: str) -> None:
        """
        Execute the file.

        Args:
            file_path (str): The path of the file to execute.

        Returns:
            None
        """
        user_input = input("Do you want to execute this file? (y/n): ").lower()
        if user_input == "y":
            clean_filename = self.__clean_file_name_ind(file_path)
            print(f"Executing {clean_filename}...")
            try:
                subprocess.run(f'python "{file_path}"', shell=True, check=True)
                print("File executed successfully.")
            except subprocess.CalledProcessError as error_msg:
                print("Error: ", error_msg)
        self.__crawl(os.path.dirname(file_path))

    def __execute_all_files(self) -> None:
        """
        Execute all the files in the current directory.

        Returns:
            None
        """
        user_input = input("Do you want to execute the above files? (y/n): ").lower()
        if user_input == "y":
            for file in os.listdir(self.path_):
                file_path = os.path.join(self.path_, file)
                if os.path.isfile(file_path):
                    clean_filename = self.__clean_file_name_ind(file_path)
                    print(f"Executing {clean_filename}...")
                    try:
                        subprocess.run(f'python "{file_path}"', shell=True, check=True)
                        print("File executed successfully.")
                    except subprocess.CalledProcessError as error_msg:
                        print("Error: ", error_msg)
            self.__crawl(self.path_)

    def __crawl(self, path_: str) -> None:
        """
        Crawl the path and list out the content in that path.
        Content can be files or directories.

        Args:
            path_ (str): The path to crawl.

        Returns:
            None
        """
        __inc_num = 0
        self.path_ = path_
        self.curr_files_count = 0
        self.content = {}
        self.clean_content = {}
        if os.path.isdir(self.path_):
            if len(os.listdir(self.path_)) > 0:
                for dir_or_file in os.listdir(self.path_):
                    if self.__is_valid_content(dir_or_file):
                        __inc_num += 1
                        __clean_name = self.__clean_name(dir_or_file)
                        self.__is_dir_of_file(os.path.join(self.path_, dir_or_file))
                        self.content[__clean_name] = os.path.join(self.path_, dir_or_file)
                        self.clean_content[__inc_num] = __clean_name

                if self.curr_files_count >= 2:
                    self.clean_content[len(self.clean_content) + 1] = "All Files"
                if os.path.dirname(self.path_):
                    self.clean_content[len(self.clean_content) + 1] = "Back"
                self.clean_content[len(self.clean_content) + 1] = "Exit"
            else:
                __message = "\nThis directory is empty.\n"
                self.clean_content[len(self.clean_content) + 1] = "Back"
                self.clean_content[len(self.clean_content) + 1] = "Exit"
                self.__cli_menu(__message)
        elif os.path.isfile(self.path_):
            self.__execute_file(self.path_)
        self.__cli_menu()

    def __content_info(self, message: str = None) -> None:
        """
        Print the content information.
        """
        print("=====================================================")
        print(f"Current Directory: {self.path_}")
        print("=====================================================")
        if message:
            print(message)
        for key, value in self.clean_content.items():
            print(f"{key}. {value}")
        print("=====================================================")

    def __cli_menu(self, message: str = None) -> None:
        """
        A CLI Menu for PyCrawlerX.

        Returns:
            None
        """
        self.__content_info(message)
        __user_input = int(input("Enter your choice: "))
        if self.clean_content[__user_input] == "Exit":
            sys.exit()
        elif self.clean_content[__user_input] == "Back":
            self.__crawl(os.path.dirname(self.path_))
        elif self.clean_content[__user_input] == "All Files":
            self.__execute_all_files()
        else:
            self.__crawl(path_ = self.content[self.clean_content[__user_input]])

    def load_environment_variables(self, key_value: dict) -> None:
        """
        Create the environment variables using key_value dictionary

        Args:
            key_value (dict): The dictionary with key and value

        Returns:
            None
        """
        for key, value in key_value.items():
            os.environ[key] = value

    def run_pycrawlerx(self, folder_path: str) -> None:
        """
        Run the PyCrawlerX.

        Args:
            path_ (str): The path to crawl.

        Returns:
            None
        """
        self.__crawl(path_ = folder_path)
        self.__cli_menu()
