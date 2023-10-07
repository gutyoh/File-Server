package main

import (
	"bufio"
	"fmt"
	"io"
	"net"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

const (
	clientDataPath = "./client/data/"
)

func main() {
	conn, err := net.Dial("tcp", "localhost:8080")
	if err != nil {
		panic(err)
	}
	defer conn.Close()

	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(conn)

	for {
		fmt.Println("Enter action (1 - get a file, 2 - save a file, 3 - delete a file):")
		action, _ := reader.ReadString('\n')
		action = strings.TrimSpace(action)

		switch action {
		case "1":
			handleClientGet(reader, writer, conn)
		case "2":
			handleClientPut(reader, writer, conn)
		case "3":
			handleClientDelete(reader, writer, conn)
		case "exit":
			writer.WriteString("exit\n")
			writer.Flush()
			return
		default:
			fmt.Println("Unknown action.")
		}
	}
}

func handleClientPut(reader *bufio.Reader, writer *bufio.Writer, conn net.Conn) {
	fmt.Println("Enter name of the file:")
	fileName, _ := reader.ReadString('\n')
	fileName = strings.TrimSpace(fileName)

	content, err := os.ReadFile(filepath.Join(clientDataPath, fileName))
	if err != nil {
		fmt.Println("Error reading file:", err)
		return
	}

	fmt.Println("Enter name of the file to be saved on server:")
	newFileName, _ := reader.ReadString('\n')
	newFileName = strings.TrimSpace(newFileName)
	if newFileName == "" {
		newFileName = fileName
	}

	writer.WriteString("PUT\n")
	writer.WriteString(newFileName + "\n")
	writer.WriteString(fmt.Sprintf("%d\n", len(content)))
	writer.Write(content)
	writer.Flush()

	fmt.Println("The request was sent.")

	response, _ := bufio.NewReader(conn).ReadString('\n')
	response = strings.TrimSpace(response)
	if strings.HasPrefix(response, "200") {
		id := strings.Split(response, " ")[1]
		fmt.Printf("Response says that file is saved! ID = %s\n", id)
	} else {
		fmt.Println("Failed to save the file.")
	}
}

func handleClientGet(reader *bufio.Reader, writer *bufio.Writer, conn net.Conn) {
	fmt.Println("Do you want to get the file by name or by id (1 - name, 2 - id):")
	by, _ := reader.ReadString('\n')
	by = strings.TrimSpace(by)

	if by == "1" {
		writer.WriteString("GET\nBY_NAME\n")
		fmt.Println("Enter name:")
		name, _ := reader.ReadString('\n')
		writer.WriteString(name)
	} else if by == "2" {
		writer.WriteString("GET\nBY_ID\n")
		fmt.Println("Enter id:")
		id, _ := reader.ReadString('\n')
		writer.WriteString(id)
	} else {
		fmt.Println("Invalid choice.")
		return
	}
	writer.Flush()

	fmt.Println("The request was sent.")

	response, _ := bufio.NewReader(conn).ReadString('\n')
	response = strings.TrimSpace(response)
	if strings.HasPrefix(response, "200") {
		length, _ := strconv.Atoi(strings.Split(response, " ")[1])
		content := make([]byte, length)
		_, err := io.ReadFull(bufio.NewReader(conn), content)
		if err != nil {
			fmt.Println("Error reading file content:", err)
			return
		}
		fmt.Println("The file was downloaded! Specify a name for it:")
		newFileName, _ := reader.ReadString('\n')
		newFileName = strings.TrimSpace(newFileName)

		err = os.WriteFile(filepath.Join(clientDataPath, newFileName), content, 0644)
		if err != nil {
			fmt.Println("Error saving the file:", err)
			return
		}
		fmt.Println("File saved on the hard drive!")
	} else {
		fmt.Println("Failed to get the file.")
	}
}

func handleClientDelete(reader *bufio.Reader, writer *bufio.Writer, conn net.Conn) {
	fmt.Println("Do you want to delete the file by name or by id (1 - name, 2 - id):")
	by, _ := reader.ReadString('\n')
	by = strings.TrimSpace(by)

	if by == "1" {
		writer.WriteString("DELETE\nBY_NAME\n")
		fmt.Println("Enter name:")
		name, _ := reader.ReadString('\n')
		writer.WriteString(name)
	} else if by == "2" {
		writer.WriteString("DELETE\nBY_ID\n")
		fmt.Println("Enter id:")
		id, _ := reader.ReadString('\n')
		writer.WriteString(id)
	} else {
		fmt.Println("Invalid choice.")
		return
	}
	writer.Flush()

	fmt.Println("The request was sent.")

	response, _ := bufio.NewReader(conn).ReadString('\n')
	response = strings.TrimSpace(response)
	if response == "200" {
		fmt.Println("The response says that this file was deleted successfully!")
	} else {
		fmt.Println("The response says that this file is not found!")
	}
}
