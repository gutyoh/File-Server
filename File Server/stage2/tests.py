import time
from hstest import TestedProgram, CheckResult, StageTest, dynamic_test


class FileServerTest(StageTest):
    @dynamic_test
    def test_1(self) -> CheckResult:

        server = TestedProgram("server")
        client = TestedProgram("client")
        server.set_return_output_after_execution(True)

        server.start_in_background()

        time.sleep(1)
        server_output = server.get_output().strip()

        server_started_message = "Server started!"
        if server_output != server_started_message:
            return CheckResult.wrong(f"Server output should be \"" + server_started_message + "\" until the client "
                                                                                              f"connects!")

        client_output = client.start().strip()
        server_output = server.get_output().strip()

        if client_output == "":
            return CheckResult.wrong(f"Client output shouldn't be empty!")

        if server_output == server_started_message:
            return CheckResult.wrong(f"After the client connects to the server you should output the received data!")

        if not server_output.__contains__("Received: Give me everything you have!"):
            return CheckResult.wrong(f"Server output should contain \"Received: Give me everything you have!\"")

        if not server_output.__contains__("Sent: All files were sent!"):
            return CheckResult.wrong("Server output should contain \"Sent: All files were sent!\"")

        if server_output.index("Sent: All files were sent!") < server_output.index(
                "Received: Give me everything you have!"):
            return CheckResult.wrong("The server should print \"Sent: All files were sent!\" only after " +
                                     "\"Received: Give me everything you have!\" was printed!")

        if not client_output.__contains__("Sent: Give me everything you have!"):
            return CheckResult.wrong("Client output should contain \"Sent: Give me everything you have!\"")

        if not client_output.__contains__("Received: All files were sent!"):
            return CheckResult.wrong("Client output should contain \"Received: All files were sent!\"")

        if client_output.index("Received: All files were sent!") < client_output.index(
                "Sent: Give me everything you have!"):
            return CheckResult.wrong("The client should print \"Received: All files were sent!\" only after " +
                                     "\"Sent: Give me everything you have!\" was printed!")

        return CheckResult.correct()


if __name__ == '__main__':
    FileServerTest().run_tests()
