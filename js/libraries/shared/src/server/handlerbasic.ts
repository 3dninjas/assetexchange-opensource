// NODE ONLY!

import express from 'express';
import { getFunctionFromRequest, getServiceFromRequest, RequestMessage, ResponseMessage } from '../common';
import { lookupServiceFunc, Registry } from './registry';

export function newBasicHandler(registry: Registry): express.RequestHandler {
  return async (req, res, next) => {
    try {
      // retrieve request message
      const reqMsg = req.body as RequestMessage;

      if (!reqMsg.address) {
        res.status(400).send('address not given');
        return;
      }

      if (reqMsg.final !== true) {
        res.status(400).send('request needs to be final');
        return;
      }

      try {
        // get and call func
        const [service, func] = lookupServiceFunc(registry, getServiceFromRequest(reqMsg), getFunctionFromRequest(reqMsg), 'basic');
        const resOutput = await func.call(service, reqMsg.input);

        // create response message
        const resMsg = <ResponseMessage>{
          id: reqMsg.id,
          output: resOutput,
          final: true,
        };

        // write response
        res.json(resMsg);
      }
      catch (err) {

        // create response message
        const resMsg = <ResponseMessage>{
          id: reqMsg.id,
          error: (err.message || err) + '',
          final: true,
        };

        // write response
        res.json(resMsg);
      }
    }
    catch (err) {

      // delegate to standard error handler
      next((err.message || err) + '');
    }
  };
}
