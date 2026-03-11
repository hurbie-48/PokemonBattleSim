from Pokemon import Pokemon


class Player:
    def __init__(self, name:str, pokemon:list[Pokemon]):
        self.name = name
        self.pokemon = pokemon

    def __repr__(self):
        return f"{self.name})"