package server

import (
	"encoding/json"
	"fmt"
	"reflect"
)

func (reg *Registry) callBasicFunc(serviceName string, functionName string, inputRaw json.RawMessage) (json.RawMessage, *string) {
	// lookup service
	service, serviceFound := reg.services[serviceName]
	if !serviceFound {
		errStr := fmt.Sprintf("service %s not found", serviceName)
		return nil, &errStr
	}

	// lookup function
	function := reflect.ValueOf(service).MethodByName(functionName)
	if !function.IsValid() {
		errStr := fmt.Sprintf("function %s.%s not found", serviceName, functionName)
		return nil, &errStr
	}

	// check function input and output count
	functionType := function.Type()
	if functionType.NumIn() != 1 || functionType.NumOut() != 2 {
		errStr := fmt.Sprintf("function %s.%s should expect exactly one input and two output values", serviceName, functionName)
		return nil, &errStr
	}

	// retrieve input and output types
	inputType := functionType.In(0)
	errorType := functionType.Out(1)

	// validate input and output types
	if !isErrorType(errorType) {
		errStr := fmt.Sprintf("function %s.%s should return error type as first output", serviceName, functionName)
		return nil, &errStr
	}

	// convert input
	inputObject := reflect.New(inputType)
	if err := json.Unmarshal(inputRaw, inputObject.Interface()); err != nil {
		errStr := err.Error()
		return nil, &errStr
	}

	// call function
	result := function.Call([]reflect.Value{
		inputObject.Elem(),
	})

	// convert error
	if !result[1].IsNil() {
		errStr := result[1].Interface().(error).Error()
		return nil, &errStr
	}

	// convert output
	outputRaw, err := json.Marshal(result[0].Interface())
	if err != nil {
		errStr := err.Error()
		return nil, &errStr
	}

	// done
	return outputRaw, nil
}
