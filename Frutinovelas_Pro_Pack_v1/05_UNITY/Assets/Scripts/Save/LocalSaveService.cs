using System.IO;
using UnityEngine;

namespace Frutinovelas.Save
{
    public class LocalSaveService
    {
        private readonly string _path;

        public LocalSaveService()
        {
            _path = Path.Combine(Application.persistentDataPath, "save.json");
        }

        public SaveData Load()
        {
            if (!File.Exists(_path))
                return new SaveData();

            try
            {
                return JsonUtility.FromJson<SaveData>(File.ReadAllText(_path)) ?? new SaveData();
            }
            catch
            {
                return new SaveData();
            }
        }

        public void Save(SaveData data)
        {
            File.WriteAllText(_path, JsonUtility.ToJson(data, true));
        }
    }
}
