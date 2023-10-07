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
	"sync"
)

const (
	serverDataPath = "./server/data/"
)

var (
	fileMutex    sync.Mutex
	fileID       int
	fileIDtoName = make(map[int]string)
	fileNametoID = make(map[string]int)
)

func handleConnection(conn net.Conn) {
	defer conn.Close()

	reader := bufio.NewReader(conn)
	writer := bufio.NewWriter(conn)

	for {
		action, err := reader.ReadString('\n')
		if err != nil {
			return
		}

		action = strings.TrimSpace(action)

		switch action {
		case "PUT":
			handlePut(reader, writer)
		case "GET":
			handleGet(reader, writer)
		case "DELETE":
			handleDelete(reader, writer)
		case "exit":
			os.Exit(0)
		default:
			writer.WriteString("Unknown action\n")
			writer.Flush()
		}
	}
}

func handlePut(reader *bufio.Reader, writer *bufio.Writer) {
	fileName, err := reader.ReadString('\n')
	if err != nil {
		return
	}
	fileName = strings.TrimSpace(fileName)

	lengthStr, err := reader.ReadString('\n')
	if err != nil {
		return
	}
	length, _ := strconv.Atoi(strings.TrimSpace(lengthStr))

	content := make([]byte, length)
	_, err = io.ReadFull(reader, content)
	if err != nil {
		return
	}

	filePath := filepath.Join(serverDataPath, fileName)
	err = os.WriteFile(filePath, content, 0644)
	if err != nil {
		writer.WriteString("403\n")
		writer.Flush()
		return
	}

	fileMutex.Lock()
	fileID++
	fileIDtoName[fileID] = fileName
	fileNametoID[fileName] = fileID
	fileMutex.Unlock()

	writer.WriteString(fmt.Sprintf("200 %d\n", fileID))
	writer.Flush()
}

func handleGet(reader *bufio.Reader, writer *bufio.Writer) {
	by, err := reader.ReadString('\n')
	if err != nil {
		return
	}
	by = strings.TrimSpace(by)

	var filePath string
	if by == "BY_ID" {
		idStr, err := reader.ReadString('\n')
		if err != nil {
			return
		}
		id, _ := strconv.Atoi(strings.TrimSpace(idStr))
		fileMutex.Lock()
		fileName, exists := fileIDtoName[id]
		fileMutex.Unlock()
		if !exists {
			writer.WriteString("404\n")
			writer.Flush()
			return
		}
		filePath = filepath.Join(serverDataPath, fileName)
	} else if by == "BY_NAME" {
		fileName, err := reader.ReadString('\n')
		if err != nil {
			return
		}
		fileName = strings.TrimSpace(fileName)
		filePath = filepath.Join(serverDataPath, fileName)
	} else {
		writer.WriteString("Invalid method\n")
		writer.Flush()
		return
	}

	content, err := os.ReadFile(filePath)
	if err != nil {
		writer.WriteString("404\n")
		writer.Flush()
		return
	}

	writer.WriteString(fmt.Sprintf("200 %d\n", len(content)))
	writer.Write(content)
	writer.Flush()
}

func handleDelete(reader *bufio.Reader, writer *bufio.Writer) {
	by, err := reader.ReadString('\n')
	if err != nil {
		return
	}
	by = strings.TrimSpace(by)

	var filePath string
	if by == "BY_ID" {
		idStr, err := reader.ReadString('\n')
		if err != nil {
			return
		}
		id, _ := strconv.Atoi(strings.TrimSpace(idStr))
		fileMutex.Lock()
		fileName, exists := fileIDtoName[id]
		fileMutex.Unlock()
		if !exists {
			writer.WriteString("404\n")
			writer.Flush()
			return
		}
		filePath = filepath.Join(serverDataPath, fileName)
	} else if by == "BY_NAME" {
		fileName, err := reader.ReadString('\n')
		if err != nil {
			return
		}
		fileName = strings.TrimSpace(fileName)
		filePath = filepath.Join(serverDataPath, fileName)
	} else {
		writer.WriteString("Invalid method\n")
		writer.Flush()
		return
	}

	err = os.Remove(filePath)
	if err != nil {
		writer.WriteString("404\n")
		writer.Flush()
		return
	}
	writer.WriteString("200\n")
	writer.Flush()
}

func main() {
	ln, err := net.Listen("tcp", ":8080")
	if err != nil {
		panic(err)
	}
	fmt.Println("Server started!")

	for {
		conn, err := ln.Accept()
		if err != nil {
			panic(err)
		}

		go handleConnection(conn)
	}
}
