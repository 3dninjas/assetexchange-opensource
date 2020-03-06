package server

// Registry represents a function registry
type Registry struct {
	services map[string]interface{}
}

// NewRegistry creates a new registry object
func NewRegistry() *Registry {
	return &Registry{
		services: make(map[string]interface{}),
	}
}

// GetServiceNames returns all service names
func (reg *Registry) GetServiceNames() []string {
	names := make([]string, 0, len(reg.services))
	for name := range reg.services {
		names = append(names, name)
	}
	return names
}

// AddService adds an service interface to the registry
func (reg *Registry) AddService(name string, service interface{}) {
	reg.services[name] = service
}
