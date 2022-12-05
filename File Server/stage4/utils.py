import re
import os
from hstest import WrongAnswer
from tests import FileServerTest


class Utils:

    @staticmethod
    def find_id(output):
        pattern = re.compile("ID = (\\d+)")
        matcher = pattern.search(output)

        if matcher:
            count = len(matcher.groups())
            if count != 1:
                raise WrongAnswer("Can't find ID of the file in the output!\nMake sure you print ID like in examples!")
            return matcher.group(1)
        else:
            raise WrongAnswer("Can't find ID of the file in the output!\nMake sure you print ID like in examples!")

    @staticmethod
    def delete_test_files():
        _dir = os.listdir(FileServerTest.SERVER_DATA_PATH)
        for file in _dir:
            if file.startswith("test_purpose_"):
                if not os.remove(os.path.join(FileServerTest.SERVER_DATA_PATH, file)):
                    raise WrongAnswer("Can't delete test files. Maybe they are not closed!")

        cdir = os.listdir(FileServerTest.CLIENT_DATA_PATH)
        for file in cdir:
            if file.startswith("test_purpose_"):
                if not os.remove(os.path.join(FileServerTest.CLIENT_DATA_PATH, file)):
                    raise WrongAnswer("Can't delete test files. Maybe their input streams are not closed!")

    @staticmethod
    def create_files(client_data_path):
        for i in range(2):
            try:
                file = open(os.path.join(client_data_path, "test_purpose_test{}.txt".format(i + 1)), "w")
                file.write("test{}".format(i + 1))
                file.close()
            except IOError as e:
                raise WrongAnswer("Can't create test files!")

    @staticmethod
    def num_existing_files(file):
        files = os.listdir(file)
        if files is None:
            return 0
        return len(files)

    @staticmethod
    def is_file_exists(path):
        return os.path.exists(path) and not os.path.isdir(path)

    @staticmethod
    def is_client_file_exists(file_name):
        return Utils.is_file_exists(os.path.join(FileServerTest.CLIENT_DATA_PATH, file_name))

    @staticmethod
    def is_server_file_exists(file_name):
        return Utils.is_file_exists(os.path.join(FileServerTest.SERVER_DATA_PATH, file_name))

    @staticmethod
    def get_server_file_content(file_name):
        return Utils.get_file_content(os.path.join(FileServerTest.SERVER_DATA_PATH, file_name))

    @staticmethod
    def get_client_file_content(file_name):
        return Utils.get_file_content(os.path.join(FileServerTest.CLIENT_DATA_PATH, file_name))

    @staticmethod
    def get_file_content(file_name):
        try:
            with open(file_name, "r") as file:
                return file.read().strip()
        except IOError as e:
            raise WrongAnswer("Can't read files content.\n" +
                              "Make sure you close input/output streams after reading or writing files!")
