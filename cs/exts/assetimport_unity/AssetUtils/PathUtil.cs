#if UNITY_EDITOR

using System.IO;

namespace AssetExchange.AssetUtils
{
    public static class PathUtil
    {
        public static string FreeDirEntryName(string dirPath, string basename, string extension)
        {
            for (int i = 0; ; i++)
            {
                var entryname = basename + (i > 0 ? "_" + i.ToString() : "") + extension;
                var entrypath = Path.Combine(dirPath, entryname);
                if (!Directory.Exists(entrypath) && !File.Exists(entrypath))
                {
                    return entryname;
                }
            }
        }
    }
}

#endif
