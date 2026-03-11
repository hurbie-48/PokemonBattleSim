class Pokemon:
    def __init__(self, name: str, level: int):
        self.name = name
        self.level = level

    def __repr__(self):
        return f"{self.name} (Lvl {self.level})"