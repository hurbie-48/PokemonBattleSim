from Pokemon import Pokemon

class Player:
    def __init__(self, name: str, pokemon: list[Pokemon], money: int):
        self.name = name
        self.money = money
        self.pokemon = pokemon

    def __repr__(self):
        return f"{self.name}"
    
    def get_active_pokemon(self) -> Pokemon:
        for p in self.pokemon:
            if p.is_alive():
                return p
        return None

    def has_usable_pokemon(self) -> bool:
        return any(p.is_alive() for p in self.pokemon)