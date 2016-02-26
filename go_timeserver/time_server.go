// time_server.go
// Just issue json formatted time on a given socket
package main

import (
	"encoding/json"
	"fmt"
	"net"
	"strconv"
	"time"
)

func main() {

	// listen on all interfaces
	ln, _ := net.Listen("tcp", "localhost:8081")

	// accept connection on port
	fmt.Println("Server ready, awaiting connection")
	conn, _ := ln.Accept()

	// Serve time
	fmt.Println("Server go at client")
	for {
		message := map[string]string{"reqId": "0", "time": strconv.Itoa(time.Now().Second())}
		fmt.Println("time issued")
		mByte, _ := json.Marshal(message)
		conn.Write(mByte)
		time.Sleep(1)
	}
}
