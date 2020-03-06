// NODE ONLY!

import { Channel } from 'queueable';
import WebSocket from 'ws';
import { getFunctionFromRequest, getServiceFromRequest, RequestMessage, ResponseMessage } from '../common';
import { spinFunc, yieldEvents } from '../utils/async';
import { lookupServiceFunc, Registry } from './registry';

export function newStreamHandler(registry: Registry): (client: WebSocket) => void {

  return (client: WebSocket) => {
    spinFunc(async () => {

      // bookkeeping
      const inputStreams = new Map<number, Channel<any>>();

      try {
        // handle incoming requests
        for await (const { data } of yieldEvents<{ data: string }>(client, 'message', 'close', 'error')) {

          // parse request message
          const reqMsg: RequestMessage = JSON.parse(data);

          // handle call initiation
          if (reqMsg.address !== undefined) {
            // prevent double use of call ids
            if (inputStreams.has(reqMsg.id)) {
              client.send(JSON.stringify(<ResponseMessage>{
                id: reqMsg.id,
                error: 'rpc call id already in use',
                final: true,
              }));
              continue;
            }
            try {
              // retrieve service function
              const serviceName = getServiceFromRequest(reqMsg)
              const funcName = getFunctionFromRequest(reqMsg)
              const [service, func] = lookupServiceFunc(registry, serviceName, funcName, 'stream');
              // execute function
              const inputStream = new Channel<any>();
              inputStreams.set(reqMsg.id, inputStream);
              const outputStream = func.call(service, inputStream);
              // spin off output stream converter
              spinFunc(async () => {
                try {
                  // forward output stream
                  for await (const output of outputStream) {
                    client.send(JSON.stringify(<ResponseMessage>{
                      id: reqMsg.id,
                      output: output,
                      final: false,
                    }));
                  }
                  // signal completion of call
                  client.send(JSON.stringify(<ResponseMessage>{
                    id: reqMsg.id,
                    final: true,
                  }));
                }
                catch (error) {
                  // forward errors
                  client.send(JSON.stringify(<ResponseMessage>{
                    id: reqMsg.id,
                    error: (error.message || error) + '',
                    final: true,
                  }));
                }
              });
            }
            catch (error) {
              client.send(JSON.stringify(<ResponseMessage>{
                id: reqMsg.id,
                error: (error.message || error) + '',
                final: true,
              }));
              continue;
            }
          }

          // handle input objects
          if (reqMsg.input !== undefined) {
            // check if call id exists
            const inputStream = inputStreams.get(reqMsg.id);
            if (!inputStream) {
              client.send(JSON.stringify(<ResponseMessage>{
                id: reqMsg.id,
                error: 'rpc call id not found',
                final: true,
              }));
              continue;
            }
            // forward data
            await inputStream.push(reqMsg.input);
          }

          // handle finalization of call
          if (reqMsg.final) {
            // check if call id exists
            const inputStream = inputStreams.get(reqMsg.id);
            if (!inputStream) {
              client.send(JSON.stringify(<ResponseMessage>{
                id: reqMsg.id,
                error: 'rpc call id not found',
                final: true,
              }));
              continue;
            }
            // closing input channel
            inputStream.push(undefined, true);
            inputStreams.delete(reqMsg.id);
          }
        }
      }
      finally {
        // cleanup
        if (inputStreams.size > 0) {
          console.warn('open rpc input streams detected, closing them now...');
          for (const inputStream of inputStreams.values()) {
            inputStream.push(undefined, true);
          }
          inputStreams.clear();
        }
      }

    });
  };
}
