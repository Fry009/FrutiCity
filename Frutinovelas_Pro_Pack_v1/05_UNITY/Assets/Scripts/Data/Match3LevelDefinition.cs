using UnityEngine;

namespace Frutinovelas.Data
{
    [CreateAssetMenu(menuName = "Frutinovelas/Match3 Level")]
    public class Match3LevelDefinition : ScriptableObject
    {
        public string id;
        public int rows = 8;
        public int cols = 8;
        public int moves = 25;
        public string objectiveType;
        public int targetAmount;
        public int coinReward;
        public int starReward;
    }
}
