package server

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net"
	"net/http"
	"os"
	"reflect"
	"time"

	common "github.com/assetninja/assetexchange/go/libs/shared/common"
	"github.com/rs/cors"
)

// Server represents an rpc server
type Server struct {
	Address      *net.TCPAddr
	StoppedEvent <-chan error
	regFile      string
	httpServer   *http.Server
}

// NewServer creates a new rpc server for a specific registry
func (registry *Registry) NewServer(category string, typex string, appHandler map[string]http.Handler) (*Server, error) {

	stoppedEvent := make(chan error, 1)
	server := &Server{nil, stoppedEvent, "", nil}

	// create handler
	handler := http.NewServeMux()
	handler.HandleFunc("/.assetexchange/stream", newStreamHandler(registry))
	handler.HandleFunc("/.assetexchange/basic", newBasicHandler(registry))

	if appHandler != nil {
		for pattern, subHandler := range appHandler {
			handler.Handle(pattern, subHandler)
		}
	}

	// create listener and retrieve address
	listener, err := net.Listen("tcp", "localhost:0")
	if err != nil {
		return nil, fmt.Errorf("could not listen on free port [%v]", err)
	}

	server.Address = listener.Addr().(*net.TCPAddr)

	// send start event to services
	for _, serviceName := range registry.GetServiceNames() {
		service := registry.services[serviceName]
		eventFunc := reflect.ValueOf(service).MethodByName("OnServerStart")
		if eventFunc.IsValid() {
			eventFunc.Call([]reflect.Value{reflect.ValueOf(server.Address)})
		}
	}

	// create http server (with cors)
	server.httpServer = &http.Server{Handler: cors.Default().Handler(handler)}

	// prepare node info
	nodeInfo := common.NodeInfo{
		Category:  category,
		Type:      typex,
		Pid:       os.Getpid(),
		Port:      server.Address.Port,
		Protocols: []string{"basic", "stream"},
		Info:      make(map[string]interface{}, 0),
		Services:  registry.GetServiceNames(),
	}

	nodeInfoRaw, err := json.MarshalIndent(nodeInfo, "", "  ")
	if err != nil {
		return nil, fmt.Errorf("could not register rpc process [%v]", err)
	}

	// register node
	regFile, err := common.LookupServiceEntryPath(category, typex, os.Getpid())
	if err != nil {
		listener.Close()
		return nil, fmt.Errorf("could not register rpc process [%v]", err)
	}

	if err = ioutil.WriteFile(regFile, nodeInfoRaw, 0644); err != nil {
		listener.Close()
		return nil, fmt.Errorf("could not register rpc process [%v]", err)
	}

	server.regFile = regFile

	// serve http requests
	go func() {
		err = server.httpServer.Serve(listener)
		if err != nil {
			stoppedEvent <- fmt.Errorf("could not start http server [%v]", err)
		} else {
			stoppedEvent <- nil
		}
	}()

	return server, nil
}

// Unpublish stops the rpc server
func (server *Server) Unpublish() error {

	// remove registration file
	if err := os.Remove(server.regFile); err != nil {
		log.Printf("could not deregister rpc process [%v]", err)
	}

	// shutdown context
	shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer shutdownCancel()

	// shutdown http server gracefully
	if err := server.httpServer.Shutdown(shutdownCtx); err != nil {
		return fmt.Errorf("could not shutdown http server gracefully [%v]", err)
	}

	return nil
}
