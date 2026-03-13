class Pokemon:
    def __init__(self, name: str, level: int, hp: int, attack: int, defense: int, speed: int):
        self.name = name
        self.level = level
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.moves = ["Tackle", "Tail Whip", "Ember"]

    def is_alive(self) -> bool:
        return self.hp > 0

    def is_fainted(self) -> bool:
        return self.hp <= 0

    def __repr__(self):
        return f"{self.name} (HP: {self.hp}/{self.max_hp})"