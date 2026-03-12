from Pokemon import Pokemon


class Player:
    def __init__(self, name:str, pokemon:list[Pokemon], money:int):
        self.name = name
        self.money = money
        self.pokemon = pokemon

    def __repr__(self):
        return f"{self.name}"