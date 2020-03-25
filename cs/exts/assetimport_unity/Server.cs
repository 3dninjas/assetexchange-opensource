#if UNITY_EDITOR

namespace AssetExchange
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    using System.Net;
    using System.Net.Sockets;
    using System.Threading;
    using AssetExchange.LightJSON;
    using AssetExchange.LightJSON.Serialization;
    using UnityEngine;

    public class Server
    {
        private readonly Dictionary<string, object> registry;
        private HttpListener listener;
        private Thread thread;
        private readonly ManualResetEvent stop = new ManualResetEvent(false);

        public Server(Dictionary<string, object> registry)
        {
            this.registry = registry;
        }

        public int Start()
        {
            Stop();

            // alloc port
            TcpListener tl = new TcpListener(IPAddress.Loopback, 0);
            tl.Start();
            int port = ((IPEndPoint)tl.LocalEndpoint).Port;
            tl.Stop();
            Debug.Log("AssetExchange.Server: using port = " + port.ToString());

            // create http listener
            listener = new HttpListener();
            listener.Prefixes.Add("http://127.0.0.1:" + port.ToString() + "/");
            listener.Prefixes.Add("http://localhost:" + port.ToString() + "/");
            listener.Start();

            thread = new Thread(() =>
            {
                // loop till stop signal
                while (!stop.WaitOne(0))
                {
                    try
                    {
                        // get next http request
                        HttpListenerContext context = listener.GetContext();

                        // handle cors
                        context.Response.Headers.Add("Access-Control-Allow-Origin", "*");
                        context.Response.Headers.Add("Access-Control-Allow-Methods", "OPTIONS, POST");
                        context.Response.Headers.Add("Access-Control-Allow-Headers", "*");
                        context.Response.Headers.Add("Access-Control-Max-Age", "86400");

                        if (context.Request.HttpMethod == "OPTIONS")
                        {
                            context.Response.StatusCode = (int)HttpStatusCode.OK;
                            context.Response.OutputStream.Flush();
                            context.Response.OutputStream.Close();
                            continue;
                        }

                        if (context.Request.HttpMethod != "POST")
                        {
                            context.Response.StatusCode = (int)HttpStatusCode.InternalServerError;
                            context.Response.OutputStream.Flush();
                            context.Response.OutputStream.Close();
                            continue;
                        }

                        // read request message
                        using (StreamReader reqReader = new StreamReader(context.Request.InputStream))
                        {
                            var reqMsg = JsonReader.Parse(reqReader.ReadToEnd()).AsJsonObject;

                            try
                            {
                                // validate request
                                if (!reqMsg.ContainsKey("address") || !reqMsg["address"].IsString)
                                {
                                    throw new Exception("address missing");
                                }

                                if (!reqMsg.ContainsKey("final") || !reqMsg["final"].IsBoolean || !reqMsg["final"].AsBoolean)
                                {
                                    throw new Exception("request not final");
                                }

                                // extract service and function name
                                var addressParts = reqMsg["address"].AsString.Split('.');
                                var serviceName = string.Join(".", addressParts.Take(addressParts.Length - 1));
                                var functionName = addressParts[addressParts.Length - 1];

                                // lookup service
                                if (!registry.ContainsKey(serviceName))
                                {
                                    throw new Exception("unknown service");
                                }

                                // lookup function
                                var function = registry[serviceName].GetType().GetMethod(functionName);
                                if (function == null)
                                {
                                    throw new Exception("unknown function");
                                }

                                var onMainThread = function.GetCustomAttributes(typeof(MainThreadAttribute), true).Any();

                                // call function
                                object output = null;

                                if (!onMainThread)
                                {
                                    output = function.Invoke(registry[serviceName], new object[] { reqMsg["input"] });
                                }
                                else
                                {
                                    output = MainThread.Execute(() =>
                                    {
                                        return function.Invoke(registry[serviceName], new object[] { reqMsg["input"] });
                                    });
                                }

                                if (!(output is JsonValue))
                                {
                                    throw new Exception("invalid output type");
                                }

                                // create response
                                var resMsg = new JsonObject
                                {
                                    { "id", reqMsg["id"] },
                                    { "output", (JsonValue)output },
                                    { "error", new JsonValue((string)null) },
                                    { "last", true },
                                };

                                // write response
                                context.Response.StatusCode = (int)HttpStatusCode.OK;
                                context.Response.ContentType = "application/json";
                                using (StreamWriter resWriter = new StreamWriter(context.Response.OutputStream))
                                {
                                    resWriter.Write(resMsg.ToString(false));
                                }
                                context.Response.OutputStream.Flush();
                                context.Response.OutputStream.Close();

                            }
                            catch (Exception ex)
                            {
                                Debug.Log(ex);

                                // create response
                                var resMsg = new JsonObject
                                {
                                    { "id", reqMsg["id"] },
                                    { "output", new JsonValue((string)null) },
                                    { "error", new JsonValue(ex.Message) },
                                    { "last", true },
                                };

                                // write response
                                context.Response.StatusCode = (int)HttpStatusCode.InternalServerError;
                                context.Response.ContentType = "application/json";
                                using (StreamWriter resWriter = new StreamWriter(context.Response.OutputStream))
                                {
                                    resWriter.Write(resMsg.ToString(false));
                                }
                                context.Response.OutputStream.Flush();
                                context.Response.OutputStream.Close();
                            }
                        }
                    }
                    catch (Exception ex)
                    {
                        Debug.Log(ex);
                    }
                }
            });

            thread.Start();

            return port;
        }

        public void Stop()
        {
            // shutdown
            stop.Set();
            listener?.Close();
            thread?.Join();

            // reset
            stop.Reset();
            listener = null;
            thread = null;
        }
    }
}

#endif
