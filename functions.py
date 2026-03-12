import os
import random
import json
from Player import Player
from Pokemon import Pokemon



def clear_screen() -> None:
    # Als iemand op windows zit gebruik cls, en anders clear
    os.system("cls") if os.name == "nt" else os.system("clear")

def welcome() -> None:
    # print welkom!
    print("\nWelkom!")

def is_name_valid(name: str) -> bool:
    # Check of de naam minimaal 2 en maximaal 15 karakters heeft.
    if 1 < len(name) < 16:
        for karakter in name:
            if karakter.isdigit():
                return False
        return True
    else:
        return False

def ask_name(msg: str) -> str:
    name = input(msg)
    while not is_name_valid(name):
        print("Vul a.u.b een naam in van minimaal 2 karakters, maximaal 15 karakters en zonder cijfers.")
        name = input(msg)
    return name

def get_random_pokemon(count:int) -> list[Pokemon]:
    
    with open("pokemon.json", "r") as f:
        pokemon_names = json.load(f)

    pokemon_names = pokemon_names["name"]
    print(pokemon_names)


    
    
    # Maak een nieuwe lijst aan waar de pokemons in komen
    pokemon = []
    for i in range(count):
        # Kies een random pokemon uit de lijst pokemon_names
        random_name = random.choice(pokemon_names)
        # Kies een random getal van 2 tot 5 en sla deze op in random_level
        random_level = random.randint(2,5)
        # Maak een nieuwe Pokemon aan met de gegevens en append dit in de lijst
        pokemon.append(Pokemon(name=random_name, level=random_level))
    # Geef de gehele lijst met pokemon terug
    return pokemon

def create_new_player(name:str, pokemon:list) -> Player:
    # Maak een nieuwe speler aan
    return Player(name=name, pokemon=pokemon)

def show_pokemon(player:Player) -> None:
    # Print alle pokemons die een speler heeft
    print(f"{player.name} heeft op dit moment de volgende pokemon: \n")
    for pokemon in player.pokemon:
        print(f"{pokemon}")