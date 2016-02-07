package main

import "encoding/json"

import (
	"github.com/ARolek/jsonpipe"
)

type Message struct {
	Name string
	Body string
	Time int64
}

func main() {
	jsonpipe.Handle("MyAction", myHandler)
	jsonpipe.ListenAndServe(":8081")
}

func myHandler(data *json.RawMessage) (map[string]interface{}, error) {
	json.Unmarshal(data, reply)
	return reply
}
