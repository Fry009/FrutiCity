using System;
using System.Collections.Generic;
using Frutinovelas.Core;

namespace Frutinovelas.Save
{
    [Serializable]
    public class SaveData
    {
        public int version = 1;
        public Wallet wallet = new Wallet();
        public List<string> completedLevels = new();
        public List<string> unlockedEpisodes = new() { "episode_01" };
        public List<FurnitureSelection> furniture = new();
        public List<CharacterProgress> characters = new();
    }

    [Serializable]
    public class FurnitureSelection
    {
        public string slotId;
        public int selectedVariant;
    }

    [Serializable]
    public class CharacterProgress
    {
        public string characterId;
        public int level = 1;
        public int xp = 0;
    }
}
