// NODE ONLY!

import net from 'net';
import process from 'process';
import { Registry } from './registry';
import { newServer, shutdownServer } from './server';

export async function mainProc(
  category: string, type: string, registry: Registry,
  onStarted: ((address: net.AddressInfo) => Promise<void>) | null,
  onShutdown: (() => Promise<void>) | null,
  shutdownSignals: NodeJS.Signals[] | null
): Promise<void> {

  // default shutdown signals
  if (!shutdownSignals) {
    shutdownSignals = [
      'SIGINT',
      'SIGTERM'
    ];
  }

  // resume stdin if paused
  const stdinWasPaused = process.stdin.isPaused();
  if (stdinWasPaused) {
    process.stdin.resume();
  }

  try {
    // create server
    const server = await newServer(registry, category, type);

    if (onStarted) {
      await onStarted(server.address);
    }

    // wait for stop signal
    await new Promise(resolve => {
      function onSigShutdown() {
        shutdownSignals?.forEach(
          sigName => process.off(sigName, onSigShutdown)
        );
        resolve();
      }
      shutdownSignals?.forEach(
        sigName => process.on(sigName, onSigShutdown)
      );
    });

    // shutdown rpc server gracefully
    await shutdownServer(server);

    if (onShutdown) {
      await onShutdown();
    }

    // we are done now!
  }
  finally {

    // reset stdin state
    if (stdinWasPaused) {
      process.stdin.pause();
    }
  }
}
