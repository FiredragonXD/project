""""
https://codespaces.new/FiredragonXD/project
"""



import random
from item import HealthPotion

class Player:
    def __init__(self, name, health=100, attack=10, defense=5):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.current_location = None
        self.inventory = [HealthPotion() for _ in range(10)]  # Initialize with 10 health potions

    def show_inventory(self):
        print("Inventory:")
        for i, item in enumerate(self.inventory):
            print(f"{i + 1}. {item.name}")

    def show_map(self):
        if self.current_location:
            print("Available movement directions:")
            for direction, location in self.current_location.connections.items():
                print(f"- {direction.capitalize()}: {location.name}")
        else:
            print("You haven't started the game yet.")

    def move(self, direction):
        if self.current_location:
            if direction in self.current_location.connections:
                new_location = self.current_location.connections[direction]
                print(f"You have moved to {new_location.name}.")
                new_location.on_enter()
                self.current_location = new_location
            else:
                print("You can't move in that direction.")
        else:
            print("You haven't started the game yet.")

    def pick_up_health(self):
        extra_health = random.randint(10, 30)
        print(f"You found {extra_health} extra health. Do you want to pick it up? (yes/no)")
        choice = input().lower().strip()
        if choice == "yes":
            self.health = min(self.health + extra_health, self.max_health)
            print(f"You picked up {extra_health} extra health.")
        elif choice == "no":
            print("You decided not to pick up the extra health.")
        else:
            print("Invalid choice.")

    def attack_enemy(self, enemy):
        damage = max(0, self.attack - enemy.defense)
        enemy.health -= damage
        print(f"You attacked {enemy.name} for {damage} damage.")
        print(f"{enemy.name}'s health: {enemy.health}/{enemy.max_health}")
        if enemy.health <= 0:
            print(f"{enemy.name} has been defeated!")
            self.current_location.enemy = None
            self.pick_up_health()  # Player picks up extra health after defeating enemy
        else:
            self.receive_attack(enemy)

    def receive_attack(self, enemy):
        damage = max(0, enemy.attack - self.defense)
        self.health -= damage
        print(f"{enemy.name} attacked you for {damage} damage.")
        print(f"Your health: {self.health}/{self.max_health}")
        if self.health <= 0:
            print("You have been defeated. Game over!")
            quit()

    def use_health_potion(self):
        if self.inventory:
            self.health = min(self.health + 20, self.max_health)
            self.inventory.pop()
            print("You used a Health Potion and restored 20 health points.")
        else:
            print("You don't have any health potions left.")

    def use_item(self, item_index):
        if 0 <= item_index < len(self.inventory):
            self.use_health_potion()
        else:
            print("Invalid item index.")

class Location:
    def __init__(self, name, description, connections=None, enemy=None):
        self.name = name
        self.description = description
        self.connections = connections or {}
        self.enemy = enemy

    def on_enter(self):
        print(self.description)
        if self.enemy:
            print(f"A {self.enemy.name} ({self.enemy.health}/{self.enemy.max_health} HP) is here.")

class RPGGame:
    def __init__(self):
        self.player = None
        self.locations = {}
        self.current_location = None

    def start_game(self):
        self.load_map()
        self.current_location = self.locations["Town"]
        self.player = Player(input("Enter your name: "))
        self.player.current_location = self.current_location
        self.current_location.on_enter()

    def load_map(self):
        town = Location("Town", "A peaceful town with friendly people.")
        forest = Location("Forest", "A dense forest filled with dangerous creatures.", {"north": town}, Enemy("Goblin"))
        cave = Location("Cave", "A dark cave with mysterious creatures.", {"east": forest}, Enemy("Bat"))
        dungeon = Location("Dungeon", "A dark dungeon with treasures and monsters.", {"south": town, "west": cave}, Enemy("Dragon"))
        town.connections = {"north": forest, "south": dungeon}
        forest.connections = {"south": town}
        cave.connections = {"east": forest}
        dungeon.connections = {"north": town, "west": cave}
        self.locations = {"Town": town, "Forest": forest, "Cave": cave, "Dungeon": dungeon}

    def play(self):
        print("Welcome to the RPG Game!")
        self.player.show_inventory()
        print("Available movement directions:", ", ".join(self.player.current_location.connections.keys()))

        while True:
            print("\nCommands: move <direction>, attack, use, map, inventory, quit")
            command = input("Enter command: ").lower().strip()
            
            if command.startswith("move"):
                direction = command.split()[1]
                self.player.move(direction)
            elif command == "attack":
                if self.player.current_location.enemy:
                    self.player.attack_enemy(self.player.current_location.enemy)
                else:
                    print("There are no enemies here.")
            elif command == "use":
                self.player.use_item(0)  # Use health potion
            elif command == "map":
                self.player.show_map()
            elif command == "inventory":
                self.player.show_inventory()
            elif command == "quit":
                print("Thanks for playing!")
                break
            else:
                print("Invalid command. Please try again.")

class Enemy:
    def __init__(self, name, health=50, attack=8, defense=3):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense

if __name__ == "__main__":
    game = RPGGame()
    game.start_game()
    game.play()
