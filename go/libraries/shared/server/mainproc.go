package server

import (
	"log"
	"net/http"
	"os"
	"os/signal"
)

// MainProc is a main routine for rpc server processes
func MainProc(category string, typex string, registry *Registry, appHandler map[string]http.Handler) {

	// create server
	server, err := registry.NewServer(category, typex, appHandler)
	if err != nil {
		log.Printf("could not start rpc server [%v]", err)
		return
	}

	log.Printf("using address: http://localhost:%d/", server.Address.Port)

	// install stop signal channel
	stopChan := make(chan os.Signal, 2)
	signal.Notify(stopChan, os.Interrupt, os.Kill)

	// wait for stop signal or stopped event of server
	select {
	case <-stopChan:
		log.Printf("stop signal received...")
		break

	case err = <-server.StoppedEvent:
		if err != nil {
			log.Printf("rpc server stopped unexpected [%v]", err)
		}
	}

	// shutdown rpc server gracefully
	if err = server.Unpublish(); err != nil {
		log.Printf("could not shutdown rpc server gracefully [%v]", err)
	}

	// we are done now!
	log.Printf("exiting now... bye!")
}
