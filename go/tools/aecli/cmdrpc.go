package main

import (
	"encoding/json"
	"log"
	"os"
	"strconv"

	client "github.com/assetninja/assetexchange/go/libs/shared/client"
)

func cmdRPCWithPortLookup(useStream bool, category string, typex string, service string, function string) {

	port, err := client.LookupPort(category, typex)
	if err != nil {
		log.Printf("could not lookup port [%v]", err)
		return
	}

	cmdRPC(useStream, strconv.Itoa(port), service, function)
}

func cmdRPC(useStream bool, portStr string, service string, function string) {

	if useStream {
		log.Printf("rpc stream client not yet implemented... coming soon")
		return
	}

	port, err := strconv.Atoi(portStr)
	if err != nil {
		log.Printf("could not parse port string [%v]", err)
		return
	}

	var input interface{}
	err = json.NewDecoder(os.Stdin).Decode(&input)
	if err != nil {
		log.Printf("could not parse JSON from stdin [%v]", err)
		return
	}

	var output interface{}
	err = client.CallBasicFunc(port, service, function, input, &output, 0)
	if err != nil {
		log.Printf("could not execute rpc call [%v]", err)
		return
	}

	json.NewEncoder(os.Stdout).Encode(output)
}
