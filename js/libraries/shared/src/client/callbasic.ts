const fetch: typeof window.fetch = (window && window.fetch) || require('node-fetch').default;

export async function rpcCallBasicFunc<InputT, OutputT>(port: number, service: string, func: string, input: InputT): Promise<OutputT> {

  const url = "http://127.0.0.1:" + port + "/.assetexchange/basic";

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    body: JSON.stringify({
      id: 0,
      address: service + '.' + func,
      input: input,
      final: true,
    }),
  });

  if (!res.ok) {
    throw new Error('invalid status code');
  }

  const resMsg = await res.json();

  if (resMsg.error) {
    throw new Error(resMsg.error);
  }

  return resMsg.output;
}
