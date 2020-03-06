// NODE ONLY!

import path from 'path';
import os from 'os';
import fs from 'fs';

export function lookupAssetExchangePath(createDirMode: 'all' | 'parent' | 'none', ...paths: string[]): string {
  // construct path
  const result = path.join(os.homedir(), '.assetexchange', ...paths);

  // create directories on request
  switch (createDirMode) {
    case 'all':
      fs.mkdirSync(result, { recursive: true });
      break;
    case 'parent':
      fs.mkdirSync(path.dirname(result), { recursive: true });
      break;
  }

  return result;
}

export function lookupServicesPath(createDirMode: 'all' | 'parent' | 'none', ...parts: string[]): string {
  return lookupAssetExchangePath(createDirMode, 'services', ...parts);
}

export function lookupServiceEntryPath(category: string, type: string, pid: number): string {
  return path.join(lookupServicesPath('all', category, type), pid + '');
}
