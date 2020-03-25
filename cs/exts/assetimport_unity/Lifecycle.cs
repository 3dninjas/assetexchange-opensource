#if UNITY_EDITOR

namespace AssetExchange
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.IO;
    using LightJSON;
    using UnityEditor;
    using UnityEngine;
    using Debug = UnityEngine.Debug;

    [InitializeOnLoad]
    public static class Lifecycle
    {
        static Server server;

        static Lifecycle()
        {
            EditorApplication.quitting += OnQuit;

            if (Application.isPlaying)
            {
                Debug.Log("AssetExchange.Lifecycle: skipping start in play mode.");
                return;
            }

            Debug.Log("AssetExchange.Lifecycle: starting...");

            server = new Server(
                new Dictionary<string, object>
                {
                    { "assetninja.assetpush#1", new AssetPushServiceV1() }
                }
            );
            var port = server.Start();

            var regPath = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
                ".assetexchange",
                "services",
                "extension.unity",
                "assetninja.extension.unity.assetimport",
                Process.GetCurrentProcess().Id.ToString()
            );

            Debug.Log("AssetExchange.Lifecycle: registry file = " + regPath);

            Directory.CreateDirectory(Path.GetDirectoryName(regPath));

            var regValue = new JsonObject
            {
                { "category", "extension.unity" },
                { "type", "assetninja.extension.unity.assetimport" },
                { "pid", Process.GetCurrentProcess().Id },
                { "port", port },
                { "protocols", new JsonArray{ "basic" } },
                { "info", new JsonObject
                    {
                        { "extension.uid", "assetninja.extension.unity.assetimport" },
                        { "extension.name", "Asset Exchange Asset Import" },
                        { "extension.description", "Handles asset pushes from Asset Ninja." },
                        { "extension.author", "Niklas Salmoukas" },
                        { "extension.version", "1.0.0" },
                        { "unity.executable", Process.GetCurrentProcess().MainModule.FileName },
                        { "unity.version", Application.unityVersion },
                    }
                },
                { "services", new JsonArray{ "assetninja.assetpush#1" } },
            }.ToString(true);

            File.WriteAllText(regPath, regValue);

            Debug.Log("AssetExchange.Lifecycle: started successfully!");
        }

        static void OnQuit()
        {
            try
            {
                var regPath = Path.Combine(
                    Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
                    ".assetexchange",
                    "services",
                    "extension.unity",
                    "assetninja.extension.unity.assetimport",
                    Process.GetCurrentProcess().Id.ToString()
                );

                File.Delete(regPath);
            }
            catch (Exception e)
            {
                Debug.LogError(e);
            }

            try
            {
                server?.Stop();
                server = null;
            }
            catch (Exception e)
            {
                Debug.LogError(e);
            }
        }
    }
}

#endif
