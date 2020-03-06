// NODE ONLY!

import cors from 'cors';
import express from 'express';
import fs from 'fs';
import http from 'http';
import net from 'net';
import process from 'process';
import ws from 'ws';
import { lookupServiceEntryPath, NodeInfo } from '../common';
import { newBasicHandler } from './handlerbasic';
import { newStreamHandler } from './handlerstream';
import { Registry, ServiceOnStart } from './registry';

export type AssetExchangeServer = {
  address: net.AddressInfo
  _httpServer: http.Server
  _httpConnections: Set<net.Socket>
  _regFile: string
}

export async function newServer(registry: Registry, category: string, type: string): Promise<AssetExchangeServer> {

  // prepare server and app
  const httpApp = express();
  const httpServer = http.createServer(httpApp);
  const wsApp = new ws.Server({ server: httpServer, path: '/.assetexchange/stream' });

  // apply some standard middlewares
  httpApp.use(cors());
  httpApp.use(express.json());

  // create handler
  wsApp.on('connection', newStreamHandler(registry));
  httpApp.all('/.assetexchange/basic', newBasicHandler(registry));

  // add connection tracking
  const connections = new Set<net.Socket>();
  httpServer.on('connection', (socket) => {
    connections.add(socket);
    socket.on('close', () => {
      connections.delete(socket);
    });
  });

  // start listening
  await new Promise<http.Server>((resolve, reject) => {
    function onError(error: any) {
      httpServer.off('error', onError);
      reject(error);
    }
    httpServer.on('error', onError);
    httpServer.listen(0, '127.0.0.1', () => {
      httpServer.off('error', onError);
      resolve();
    });
  });

  const address = httpServer.address() as net.AddressInfo;

  // run on start event
  for (const serviceName of Object.keys(registry)) {
    registry[serviceName][ServiceOnStart]?.call(registry[serviceName], address);
  }

  // prepare node info
  const nodeInfo: NodeInfo = {
    category: category,
    type: type,
    pid: process.pid,
    port: address.port,
    protocols: ['basic', 'stream'],
    info: {},
    services: Object.keys(registry),
  };

  // write node info
  const regFile = lookupServiceEntryPath(category, type, process.pid);
  await fs.promises.writeFile(regFile, JSON.stringify(nodeInfo, null, 2), 'utf8');

  // done
  return {
    address: address,
    _httpServer: httpServer,
    _httpConnections: connections,
    _regFile: regFile,
  };
}

export async function shutdownServer(server: AssetExchangeServer): Promise<void> {

  // remove registration
  try {
    await fs.promises.unlink(server._regFile);
  }
  catch (err) {
    console.warn('could not remove registration file', err);
  }

  // stop listening
  await new Promise((resolve, reject) => {

    // if there are still connections after timeout occured, close them forcefully
    let timeoutHandle: NodeJS.Timeout | null = setTimeout(() => {
      timeoutHandle = null;
      if (server._httpConnections.size > 0) {
        console.warn('close pending connections forcefully...')
        for (const connection of server._httpConnections) {
          try {
            connection.destroy();
          }
          catch (err) {
            console.warn(err);
          }
        }
      }
    }, 10 * 1000);

    // stop listening and return once all connections are closed
    server._httpServer.close(error => {
      if (timeoutHandle != null) {
        clearTimeout(timeoutHandle);
      }
      if (error) {
        return reject(error);
      }
      return resolve();
    })
  });
}
