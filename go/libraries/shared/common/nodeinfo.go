package common

// NodeInfo represents all node information available within the registry
type NodeInfo struct {
	Category  string                 `json:"category"`
	Type      string                 `json:"type"`
	Pid       int                    `json:"pid"`
	Port      int                    `json:"port"`
	Protocols []string               `json:"protocols"`
	Info      map[string]interface{} `json:"info"`
	Services  []string               `json:"services"`
}
