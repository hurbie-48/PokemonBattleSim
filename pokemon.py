import random

class Pokemon:
    def __init__(self, data=None):
        self.name = "Unknown"
        self.level = random.randint(2, 5)
        self.type = []

        if isinstance(data, dict):
            self.name = data.get("name", "Unknown")
            self.type = data.get("type", [])
        
        elif isinstance(data, list) and len(data) > 0:
            random_pokemon = random.choice(data)
            self.name = random_pokemon.get("name", "Unknown")
            self.type = random_pokemon.get("type", [])