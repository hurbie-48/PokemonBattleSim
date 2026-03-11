class Player:
    def __init__(self, name:str, pokemon:list):
        self.name = name
        self.pokemon = pokemon

    def __repr__(self):
        return f"{self.name})"