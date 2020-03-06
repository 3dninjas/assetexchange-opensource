import { ResponseMessage } from '../common';
import { spinFunc, yieldEvents } from '../utils/async';
import { RestrictedAsyncIterable } from '../utils/types';

const WebSocket: typeof window.WebSocket = (window && window.WebSocket) || require('ws').default;

const connections = new Map<number, { ws: WebSocket, nextId: number }>();

function isWebSocketOK(ws: WebSocket) {
  return [WebSocket.CONNECTING, WebSocket.OPEN].indexOf(ws.readyState) !== -1;
}

function ensureWebSocketOK(ws: WebSocket) {
  if (!isWebSocketOK(ws)) {
    throw new Error("websocket is not ok");
  }
}

async function ensureWebSocketWritable(ws: WebSocket) {
  ensureWebSocketOK(ws);
  // apply some backpressure here
  while (ws.bufferedAmount > 0) {
    await new Promise((resolve) => setTimeout(resolve, 10));
    ensureWebSocketOK(ws);
  }
}

function waitForWebSocketToBeReady(ws: WebSocket): Promise<void> {
  return new Promise((resolve, reject) => {
    // check already marterialized states
    if (!isWebSocketOK(ws)) {
      return reject(new Error("websocket is closed"));
    }
    if (ws.readyState == WebSocket.OPEN) {
      return resolve();
    }
    // wait for close/error or open
    function onWebSocketClose(event: { reason: string }) {
      removeHandler();
      return reject(new Error(event.reason));
    }
    function onWebSocketOpen(_: {}) {
      removeHandler();
      return resolve();
    }
    function removeHandler() {
      ws.removeEventListener('close', onWebSocketClose);
      ws.removeEventListener('open', onWebSocketOpen);
    }
    ws.addEventListener('close', onWebSocketClose);
    ws.addEventListener('open', onWebSocketOpen);
  });
}

export async function* rpcCallStreamFunc<InputT, OutputT>(port: number, service: string, func: string, inputStream: AsyncIterable<InputT>): RestrictedAsyncIterable<OutputT> {

  // allocate websocket connection
  const connection = (() => {
    let connection = connections.get(port);

    if (!connection || !isWebSocketOK(connection.ws)) {
      const url = "ws://127.0.0.1:" + port + "/.assetexchange/stream";
      connection = {
        ws: new WebSocket(url),
        nextId: 0
      };
      connections.set(port, connection);
    }

    return connection;
  })();

  // allocate id
  const id = connection.nextId++;

  // spin off websocket writer
  spinFunc(async () => {
    // register function call
    await waitForWebSocketToBeReady(connection.ws);
    connection.ws.send(JSON.stringify({
      id: id,
      address: service + '.' + func,
      final: false,
    }));

    // forward input
    for await (const input of inputStream) {
      await ensureWebSocketWritable(connection.ws);
      connection.ws.send(JSON.stringify({
        id: id,
        input: input,
        final: false,
      }));
    }

    // finalize function call
    await ensureWebSocketWritable(connection.ws);
    connection.ws.send(JSON.stringify({
      id: id,
      final: true,
    }));
  });

  // reader
  if (!isWebSocketOK(connection.ws)) {
    throw new Error('websocket closed');
  }

  // read websocket messages
  for await (const { data } of yieldEvents<{ data: string }>(connection.ws, 'message', 'close', 'error')) {
    // check if messages is adsressed to us
    const resMsg: ResponseMessage = JSON.parse(data);
    if (resMsg.id == id) {
      // yield received output
      if (resMsg.output !== undefined) {
        yield resMsg.output;
      }
      // raise received errors
      if (resMsg.error) {
        throw new Error(resMsg.error);
      }
      // finalize function call
      if (resMsg.final) {
        return;
      }
    }
  }
}
