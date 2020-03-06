//go:generate rsrc -manifest windows.manifest -o resource_windows.syso

package main

import "os"

func main() {

	args := os.Args[1:]

	if len(args) >= 1 {
		if args[0] == "nodes" {
			cmdNodes(hasFlag(args[1:], "--show-info"))
		} else if args[0] == "rpc" {
			params := args[1:]
			if len(params) >= 5 {
				cmdRPCWithPortLookup(params[0] == "stream", params[1], params[2], params[3], params[4])
			} else if len(params) >= 4 {
				cmdRPC(params[0] == "stream", params[1], params[2], params[3])
			} else {
				cmdUnknown()
			}
		} else {
			cmdUnknown()
		}
	} else {
		cmdUnknown()
	}
}

func hasFlag(args []string, flag string) bool {
	for _, a := range args {
		if a == flag {
			return true
		}
	}
	return false
}
