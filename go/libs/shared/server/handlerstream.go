package server

import (
	"encoding/json"
	"log"
	"net/http"
	"sync"

	common "github.com/assetninja/assetexchange/go/libs/shared/common"
	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool { return true },
}

func newStreamHandler(registry *Registry) func(res http.ResponseWriter, req *http.Request) {

	return func(res http.ResponseWriter, req *http.Request) {
		// upgrade http connection to websocket
		ws, err := upgrader.Upgrade(res, req, nil)
		if err != nil {
			log.Printf("websocket upgrade failed: %f", err)
			return
		}
		defer ws.Close()

		// create new rpc server
		reqChan := make(chan common.RequestMessage)
		resChan := make(chan common.ResponseMessage)

		newStreamTracker(registry).track(reqChan, resChan)

		// manage lifecycle of reader and writer
		var wg sync.WaitGroup
		wg.Add(2)

		// translate incoming websocket messages
		go func() {
			// receiver loop
			for {
				// read next websocket message
				_, reqRaw, err := ws.ReadMessage()
				if err != nil {
					log.Printf("could not read websocket message: %v", err)
					break
				}
				// unmarshal json
				reqMsg := common.RequestMessage{}
				if err := json.Unmarshal(reqRaw, &reqMsg); err != nil {
					log.Printf("could not parse websocket message: %v", err)
					continue
				}
				// pass to channel
				reqChan <- reqMsg
			}
			// close request channel for graceful shutdown
			close(reqChan)
			// signal completion
			wg.Done()
		}()

		// translate outgoing messages to websocket messages
		go func() {
			// sender loop
			for resMsg := range resChan {
				// marshal json
				resRaw, err := json.Marshal(resMsg)
				if err != nil {
					log.Printf("could not generate websocket message: %v", err)
					continue
				}
				// write to websocket
				err = ws.WriteMessage(websocket.TextMessage, resRaw)
				if err != nil {
					log.Printf("could not write websocket message: %v", err)
					break
				}
			}
			// consume pending messages for graceful shutdown
			for range resChan {
			}
			// signal completion
			wg.Done()
		}()

		// wait for completion of reader and writer
		wg.Wait()

		// close websocket will happen here automatically
	}
}
