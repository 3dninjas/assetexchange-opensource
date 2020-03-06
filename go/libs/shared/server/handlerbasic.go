package server

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	common "github.com/assetninja/assetexchange/go/libs/shared/common"
)

func newBasicHandler(registry *Registry) func(res http.ResponseWriter, req *http.Request) {

	return func(res http.ResponseWriter, req *http.Request) {

		// error util
		reportError := func(message string, code int) {
			http.Error(res, message, code)
			log.Print(message)
		}

		// read request message
		reqMsg := common.RequestMessage{
			ID:      0,
			Address: nil,
			Input:   nil,
			Final:   true,
		}

		if err := json.NewDecoder(req.Body).Decode(&reqMsg); err != nil {
			reportError(
				fmt.Sprintf("could not parse http body: %v", err),
				http.StatusBadRequest)
			return
		}

		if reqMsg.Address == nil {
			reportError("address not given", http.StatusBadRequest)
			return
		}

		if reqMsg.Final != true {
			reportError("request needs to be final", http.StatusBadRequest)
			return
		}

		// call the function
		resOutput, resError := registry.callBasicFunc(reqMsg.GetService(), reqMsg.GetFunction(), reqMsg.Input)

		// create response message
		resMsg := common.ResponseMessage{
			ID:     reqMsg.ID,
			Output: resOutput,
			Error:  resError,
			Final:  true,
		}

		// write response
		if err := json.NewEncoder(res).Encode(resMsg); err != nil {
			reportError(
				fmt.Sprintf("could not generate response body: %v", err),
				http.StatusInternalServerError)
		}
	}
}
