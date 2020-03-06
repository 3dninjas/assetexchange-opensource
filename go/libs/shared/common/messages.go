package common

import (
	"encoding/json"
	"strings"
)

// RequestMessage represents a certain request action within a function call cycle
type RequestMessage struct {
	ID      uint64          `json:"id"`
	Address *string         `json:"address"`
	Input   json.RawMessage `json:"input,omitempty"`
	Final   bool            `json:"final"`
}

// CreateCallRequest is a factory function for RequestMessage
func CreateCallRequest(id uint64, service string, function string, input json.RawMessage, final bool) RequestMessage {
	// create message
	address := strings.Join([]string{service, function}, ".")
	return RequestMessage{
		ID:      id,
		Address: &address,
		Input:   input,
		Final:   final,
	}
}

// IsCall returns true if request is a call initiation
func (msg *RequestMessage) IsCall() bool {
	return msg.Address != nil
}

// GetService extracts service name of address
func (msg *RequestMessage) GetService() string {
	parts := strings.Split(*msg.Address, ".")
	return strings.Join(parts[:len(parts)-1], ".")
}

// GetFunction extracts function name of address
func (msg *RequestMessage) GetFunction() string {
	parts := strings.Split(*msg.Address, ".")
	return parts[len(parts)-1]
}

// HasInput returns true if request contains input
func (msg *RequestMessage) HasInput() bool {
	return msg.Input != nil
}

// IsFinal returns true if request finalizes input stream of call
func (msg *RequestMessage) IsFinal() bool {
	return msg.Final
}

// ResponseMessage represents a certain response action within a function call cycle
type ResponseMessage struct {
	ID     uint64          `json:"id"`
	Output json.RawMessage `json:"output,omitempty"`
	Error  *string         `json:"error"`
	Final  bool            `json:"final"`
}

// CreateOutputResponse is a factory function for ResponseMessage
func CreateOutputResponse(id uint64, output json.RawMessage, final bool) ResponseMessage {
	// create message
	return ResponseMessage{
		ID:     id,
		Output: output,
		Error:  nil,
		Final:  final,
	}
}

// CreateErrorResponse is a factory function for ResponseMessage
func CreateErrorResponse(id uint64, error string, final bool) ResponseMessage {
	// create message
	return ResponseMessage{
		ID:     id,
		Output: nil,
		Error:  &error,
		Final:  final,
	}
}

// CreateFinalResponse is a factory function for ResponseMessage
func CreateFinalResponse(id uint64) ResponseMessage {
	// create message
	return ResponseMessage{
		ID:     id,
		Output: nil,
		Error:  nil,
		Final:  true,
	}
}

// HasOutput returns true if response contains output
func (msg *ResponseMessage) HasOutput() bool {
	return msg.Output != nil
}

// HasError returns true if response contains error
func (msg *ResponseMessage) HasError() bool {
	return msg.Error != nil
}

// IsFinal returns true if response finalizes output stream of call
func (msg *ResponseMessage) IsFinal() bool {
	return msg.Final
}
