import re


def check_file_name(filename):
    # match file1 to file10 only
    return re.match(r"^file[1-9]$|^file10$", filename)


def delete(file):
    if check_file_name(file) and file in Storage.files:
        Storage.files.remove(file)
        return True
    return False


def get(file):
    return check_file_name(file) and file in Storage.files


def add(file):
    if check_file_name(file) and file not in Storage.files:
        # add file to storage
        Storage.files.add(file)
        return True
    return False


class Storage:
    files = set()

    def __init__(self):
        self.files = set()


def main():
    while True:
        line = input()
        if line == "":
            break

        tokens = line.split(" ")
        command = tokens[0]

        if command == "exit":
            break

        filename = tokens[1]

        if command == "add":
            if add(filename):
                print("The file", filename, "added successfully")
            else:
                print("Cannot add the file", filename)
        elif command == "get":
            if get(filename):
                print("The file", filename, "was sent")
            else:
                print("The file", filename, "not found")
        elif command == "delete":
            if delete(filename):
                print("The file", filename, "was deleted")
            else:
                print("The file", filename, "not found")

if __name__ == '__main__':
    main()