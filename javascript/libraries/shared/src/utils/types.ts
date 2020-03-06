export interface RestrictedAsyncIterable<T> {
  [Symbol.asyncIterator](): AsyncIterator<T, void, undefined>; // we enforce void on return
}
