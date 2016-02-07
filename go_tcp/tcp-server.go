package main

import "net"
import "fmt"
import "bufio"
import "strings"

func main() {
	fmt.Println("Launching server...")

	ln, _ := net.Listen("tcp", ":8081") // listen on all interfaces

	// accept connection on port
	conn, _ := ln.Accept()

	for {
		// will listen for message to process ending in newline (\n)
		message, _ := bufio.NewReader(conn).ReadString('\n')

		// output message received
		fmt.Print("Message Received:", string(message))

		// sample process for string received
		newmessage := strings.ToUpper(message)

		// send new string back to client

		conn.Write([]byte(newmessage + "\n"))

	}
} // See more at: https://systembash.com/a-simple-go-tcp-server-and-tcp-client/#sthash.4d2TFKuc.dpuf
