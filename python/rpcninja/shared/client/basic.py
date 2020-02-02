import urllib.request
import json

def call_basic_func(port, service, function, input, timeout):

    # prepare url
    url = "http://127.0.0.1:" + str(port) + "/.rpc/basic"

    # prepare timeout
    if timeout == 0:
        timeout = 10

    # prepare request message
    reqMsg = {
        'id': 0,
        'address': service + '.' + function,
        'input': input,
        'final': True
    }
    reqMsgByte = json.dumps(reqMsg).encode('utf8')

    # execute request
    req = urllib.request.Request(
        url, data=reqMsgByte, method="POST",
        headers={'content-type': 'application/json'}
    )

    # read response message
    res = urllib.request.urlopen(req, timeout=timeout)
    resMsg = json.loads(res.read().decode('utf-8'))

    # raise error if one occured
    if resMsg['error'] is not None:
        raise RuntimeError(resMsg['error'])

    return resMsg['output']
