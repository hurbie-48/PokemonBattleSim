import random

class Pokemon:
    def __init__(self):
        pokemon_pool = ["Mudkip", "Pikachu", "Chikorita", "Torchic", "Bulbasaur"]

        self.name = random.choice(pokemon_pool)
        self.level = random.randint(2, 5)