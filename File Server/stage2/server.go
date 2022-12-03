package main

import (
	"bufio"
	"fmt"
	"net"
	"strings"
)

func main() {
	l, err := net.Listen("tcp", "127.0.0.1:12345")
	if err != nil {
		fmt.Println(err)
		return
	}
	defer l.Close()
	fmt.Println("Server started!")

	c, err := l.Accept()
	if err != nil {
		fmt.Println(err)
		return
	}

	for {
		netData, err := bufio.NewReader(c).ReadString('\n')
		if err != nil {
			fmt.Println(err)
			return
		}
		if strings.TrimSpace(netData) == "STOP" {
			fmt.Println("Exiting TCP server!")
			return
		}

		fmt.Println("Received:", strings.TrimSuffix(netData, "\n"))

		sentMessage := "All files were sent!"
		fmt.Println("Sent:", sentMessage)
		c.Write([]byte(sentMessage + "\n"))
		return
	}
}
