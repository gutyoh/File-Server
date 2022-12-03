import os
import time

from hstest import TestedProgram, CheckResult, StageTest, dynamic_test, TestCase
from collections import OrderedDict


class FileServerTest(StageTest):
    ON_CONNECT_EXCEPTION_MESSAGE = "A client can't connect to the server!\n" + \
    "Make sure the server handles connections and doesn't stop after one client connected."

    FILES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server", "data")

    SAVED_FILES = dict()

    def generate(self):
        return [TestCase(stdin="exit", attach=self.ON_CONNECT_EXCEPTION_MESSAGE)]

    def test(self):
        pass

    @staticmethod
    def test_stop_server():
        server = TestedProgram("server")
        client = TestedProgram("client")

        server.start_in_background()
        client.start()
        client.execute("exit")

        # try {
#             Thread.sleep(200);
#         } catch (InterruptedException ignored) {}

        try:
            time.sleep(0.2)

        


