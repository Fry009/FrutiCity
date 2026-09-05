using System;
using System.Collections.Generic;

namespace Frutinovelas.Core
{
    [Serializable]
    public class Wallet
    {
        public int coins = 500;
        public int stars = 0;
        public int energy = 50;
        public int gems = 0;

        public int Get(CurrencyType type) => type switch
        {
            CurrencyType.Coins => coins,
            CurrencyType.Stars => stars,
            CurrencyType.Energy => energy,
            CurrencyType.Gems => gems,
            _ => 0
        };

        public bool TrySpend(CurrencyType type, int amount)
        {
            if (amount < 0 || Get(type) < amount) return false;
            Add(type, -amount);
            return true;
        }

        public void Add(CurrencyType type, int amount)
        {
            switch (type)
            {
                case CurrencyType.Coins: coins += amount; break;
                case CurrencyType.Stars: stars += amount; break;
                case CurrencyType.Energy: energy += amount; break;
                case CurrencyType.Gems: gems += amount; break;
            }
        }
    }
}
