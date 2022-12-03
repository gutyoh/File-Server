from hstest import CheckResult, StageTest
from hstest.test_case import TestCase
from collections import OrderedDict


class Clue:
    def __init__(self, output, feedback):
        self.output = output
        self.feedback = feedback


class FileServerTest(StageTest, Clue):

    def generate(self) -> list[TestCase]:
        test_cases = []
        inputs_with_clues = self.generate_inputs_with_clues()
        for inp, clue in inputs_with_clues.items():
            test_case = TestCase(stdin=inp, attach=clue)
            test_case.input = inp
            test_case.attach = clue
            test_cases.append(test_case)
        return test_cases

    def check(self, reply: str, clue: Clue) -> CheckResult:
        lines_wo_spaces = [line.strip() for line in reply.strip().split("\n") if line.strip() != ""]

        reply = "\n".join(lines_wo_spaces)

        return CheckResult(reply == clue.output, clue.feedback)

    @staticmethod
    def generate_inputs_with_clues() -> OrderedDict:
        inputs_with_clues = OrderedDict()

        # Test cases to check add() method
        # 1
        output = "The file file1 added successfully"
        feedback = "Failed to add file1. The answer to command \"add file1\" should be " + \
                   "\"The file file1 added successfully\\n\""

        inp = "add file1\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 2
        output = "The file file2 added successfully"
        feedback = "Wrong answer on action \"add\""

        inp = "add file2\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 3
        output = "The file file3 added successfully"
        feedback = "Wrong answer on action \"add\""

        inp = "add file3\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 4
        output = "The file file4 added successfully"
        feedback = "Failed to add file4. The answer to command \"add file4\" should be " + \
                   "\"The file file4 added successfully\\n\""

        inp = "add file4\n" + "exit";
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 5
        output = "The file file5 added successfully"
        feedback = "Wrong answer on action \"add\""

        inp = "add file5\n" + "exit";
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 6
        output = "The file file6 added successfully"
        feedback = "Wrong answer on action \"add\""

        inp = "add file6\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 7
        output = "The file file7 added successfully"
        feedback = "Wrong answer on action \"add\""

        inp = "add file7\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 8
        output = "The file file8 added successfully"
        feedback = "Failed to add file8. The answer to command \"add file8\" should be " + \
                   "\"The file file8 added successfully\\n\""

        inp = "add file8\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 9
        output = "The file file9 added successfully"
        feedback = "Failed to add file9. The answer to command \"add file9\" should be " + \
                   "\"The file file9 added successfully\\n\""

        inp = "add file9\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 10
        output = "The file file10 added successfully"
        feedback = "Wrong answer on action \"add\""

        inp = "add file10\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # Testing wrong names to add
        # 11
        output = "Cannot add the file fileWrong"
        feedback = "Wrong answer on action \"add\""

        inp = "add fileWrong\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 12
        output = "Cannot add the file file11";
        feedback = "Incorrect reaction to add file11. The answer to command \"add file11\" should be " + \
                   "\"Cannot add the file file11\\n\", as only filenames file1, file2..file10 " \
                   "are allowed at this stage."

        inp = "add file11\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 13
        output = "The file file1 added successfully\n" + "Cannot add the file file1"
        feedback = "Incorrect reaction to attempt of adding existing file. " \
                   "The answer to second command \"add file1\" should be " + \
                   "\"Cannot add the file file1\\n\", as only one file of such name could be added"

        inp = "add file1\n" + "add file1\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # Test cases to check get() method
        # 14
        output = "The file file1 not found"
        feedback = "Incorrect reaction to get file1. The answer to command \"get file1\" should be " + \
                   "\"The file file1 not found\\n\", if it was not added."

        inp = "get file1\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 15
        output = "The file file2 not found"
        feedback = "Wrong answer on action \"get\""

        inp = "get file2\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 16
        output = "The file file1 added successfully\n" + "The file file1 was sent"
        feedback = "Wrong answer on action \"get\""

        inp = "add file1\n" + "get file1\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 17
        output = "The file file2 added successfully\n" + "The file file2 was sent"
        feedback = "Wrong answer on action \"get\""

        inp = "add file2\n" + "get file2\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # Test cases to check delete() method
        # 18
        output = "The file file1 not found";
        feedback = "Incorrect reaction to delete file1. The answer to command \"delete file1\" should be " + \
                   "\"The file file1 not found\\n\", if it was not added."

        inp = "delete file1\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 19
        output = "The file file3 not found"
        feedback = "Wrong answer on action \"delete\""

        inp = "delete file3\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 20
        output = "The file file1 added successfully\n" + "The file file1 was deleted"
        feedback = "Wrong answer on action \"delete\""

        inp = "add file1\n" + "delete file1\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 21
        output = "The file file4 added successfully\n" + "The file file4 was deleted"
        feedback = "Incorrect reaction to delete file4. The answer to command \"delete file4\" should be " + \
                   "\"The file file4 was deleted\\n\", if it was added before."

        inp = "add file4\n" + "delete file4\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 22
        output = "The file file1 added successfully\n" + "The file file1 was deleted\n" + "The file file1 not found"
        feedback = "Incorrect reaction to delete file1. The answer to command \"delete file1\" should be " + \
                   "\"The file file1 not found\", if it was deleted before."

        inp = "add file1\n" + "delete file1\n" + "get file1\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # 23
        output = "The file file1 added successfully\n" + "The file file1 was deleted\n" + \
                 "The file file1 added successfully"
        feedback = "Wrong answer on action \"delete\""

        inp = "add file1\n" + "delete file1\n" + "add file1\n" + "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        # Test case to check exit()
        # 24
        output = ""
        feedback = "Incorrect reaction to exit. The reaction to command \"exit\" should be " + \
                   "the end of the Server execution."

        inp = "exit"
        clue = Clue(output, feedback)
        inputs_with_clues[inp] = clue

        return inputs_with_clues


if __name__ == '__main__':
    FileServerTest().run_tests()
