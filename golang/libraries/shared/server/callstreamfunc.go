package server

import (
	"encoding/json"
	"fmt"
	"reflect"
)

func (reg *Registry) callStreamFunc(serviceName string, functionName string) (chan<- json.RawMessage, <-chan json.RawMessage, <-chan string) {

	// bail out routine during preparation stage
	bailOut := func(error string) (chan<- json.RawMessage, <-chan json.RawMessage, <-chan string) {
		// prepare input channel
		inputChannel := make(chan json.RawMessage)
		go func() {
			// discard any input
			for range inputChannel {
			}
		}()
		// prepare output channel
		outputChannel := make(chan json.RawMessage)
		close(outputChannel)
		// prepare error channel
		errorChannel := make(chan string, 1)
		errorChannel <- error
		close(errorChannel)
		// prepare input channel and return all prepared channels
		return inputChannel, outputChannel, errorChannel
	}

	// lookup service
	service, serviceFound := reg.services[serviceName]
	if !serviceFound {
		return bailOut(fmt.Sprintf("service %s not found", serviceName))
	}

	// lookup function
	function := reflect.ValueOf(service).MethodByName(functionName)
	if !function.IsValid() {
		return bailOut(fmt.Sprintf("function %s.%s not found", serviceName, functionName))
	}

	// check function input and output count
	functionType := function.Type()
	if functionType.NumIn() != 3 || functionType.NumOut() != 0 {
		return bailOut(fmt.Sprintf("function %s.%s should expect exactly 3 input and no output values", serviceName, functionName))
	}

	// retrieve input and output types
	inputType := functionType.In(0)
	outputType := functionType.In(1)
	errorType := functionType.In(2)

	// validate input and output types
	if !isChannelType(inputType, reflect.RecvDir) {
		return bailOut(fmt.Sprintf("function %s.%s should expect receiver channel as first parameter", serviceName, functionName))
	}

	if !isChannelType(outputType, reflect.SendDir) {
		return bailOut(fmt.Sprintf("function %s.%s should expect sender channel as second parameter", serviceName, functionName))
	}

	if !isErrorChannelType(errorType, reflect.SendDir) {
		return bailOut(fmt.Sprintf("function %s.%s should expect error sender channel as third parameter", serviceName, functionName))
	}

	// prepare outer channels
	outerInputChannel := make(chan json.RawMessage)
	outerOutputChannel := make(chan json.RawMessage)

	errorChannelPrimary := make(chan string)
	errorChannelInputConv := make(chan string)
	errorChannelOutputConv := make(chan string)
	outerErrorChannel := mergeStringChannels(errorChannelPrimary, errorChannelInputConv, errorChannelOutputConv)

	// prepare inner channels
	innerInputChannel := reflect.MakeChan(reflect.ChanOf(reflect.BothDir, inputType.Elem()), 0)
	innerOutputChannel := reflect.MakeChan(reflect.ChanOf(reflect.BothDir, outputType.Elem()), 0)
	innerErrorChannel := reflect.MakeChan(reflect.ChanOf(reflect.BothDir, errorType.Elem()), 0)

	// input converter
	go func() {
		for inputRaw := range outerInputChannel {
			inputObject := reflect.New(inputType.Elem())
			if err := json.Unmarshal(inputRaw, inputObject.Interface()); err != nil {
				errorChannelInputConv <- err.Error()
				continue
			}
			innerInputChannel.Send(inputObject.Elem())
		}
		innerInputChannel.Close()
		close(errorChannelInputConv)
	}()

	// output converter
	go func() {
		for {
			outputObject, ok := innerOutputChannel.Recv()
			if !ok {
				break
			}
			outputRaw, err := json.Marshal(outputObject.Interface())
			if err != nil {
				errorChannelOutputConv <- err.Error()
				continue
			}
			outerOutputChannel <- outputRaw
		}
		close(outerOutputChannel)
		close(errorChannelOutputConv)
	}()

	// error converter
	go func() {
		for {
			errorObject, ok := innerErrorChannel.Recv()
			if !ok {
				break
			}
			errorChannelPrimary <- errorObject.Interface().(error).Error()
		}
		close(errorChannelPrimary)
	}()

	// call function
	go func() {
		function.Call([]reflect.Value{
			innerInputChannel,
			innerOutputChannel,
			innerErrorChannel,
		})
	}()

	// done
	return outerInputChannel, outerOutputChannel, outerErrorChannel
}
