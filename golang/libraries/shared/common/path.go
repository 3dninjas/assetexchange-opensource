package common

import (
	"os"
	"path"
	"strconv"
)

type CreateDirMode int

const (
	CreateDirModeAll = iota
	CreateDirModeParent
	CreateDirModeNone
)

func LookupAssetExchangePath(createDirMode CreateDirMode, paths ...string) (string, error) {

	// construct path
	homePath, err := os.UserHomeDir()
	if err != nil {
		return "", err
	}

	result := path.Join(append([]string{homePath, ".assetexchange"}, paths...)...)

	// create directories on request
	if createDirMode == CreateDirModeAll {
		err = os.MkdirAll(result, 0755)
		if err != nil {
			return "", err
		}
	} else if createDirMode == CreateDirModeParent {
		err = os.MkdirAll(path.Dir(result), 0755)
		if err != nil {
			return "", err
		}
	}

	return result, nil

}

// LookupServicesPath creates a path within the rpc registry and returns the normalized path
func LookupServicesPath(createDirMode CreateDirMode, parts ...string) (string, error) {
	return LookupAssetExchangePath(createDirMode, append([]string{"services"}, parts...)...)
}

// LookupServiceEntryPath returns the path to a registration file within the rpc registry
func LookupServiceEntryPath(category string, typex string, pid int) (string, error) {
	dir, err := LookupServicesPath(CreateDirModeAll, category, typex)
	if err != nil {
		return "", err
	}
	return path.Join(dir, strconv.Itoa(pid)), nil
}
