#if UNITY_EDITOR

namespace AssetExchange
{
    using System;
    using System.Collections.Generic;
    using System.Threading.Tasks;
    using UnityEditor;

    [InitializeOnLoad]
    public static class MainThread
    {
        private static readonly Queue<Action> queue = new Queue<Action>();

        static MainThread()
        {
            EditorApplication.update += Update;
        }

        static void Update()
        {
            lock (queue)
            {
                while (queue.Count > 0)
                {
                    queue.Dequeue().Invoke();
                }
            }
        }

        public static TResult Execute<TResult>(Func<TResult> func)
        {
            var completion = new TaskCompletionSource<TResult>();

            lock (queue)
            {
                void Wrapped()
                {
                    try
                    {
                        completion.TrySetResult(func());
                    }
                    catch (Exception ex)
                    {
                        completion.TrySetException(ex);
                    }
                }

                queue.Enqueue(Wrapped);
            }

            return completion.Task.Result;
        }

        public static void Execute(Action func)
        {
            var completion = new TaskCompletionSource<bool>();

            lock (queue)
            {
                void Wrapped()
                {
                    try
                    {
                        func();
                        completion.TrySetResult(true);
                    }
                    catch (Exception ex)
                    {
                        completion.TrySetException(ex);
                    }
                }

                queue.Enqueue(Wrapped);
            }

            completion.Task.Wait();
        }
    }

    [AttributeUsage(AttributeTargets.Method, Inherited = true)]
    public class MainThreadAttribute : Attribute
    {
    }
}

#endif
