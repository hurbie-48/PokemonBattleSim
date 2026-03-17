class Trainer:
    def __init__(self, name: str, description: str, pokemon: list, price_money: int):
        self.name = name
        self.description = description
        self.pokemon = pokemon
        self.price_money = price_money
        self.is_beaten = False

    def get_active_pokemon(self):
        for p in self.pokemon:
            if p.is_alive():
                return p
        return None

    def has_usable_pokemon(self) -> bool:
        return any(p.is_alive() for p in self.pokemon)


