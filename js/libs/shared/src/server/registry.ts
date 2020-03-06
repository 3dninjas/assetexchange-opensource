// NODE ONLY!

import net from 'net';
import { RestrictedAsyncIterable } from '../utils/types';

// rpc function signatures
export type BasicFunc = (input: any) => Promise<any>;
export type StreamFunc = (inputStream: RestrictedAsyncIterable<any>) => RestrictedAsyncIterable<any>;

// service interface
export const ServiceData = Symbol();
export const ServiceOnStart = Symbol();

export interface Service {
  [ServiceOnStart]?: (address: net.AddressInfo) => void;
  [funcName: string]: BasicFunc | StreamFunc;
}

// registry interface
export type Registry = {
  [serviceName: string]: Service;
}

// service and function lookup
export function lookupServiceFunc(registry: Registry, serviceName: string, funcName: string, funcType: 'basic'): [Service, BasicFunc];
export function lookupServiceFunc(registry: Registry, serviceName: string, funcName: string, funcType: 'stream'): [Service, StreamFunc];

export function lookupServiceFunc(registry: Registry, serviceName: string, funcName: string, funcType: 'basic' | 'stream'): [Service, BasicFunc | StreamFunc] {

  // lookup service
  const service = registry[serviceName];
  if (!service) {
    throw new Error(`could not find service '${serviceName}'`);
  }

  // lookup function
  if (funcName.substr(0, 1) != funcName.substr(0, 1).toUpperCase()) {
    throw new Error(`invalid function name '${funcName}'`);
  }

  const func = service[funcName];
  if (!func || typeof func !== 'function') {
    throw new Error(`could not find service function '${funcName}'`);
  }

  if (funcType == 'basic') {
    if (func.length != 1) {
      throw new Error(`service function '${funcName}' is not a function according to basic protocol`);
    }
    return [service, func as BasicFunc];
  }

  if (func.length != 1) {
    throw new Error(`service function '${funcName}' is not a function according to stream protocol`);
  }
  return [service, func as StreamFunc];
}
