using UnityEngine;

namespace Frutinovelas.Data
{
    [CreateAssetMenu(menuName = "Frutinovelas/Character")]
    public class CharacterDefinition : ScriptableObject
    {
        public string id;
        public string displayName;
        public string profession;
        [TextArea] public string goal;
        public Sprite portrait;
        public Sprite fullBody;
        public string passiveAbilityId;
    }
}
