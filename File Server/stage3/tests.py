import os
import time
import random

from hstest import TestedProgram, CheckResult, StageTest, TestCase


class FileServerTest(StageTest):
    ON_CONNECT_EXCEPTION_MESSAGE = "A client can't connect to the server!\n" + \
                                   "Make sure the server handles connections and doesn't stop after one client " \
                                   "connected. "

    FILES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server", "data")

    SAVED_FILES = dict()

    def generate(self):
        return [TestCase(stdin="exit", attach=self.ON_CONNECT_EXCEPTION_MESSAGE)]

    def test(self):

        self.test_stop_server()

        # client = TestedProgram("client")
        server = TestedProgram("server")
        # file_name = ""
        # file_content = ""

        if not os.path.exists(self.FILES_PATH) or not os.path.isdir(self.FILES_PATH):
            return CheckResult.wrong("Can't find '/server/data' folder. You should store all saved files in it!\n" +
                                     "The folder should be created even if the server wasn't started!")

        # Delete files in case the previous test was failed with exception
        self.delete_test_files()
        server.start_in_background()

        # Test #1 Saving a file on the server
        client = self.get_client()
        client.start()
        file_name = FileNameGenerator.name()
        file_content = FileNameGenerator.content()
        self.SAVED_FILES[file_name] = file_content
        client.execute(f"save {file_name} {file_content}")

        if not self.is_file_exists(file_name):
            return CheckResult.wrong("Can't find just saved file in the /server/data folder!")

        saved_file_content = self.get_file_content(file_name)
        if not saved_file_content == self.SAVED_FILES[file_name]:
            return CheckResult.wrong("A file after saving has wrong content!")

        # // Test #2 Saving a fail that already exists
        client = self.get_client()
        client.start()
        output = client.execute(f"save {file_name} {file_content}")

        if "The response says that creating the file was forbidden!" not in output:
            return CheckResult.wrong("You should print 'The response says that creating the file was forbidden!' " +
                                     "if a client tries to add file that already exist!")

        # // Test #3 Getting a file
        client = self.get_client()
        client.start()
        output = client.execute(f"1\n{file_name}")

        if "The content of the file is" not in output:
            return CheckResult.wrong("When a client tries to get a file that is stored on the server" +
                                     "you should print:\n\"The content of the file is: FILE_CONTENT\"\nwhere "
                                     "FILE_CONTENT is a " +
                                     "content of the requested file!")

        if file_content not in output:
            return CheckResult.wrong("The server returned wrong content of the file!")

        # Test #4 Getting a not existing file
        client = self.get_client()
        client.start()
        file_name = FileNameGenerator.name()
        output = client.execute(f"1\n{file_name}")

        if "The response says that the file was not found!" not in output:
            return CheckResult.wrong("You should print \"The response says that the file was not found!\" if a" +
                                     " client tries to request a file that doesn't exist")

        # Test #5 Deleting a file that doesn't exist
        client = self.get_client()
        client.start()
        file_name = FileNameGenerator.name()
        output = client.execute(f"3\n{file_name}")

        if "The response says that the file was not found!" not in output:
            return CheckResult.wrong("You should print \"The response says that the file was not found!\" if a" +
                                     " client tries to delete a file that doesn't exist")

        # Test #6 Deleting a file
        client = self.get_client()
        client.start()

        file_name = list(self.SAVED_FILES.keys())[0]
        client.execute(f"3\n{file_name}")

        if self.is_file_exists(file_name):
            return CheckResult.wrong("You should delete a file from /server/data folder if the user requests it!")

        # Stop server
        client = self.get_client()
        client.start()
        client.execute("exit")

        return CheckResult.correct()

    @staticmethod
    def test_stop_server():
        server = TestedProgram("server")
        client = TestedProgram("client")

        server.start_in_background()
        client.start()
        client.execute("exit")

        try:
            time.sleep(0.2)
        except KeyboardInterrupt:  # This should be InterruptedException in Java
            pass

        if not server.is_finished():
            return CheckResult.wrong("The server should stop after a client sends 'exit'!")

    def delete_test_files(self):
        _dir = os.listdir(self.FILES_PATH)
        for file in _dir:
            if file.startswith("test_purpose_"):
                os.remove(os.path.join(self.FILES_PATH, file))
                is_deleted = os.path.exists(os.path.join(self.FILES_PATH, file))
                if not is_deleted:
                    return CheckResult.wrong("Can't delete test files. Maybe they are not closed!")

    def is_file_exists(self, file_name):
        return os.path.exists(os.path.join(self.FILES_PATH, file_name))

    def get_file_content(self, file_name):
        path = os.path.join(self.FILES_PATH, file_name)
        try:
            return open(path, "r").read().strip()
        except IOError as e:
            print(e)

        raise Exception("Can't read file!")

    def after_test_delete_files(self):
        self.delete_test_files()

    @staticmethod
    def get_client():
        return TestedProgram("client")


class FileNameGenerator:
    LEXICON = "ABCDEFGHIJKLMNOPQRSTUVWXYZ12345674890"

    rand = random.Random()

    identifiers = set()

    @staticmethod
    def name():
        return FileNameGenerator.generate(5, True)

    @staticmethod
    def content():
        return FileNameGenerator.generate(15, False)

    @staticmethod
    def generate(length, name):
        builder = ""
        while len(builder) == 0:
            if name:
                builder += "test_purpose_"
            length = random.randint(0, length) + 5
            for i in range(length):
                builder += random.choice(FileNameGenerator.LEXICON)
            if builder in FileNameGenerator.identifiers:
                builder = ""
            else:
                FileNameGenerator.identifiers.add(builder)
        if name:
            builder += ".txt"
        return builder


if __name__ == '__main__':
    FileServerTest().run_tests()
