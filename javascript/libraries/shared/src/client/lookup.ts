import { NodeInfo } from '../common';

declare global {
  interface Window {
    _native_lookup_nodes: (callback: (error: string | null, nodes: NodeInfo[]) => void) => void;
    _native_lookup_node_port: (category: string, type: string, callback: (error: string | null, port: number) => void) => void;
  }
}

export async function rpcLookupNodes(): Promise<NodeInfo[]> {
  if (window && window._native_lookup_nodes) {
    return await new Promise((resolve, reject) => {
      window._native_lookup_nodes((error, nodes) => {
        if (error) {
          return reject(error);
        }
        return resolve(nodes);
      });
    });
  } else {
    const { default: fs } = require('fs');
    const { default: path } = require('path');
    const { lookupServicesPath } = require('../common/path');
    const nodes: NodeInfo[] = []
    await (async function findEntries(dirPath: string) {
      const entries = await fs.promises.readdir(dirPath, { withFileTypes: true });
      for (const entry of entries) {
        const entryPath = path.join(dirPath, entry.name);
        if (entry.isFile()) {
          if (/^[\d]+$/.test(entry.name)) {
            try {
              nodes.push(JSON.parse(await fs.promises.readFile(entryPath, 'utf-8')));
            }
            catch (err) {
              console.warn(`could not read ${entryPath}`, err);
            }
          }
        }
        else if (entry.isDirectory()) {
          await findEntries(entryPath);
        }
      }
    })(lookupServicesPath('all'));
    return nodes;
  }
}

export async function rpcLookupNodePort(category: string, type: string): Promise<number> {
  if (window && window._native_lookup_node_port) {
    return await new Promise((resolve, reject) => {
      window._native_lookup_node_port(category, type, (error, port) => {
        if (error) {
          return reject(error);
        }
        return resolve(port);
      });
    });
  } else {
    const nodes = await rpcLookupNodes();
    const node = nodes.find(node => node.category == category && node.type == type);
    if (!node) {
      throw new Error('could not find port');
    }
    return node.port;
  }
}
