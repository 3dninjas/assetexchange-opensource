package client

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"runtime"
	"sort"
	"strconv"
	"strings"
	"syscall"
	"time"

	common "github.com/assetninja/assetexchange/go/libs/shared/common"
)

// LookupNodes retrieves all currently registered nodes
func LookupNodes() ([]common.NodeInfo, []error) {

	for retry := 0; ; retry++ {

		result := make([]common.NodeInfo, 0)
		errors := make([]error, 0)

		regDir, err := common.LookupServicesPath(common.CreateDirModeAll)
		if err != nil {
			errors = append(errors, err)
			return result, errors
		}

		err = filepath.Walk(regDir,
			func(entryPath string, info os.FileInfo, err error) error {
				// assert we have correct paths (who knows what can happen)
				if !strings.HasPrefix(strings.ReplaceAll(entryPath, "\\", "/"), strings.ReplaceAll(regDir, "\\", "/")) {
					panic("unexpected entry path during directory walk")
				}
				// ignore any errors
				if err != nil {
					errors = append(errors, err)
					return nil
				}
				// ignore dirs, we read files only
				if info.IsDir() {
					return nil
				}
				// extract pid from filename
				pidStr := filepath.Base(entryPath)
				pid, err := strconv.Atoi(string(pidStr))
				if err != nil {
					// remove non-pid file
					os.Remove(entryPath)
					return nil
				}
				// check if process is still running
				process, err := os.FindProcess(pid)
				if err != nil {
					// remove stale pid file
					os.Remove(entryPath)
					return nil
				} else if runtime.GOOS != "windows" {
					err = process.Signal(syscall.Signal(0))
					if err != nil {
						// remove stale pid file
						os.Remove(entryPath)
						return nil
					}
				}
				// read node info
				nodeInfoRaw, err := ioutil.ReadFile(entryPath)
				if err != nil {
					errors = append(errors, err)
					return nil
				}
				var nodeInfo common.NodeInfo
				err = json.Unmarshal(nodeInfoRaw, &nodeInfo)
				if err != nil {
					errors = append(errors, err)
					return nil
				}
				// append port spec
				result = append(result, nodeInfo)
				return nil
			})
		if err != nil {
			errors = append(errors, err)
		}

		if len(errors) > 0 && retry < 4 {
			time.Sleep(25 * time.Millisecond)
			continue
		}

		sort.SliceStable(result, func(i, j int) bool {
			return result[i].Port < result[j].Port
		})

		return result, errors
	}
}

// LookupPort retrieves a port for a specific category and type of service
func LookupPort(category string, typex string) (int, error) {
	nodes, _ := LookupNodes()
	for _, node := range nodes {
		if node.Category == category && node.Type == typex {
			return node.Port, nil
		}
	}
	return 0, fmt.Errorf("could not find port")
}
