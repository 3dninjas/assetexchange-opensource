package main

import (
	"fmt"
	"os"
)

func cmdUnknown() {
	exe := os.Args[0]
	fmt.Printf("Usage:\n")
	fmt.Printf("$ %s nodes [--show-info]\n", exe)
	fmt.Printf("$ echo '{ ... }' | %s rpc basic|stream <port> <service> <function> | jq\n", exe)
	fmt.Printf("$ echo '{ ... }' | %s rpc basic|stream <category> <type> <service> <function> | jq\n", exe)
}
