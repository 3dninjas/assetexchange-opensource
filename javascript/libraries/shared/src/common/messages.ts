export type RequestMessage = {
  id: number
  address?: string
  input?: any
  final: boolean
}

export function getServiceFromRequest(reqMsg: RequestMessage): string {
  if (!reqMsg.address) {
    throw new Error('address not available');
  }
  const parts = reqMsg.address.split('.');
  parts.pop();
  return parts.join('.');
}

export function getFunctionFromRequest(reqMsg: RequestMessage): string {
  if (!reqMsg.address) {
    throw new Error('address not available');
  }
  return reqMsg.address.split('.').pop() as string;
}

export type ResponseMessage = {
  id: number
  output?: any
  error?: string
  final: boolean
}
