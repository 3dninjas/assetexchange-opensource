import { RestrictedAsyncIterable } from './types';

interface NodeEventEmitterInterface {
  addListener(event: string, listener: (...args: any[]) => void): unknown;
  removeListener(event: string, listener: (...args: any[]) => void): unknown;
}

interface DOMEventEmitterInterface {
  addEventListener(event: string, listener: (...args: any[]) => void): unknown;
  removeEventListener(event: string, listener: (...args: any[]) => void): unknown;
}

export type EventEmitterInterface = NodeEventEmitterInterface | DOMEventEmitterInterface

function isDOMEventEmitter(emitter: EventEmitterInterface): emitter is DOMEventEmitterInterface {
  return (emitter as DOMEventEmitterInterface).addEventListener !== undefined;
}

export async function* yieldEvents<OutputT>(emitter: EventEmitterInterface, nextEvent: string, endEvent?: string, errorEvent?: string): RestrictedAsyncIterable<OutputT> {

  let curResolve: (() => void) | undefined = undefined;
  const curValues: OutputT[] = [];
  let curError: any | undefined = undefined;
  let completed = false;

  function tryResolve() {
    if (curResolve !== undefined) {
      const resolve = curResolve;
      curResolve = undefined;
      resolve();
    }
  }

  function onNext(value: OutputT) {
    curValues.push(value);
    tryResolve();
  }

  function onEnd() {
    completed = true;
    tryResolve();
  }

  function onError(error: any) {
    curError = error;
    tryResolve();
  }

  if (isDOMEventEmitter(emitter)) {
    emitter.addEventListener(nextEvent, onNext);
    if (endEvent) emitter.addEventListener(endEvent, onEnd);
    if (errorEvent) emitter.addEventListener(errorEvent, onError);
  } else {
    emitter.addListener(nextEvent, onNext);
    if (endEvent) emitter.addListener(endEvent, onEnd);
    if (errorEvent) emitter.addListener(errorEvent, onError);
  }

  function unlisten() {
    if (isDOMEventEmitter(emitter)) {
      emitter.removeEventListener(nextEvent, onNext);
      if (endEvent) emitter.removeEventListener(endEvent, onEnd);
      if (errorEvent) emitter.removeEventListener(errorEvent, onError);
    } else {
      emitter.removeListener(nextEvent, onNext);
      if (endEvent) emitter.removeListener(endEvent, onEnd);
      if (errorEvent) emitter.removeListener(errorEvent, onError);
    }
  }

  try {
    while (true) {
      await new Promise(resolve => curResolve = resolve);
      while (curValues.length > 0) {
        yield curValues.shift() as OutputT;
      }
      if (curError !== undefined) {
        throw curError;
      }
      if (completed) {
        return;
      }
    }
  }
  finally {
    unlisten();
  }
}

export function spinFunc(func: () => Promise<void>) {
  try {
    func().catch(console.error);
  }
  catch (error) {
    console.error(error);
  }
}
