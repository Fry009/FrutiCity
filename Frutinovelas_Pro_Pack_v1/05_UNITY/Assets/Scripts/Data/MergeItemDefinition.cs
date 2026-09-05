using UnityEngine;

namespace Frutinovelas.Data
{
    [CreateAssetMenu(menuName = "Frutinovelas/Merge Item")]
    public class MergeItemDefinition : ScriptableObject
    {
        public string id;
        public string chainId;
        public int level = 1;
        public string displayName;
        public Sprite icon;
        public MergeItemDefinition nextLevel;
    }
}
