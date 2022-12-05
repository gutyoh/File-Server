import os
import re
import time

from hstest import TestedProgram, CheckResult, StageTest, TestCase, WrongAnswer


class FileServerTest(StageTest):
    ON_CONNECT_EXCEPTION_MESSAGE = "A client can't connect to the server!\n" + \
                                   "Make sure the server handles connections and doesn't stop after one client " \
                                   "connected. "

    SERVER_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server", "data")

    CLIENT_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "client", "data")

    FILES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server", "data")

    ID = ""

    SAVED_FILES = dict()

    def generate(self) -> list:
        return [
            TestCase(stdin="exit", attach=self.ON_CONNECT_EXCEPTION_MESSAGE),
            TestCase(stdin="exit", attach=self.ON_CONNECT_EXCEPTION_MESSAGE),
            TestCase(stdin="exit", attach=self.ON_CONNECT_EXCEPTION_MESSAGE),
            TestCase(stdin="exit", attach=self.ON_CONNECT_EXCEPTION_MESSAGE),
            TestCase(stdin="exit", attach=self.ON_CONNECT_EXCEPTION_MESSAGE)
        ]

    # Test #1. Check if server stops
    def check_server_stop(self) -> CheckResult:
        server = self.get_server()
        server.start_in_background()

        client = self.get_client()
        client.start()
        client.execute("exit")

        try:
            time.sleep(0.5)
        except Exception as e:
            print(e)

        if not server.is_finished():
            return CheckResult.wrong("You should stop the server if a client sends 'exit'")
        return CheckResult.correct()

    # Test #2. Check folders with data
    def check_paths(self) -> CheckResult:
        if not os.path.exists(self.SERVER_DATA_PATH) or not os.path.isdir(self.SERVER_DATA_PATH):
            return CheckResult.wrong("Can't find '/server/data' folder. You should store all saved files in it!\n" +
                                     "The folder should be created even if the server wasn't started!")

        if not os.path.exists(self.CLIENT_DATA_PATH) or not os.path.isdir(self.CLIENT_DATA_PATH):
            return CheckResult.wrong("Can't find '/client/data' folder. You should store all files you want to " +
                                     "store on the server in it!\n" +
                                     "The folder should be created even if the client wasn't started!")

        return CheckResult.correct()

    def test_save_and_get(self) -> CheckResult:
        Utils.create_files(self.CLIENT_DATA_PATH)

        # Test #3. Check saving file on the server
        server = self.get_server()
        server.start_in_background()

        folder = os.path.join(self.SERVER_DATA_PATH)
        num_of_files_before_adding = Utils.num_existing_files(folder)

        client = self.get_client()
        client.start()
        client.execute("2\ntest_purpose_test1.txt")
        client_output = client.execute("")

        if "Response says that file is saved! ID =" not in client_output:
            return CheckResult.wrong("After saving a file on the server you should print:\n" +
                                     "Response says that file is saved! ID = **, where ** is an id of the file!")

        self.ID = Utils.find_id(client_output)

        num_of_files_after_adding = Utils.num_existing_files(folder)

        if num_of_files_after_adding == num_of_files_before_adding:
            return CheckResult.wrong("Once a client saved a file on the server number of files in /server/data/ "
                                     "should be changed!")

        client = self.get_client()
        client.start()
        client_output = client.execute("2\ntest_purpose_test2.txt\ntest_purpose_newFile.txt")

        if "Response says that file is saved! ID =" not in client_output:
            return CheckResult.wrong("After saving a file on the server you should print:\n" +
                                     "Response says that file is saved! ID = **, where ** is an id of the file!")

        if not Utils.is_server_file_exists("test_purpose_newFile.txt"):
            return CheckResult.wrong("Can't find a file after saving on the server." +
                                     "You should save client's files in /server/data/ folder!")

        saved_file_content = Utils.get_server_file_content("test_purpose_newFile.txt")

        if not saved_file_content == "test2":
            return CheckResult.wrong("A file after saving has wrong content!")

        # Test #4. Check getting files
        client = self.get_client()
        client.start()
        client_output = client.execute("1\n1\ntest_purpose_notExist.txt")

        if "The response says that this file is not found!" not in client_output:
            return CheckResult.wrong("When client tries to get a file by name that doesn't exist you should print:\n" +
                                     "\"The response says that this file is not found!\"")

        client = self.get_client()
        client.start()
        client_output = client.execute("1\n2\n" + (self.ID + "511"))

        if "The response says that this file is not found!" not in client_output:
            return CheckResult.wrong("When client tries to get a file by ID that doesn't exist you should print:\n" +
                                     "\"The response says that this file is not found!\"")

        client = self.get_client()
        client.start()
        client.execute("1\n1\ntest_purpose_newFile.txt\ntest_purpose_get.txt")

        if not Utils.is_client_file_exists("test_purpose_get.txt"):
            return CheckResult.wrong("Can't find a file after getting it from the server by name.\n" +
                                     "You should store all downloaded files from the server in /client/data/ folder.")

        downloaded_by_name_file_content = Utils.get_client_file_content("test_purpose_get.txt")
        if not downloaded_by_name_file_content == "test2":
            return CheckResult.wrong("After getting a file from the server by name it has wrong content!")

        client = self.get_client()
        client.start()
        client.execute("1\n2\n" + self.ID + "\ntest_purpose_get_id.txt")

        if not Utils.is_client_file_exists("test_purpose_get_id.txt"):
            return CheckResult.wrong("Can't find a file after getting it from the server by ID.\n" +
                                     "You should store all downloaded files from the server in /client/data/ folder.")

        downloaded_by_id_file_content = Utils.get_client_file_content("test_purpose_get_id.txt")
        if not downloaded_by_id_file_content == "test1":
            return CheckResult.wrong("After getting a file from the server by ID it has wrong content!")

        client = self.get_client()
        client.start()
        client.execute("exit")

        return CheckResult.correct()

    def test_get_after_server_restart(self) -> CheckResult:
        server = self.get_server()
        client = self.get_client()

        server.start_in_background()
        client.start()
        client.execute("1\n1\ntest_purpose_newFile.txt\ntest_purpose_get_after_restart.txt")

        if not Utils.is_client_file_exists("test_purpose_get_after_restart.txt"):
            return CheckResult.wrong("Can't find a file after getting it from the server by name.\n" +
                                     "Looks like your server lose all stored files after restart.\n" +
                                     "You should store all downloaded files from the server in /client/data/ folder.")

        client = self.get_client()
        client.start()
        client.execute("1\n2\n" + self.ID + "\ntest_purpose_get_by_id_after_restart.txt")

        if not Utils.is_client_file_exists("test_purpose_get_by_id_after_restart.txt"):
            return CheckResult.wrong("Can't find a file after getting it from the server by ID.\n" +
                                     "Looks like your server lose all stored files after restart.\n" +
                                     "You should store all downloaded files from the server in /client/data/ folder.")

        client = self.get_client()
        client.start()
        client.execute("exit")

        return CheckResult.correct()

    def test_delete_files(self) -> CheckResult:
        server = self.get_server()
        client = self.get_client()

        #  File folder = new File(serverDataPath);
        folder = os.path.join(self.SERVER_DATA_PATH)
        num_of_files_before_deleting = Utils.num_existing_files(folder)

        server.start_in_background()
        client.start()
        client.execute("3\n1\ntest_purpose_newFile.txt")

        time.sleep(2)
        num_of_files_after_deleting_by_name = Utils.num_existing_files(folder)
        if num_of_files_before_deleting == num_of_files_after_deleting_by_name:
            return CheckResult.wrong("Once a client deleted a file by name from the server, " +
                                     "number of files in /server/data/ should be fewer!")

        client = self.get_client()
        client.start()
        client.execute("3\n2\n" + self.ID)

        time.sleep(2)
        num_of_files_after_deleting_by_id = Utils.num_existing_files(folder)
        if num_of_files_after_deleting_by_name == num_of_files_after_deleting_by_id:
            return CheckResult.wrong("Once a client deleted a file by ID from the server, " +
                                     "number of files in /server/data/ should be fewer!")

        client = self.get_client()
        client.start()
        client.execute("exit")

        return CheckResult.correct()

    @staticmethod
    def after_test_delete_files():
        Utils.delete_test_files()

    @staticmethod
    def get_client() -> TestedProgram:
        return TestedProgram("client")

    @staticmethod
    def get_server() -> TestedProgram:
        return TestedProgram("server")


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


if __name__ == '__main__':
    FileServerTest().run_tests()
