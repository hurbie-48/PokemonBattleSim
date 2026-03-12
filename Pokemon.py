class Pokemon:
    def __init__(self, name: str, level: int, hp:int, attack:int, defense:int):
        self.name = name
        self.level = level
        self.hp = hp
        self.attack = attack
        self.defense = defense

    def __repr__(self):
        return f"{self.name} (Lvl {self.level})"