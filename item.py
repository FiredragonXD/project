class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def use(self, player):
        pass

class HealthPotion(Item):
    def __init__(self):
        super().__init__("Health Potion", "Restores 20 health points.")

    def use(self, player):
        player.health = min(player.health + 20, player.max_health)
        print("You used a Health Potion and restored 20 health points.")

class Weapon(Item):
    def __init__(self, name, description, attack_bonus):
        super().__init__(name, description)
        self.attack_bonus = attack_bonus

    def use(self, player):
        player.attack += self.attack_bonus
        print(f"You equipped {self.name} and gained {self.attack_bonus} attack points.")

class Armor(Item):
    def __init__(self, name, description, defense_bonus):
        super().__init__(name, description)
        self.defense_bonus = defense_bonus

    def use(self, player):
        player.defense += self.defense_bonus
        print(f"You equipped {self.name} and gained {self.defense_bonus} defense points.")
