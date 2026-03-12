import os
import random
import json

from Trainer import Trainer
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


def get_random_pokemon_names() -> list[str]:
    with open("pokemon.json", "r") as f:
        data = json.load(f)
    pokemon_names = [p["name"] for p in data["pokemon"]]
    return pokemon_names

def get_random_pokemon(count:int) -> list[Pokemon]:
    pokemon_names = get_random_pokemon_names()

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

def create_new_player(name:str, pokemon:list[Pokemon], money:int) -> Player:
    # Maak een nieuwe speler aan
    return Player(name=name, pokemon=pokemon, money=money)

def show_player_stats(player:Player) -> None:
    # Print alle pokemons die een speler heeft
    print(f"{player.name} heeft op dit moment ${player.money} en de volgende pokemon: \n")
    for pokemon in player.pokemon:
        print(f"{pokemon}")

def show_trainer_stats(trainer:Trainer) -> None:
    print(f"Naam: {trainer.name}\nBeschrijving: {trainer.description}\nPrijzengeld: {trainer.price_money}")
    print(f"{trainer.name} heeft de volgende pokemon:")
    for pokemon in trainer.pokemon:
        print(f"{pokemon}")

def show_all_trainers(trainers:list[Trainer]) -> None:
    print("Hier zijn de bestaande trainers:\n-----\n")
    for trainer in trainers:
        show_trainer_stats(trainer)

def create_new_trainer(name:str, description:str, pokemon:list, price_money:int) -> Trainer:
    # Maak een nieuwe trainer aan
    return Trainer(name=name, description=description, pokemon=pokemon, price_money=price_money)