from Pokemon import Pokemon


class Trainer:
    def __init__(self, name:str, description:str, pokemon:list[Pokemon], price_money:int):
        self.name = name
        self.description = description
        self.pokemon = pokemon
        self.price_money = price_money

    def __repr__(self):
        return f"{self.name}"