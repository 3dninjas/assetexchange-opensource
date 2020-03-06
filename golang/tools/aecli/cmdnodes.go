package main

import (
	"bytes"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"

	client "github.com/assetninja/assetexchange/golang/libraries/shared/client"

	"github.com/olekukonko/tablewriter"
)

func cmdNodes(showInfo bool) {
	// node lookup
	nodes, errs := client.LookupNodes()
	if len(errs) > 0 {
		log.Printf("the following errors occured:")
		for err := range errs {
			log.Printf("- %v", err)
		}
	}

	// prepare table
	table := tablewriter.NewWriter(os.Stdout)
	table.SetHeader([]string{"Port / PID", "Property"})
	table.SetAlignment(tablewriter.ALIGN_LEFT)
	table.SetAutoWrapText(false)

	// add data
	for _, node := range nodes {

		table.Append([]string{strconv.Itoa(node.Port) + " / " + strconv.Itoa(node.Pid), "Classification"})
		table.Append([]string{"", "  - Category: " + node.Category})
		table.Append([]string{"", "  - Type: " + node.Type})

		if len(node.Services) > 0 {
			table.Append([]string{"", "Services"})
			for _, serviceName := range node.Services {
				table.Append([]string{"", "  - " + serviceName})
			}
		}

		if showInfo && len(node.Info) > 0 {
			table.Append([]string{"", "Info"})

			subTableBuf := new(bytes.Buffer)
			subTable := tablewriter.NewWriter(subTableBuf)
			subTable.SetAlignment(tablewriter.ALIGN_LEFT)
			subTable.SetAutoWrapText(false)
			subTable.SetBorder(false)

			infoProps := make([]string, 0)
			for prop := range node.Info {
				infoProps = append(infoProps, prop)
			}
			sort.Strings(infoProps)

			for _, prop := range infoProps {
				val := node.Info[prop]
				subTable.Append([]string{"- " + prop, fmt.Sprintf("%v", val)})
			}

			subTable.Render()
			table.Append([]string{"", subTableBuf.String()})
		}

		table.Append([]string{"", ""})
	}

	// render table
	table.Render()
}
