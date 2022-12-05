package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strings"
)

type Storage struct {
	files map[string]bool
}

func (s *Storage) Add(file string) bool {
	if s.CheckFileName(file) && !contains(s.files, file) && len(s.files) < 10 {
		s.files[file] = true
		return true
	}
	return false
}

func (s *Storage) Get(file string) bool {
	return s.CheckFileName(file) && contains(s.files, file)
}

func (s *Storage) CheckFileName(filename string) bool {
	matched, _ := regexp.MatchString(`^file[1-9]$|^file10$`, filename)
	return matched
}

func (s *Storage) Delete(file string) bool {
	if s.CheckFileName(file) && contains(s.files, file) {
		delete(s.files, file)
		return true
	}
	return false
}

func contains(m map[string]bool, key string) bool {
	_, ok := m[key]
	return ok
}

func main() {
	s := Storage{files: make(map[string]bool)}

	scanner := bufio.NewScanner(os.Stdin)

	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			break
		}
		tokens := strings.Split(line, " ")
		command := tokens[0]

		if command == "exit" {
			break
		}

		filename := tokens[1]

		switch command {
		case "add":
			if s.Add(filename) {
				fmt.Printf("The file %s added successfully\n", filename)
			} else {
				fmt.Printf("Cannot add the file %s\n", filename)
			}
		case "get":
			if s.Get(filename) {
				fmt.Printf("The file %s was sent\n", filename)
			} else {
				fmt.Printf("The file %s not found\n", filename)
			}
		case "delete":
			if s.Delete(filename) {
				fmt.Printf("The file %s was deleted\n", filename)
			} else {
				fmt.Printf("The file %s not found\n", filename)
			}
		}
	}
}
