package client

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"
	"time"

	common "github.com/3dninjas/assetexchange/go/libs/shared/common"
)

// CallBasicFunc executes a complete rpc call with single input and single output via HTTP
func CallBasicFunc(port int, service string, function string, input interface{}, output interface{}, timeout time.Duration) error {

	url := "http://127.0.0.1:" + strconv.Itoa(port) + "/.assetexchange/basic"

	if timeout == 0 {
		timeout = 10 * time.Second
	}

	inputRaw, err := json.Marshal(input)
	if err != nil {
		return fmt.Errorf("could not marshal input [%v]", err)
	}

	reqMsg := common.CreateCallRequest(0, service, function, inputRaw, true)

	reqMsgByte, err := json.Marshal(reqMsg)
	if err != nil {
		return fmt.Errorf("could not marshall request message [%v]", err)
	}

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(reqMsgByte))
	if err != nil {
		return fmt.Errorf("could not create request [%v]", err)
	}

	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{Timeout: timeout}
	res, err := client.Do(req)
	if err != nil {
		return fmt.Errorf("could not execute request [%v]", err)
	}
	defer res.Body.Close()

	resMsg := common.ResponseMessage{}
	if err := json.NewDecoder(res.Body).Decode(&resMsg); err != nil {
		return fmt.Errorf("could not parse response [%v]", err)
	}

	if resMsg.HasError() {
		return fmt.Errorf("rpc call failed [%s]", *resMsg.Error)
	}

	if resMsg.HasOutput() {
		return json.Unmarshal(resMsg.Output, output)
	}

	return nil
}
