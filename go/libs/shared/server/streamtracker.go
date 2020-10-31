package server

import (
	"encoding/json"
	"sync"

	common "github.com/3dninjas/assetexchange/go/libs/shared/common"
)

type streamTracker struct {
	registry *Registry
	active   bool
}

func newStreamTracker(registry *Registry) *streamTracker {
	return &streamTracker{
		registry: registry,
		active:   false,
	}
}

func (tracker *streamTracker) track(reqChan <-chan common.RequestMessage, resChan chan<- common.ResponseMessage) {

	// prevent double execution
	if tracker.active {
		panic("rpc stream tracker is already active")
	}
	tracker.active = true

	// bookkeeping
	inputChannels := make(map[uint64]chan<- json.RawMessage)
	var outputWaitGroup sync.WaitGroup

	// handle incoming requests
	handleReq := func(r common.RequestMessage) {
		// handle call initiation
		if r.IsCall() {
			// prevent double use of call ids
			if _, exists := inputChannels[r.ID]; exists {
				resChan <- common.CreateErrorResponse(r.ID, "rpc call id already in use", true)
				return
			}
			// check arguments
			if r.Address == nil {
				resChan <- common.CreateErrorResponse(r.ID, "rpc call address is missing", true)
				return
			}
			// execute function
			inputChannel, outputChannel, errorChannel := tracker.registry.callStreamFunc(r.GetService(), r.GetFunction())
			inputChannels[r.ID] = inputChannel
			// transform output and error
			outputWaitGroup.Add(1)
			go func() {
				// consume output and error channels
				for {
					select {
					case outputRaw, ok := <-outputChannel: // propagate output object
						if ok {
							resChan <- common.CreateOutputResponse(r.ID, outputRaw, false)
						} else {
							outputChannel = nil
						}
					case errorRaw, ok := <-errorChannel: // propagate error object
						if ok {
							resChan <- common.CreateErrorResponse(r.ID, errorRaw, false)
						} else {
							errorChannel = nil
						}
					}
					// stop read loop once both channels are closed
					if outputChannel == nil && errorChannel == nil {
						break
					}
				}
				// signal completion of call
				resChan <- common.CreateFinalResponse(r.ID)
				outputWaitGroup.Done()
			}()
		}

		// handle input objects
		if r.HasInput() {
			// check if call id exists
			if _, exists := inputChannels[r.ID]; !exists {
				resChan <- common.CreateErrorResponse(r.ID, "rpc call id not found", true)
				return
			}
			// forward data
			inputChannels[r.ID] <- r.Input
		}

		// handle finalization of call
		if r.IsFinal() {
			// check if call id exists
			if _, exists := inputChannels[r.ID]; !exists {
				resChan <- common.CreateErrorResponse(r.ID, "rpc call id not found", true)
				return
			}
			// closing input channel
			close(inputChannels[r.ID])
			delete(inputChannels, r.ID)
		}
	}

	// worker loop
	go func() {
		// process all request messages
		for reqMsg := range reqChan {
			handleReq(reqMsg)
		}

		// close all input channels of running calls
		for _, c := range inputChannels {
			close(c)
		}
		inputChannels = make(map[uint64]chan<- json.RawMessage)

		// wait for completion of still running calls
		outputWaitGroup.Wait()

		// close response channel for proper shutdown
		close(resChan)

		// mark as stopped
		tracker.active = false
	}()
}
