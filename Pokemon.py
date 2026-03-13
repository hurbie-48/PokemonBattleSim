class Pokemon:
    def __init__(self, name: str, level: int, hp:int, attack:int, defense:int):
        self.name = name
        self.level = level
        self.hp = hp
        self.attack = attack
        self.defense = defense

    def __repr__(self):
        return f"{self.name} (Lvl {self.level})"
    
    def is_alive(self) -> bool:
        return self.hp > 0
    
    def is_fainted(self) -> bool:
        return self.hp <= 0
    
    def speed(self) -> int:
        # Simple speed calculation based on level and attack
        return self.level * 2 + self.attack