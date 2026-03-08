from pokemon import *
import os
import platform

players = {}

def welcome() -> None:
    print("Welcome!")

def addNewPlayer(name: str) -> str:
    player_count = len(players) + 1
    player_key = f"Player #{player_count}"
    
    players[player_key] = {
        "name": name,
        "pokemon": []
    }
    return player_key

def showAllPlayers() -> None:
    if not players:
        print("There are currently no players!")
        return
    print("--- Current Player Records ---")
    for player_id, info in players.items():
        player_name = info["name"]
        pokemon_display = []
        for p in info["pokemon"]:
            if hasattr(p, 'name'):
                pokemon_display.append(f"{p.name} (Lvl {p.level})")
            else:
                pokemon_display.append(str(p))
        pokemon_str = ", ".join(pokemon_display) if pokemon_display else "None"
        print(f"{player_id}: {player_name}")
        print(f"  Team: {pokemon_str}")

def validateName(name: str) -> bool:
    existing_names = [info["name"] for info in players.values()]
    
    if name in existing_names: return False
    if len(name) < 2 or len(name) > 15: return False
    if not name[0].isupper(): return False
    return True

def validateNumber(number: int) -> bool:
    return 1 <= number <= 10

def askName(msg: str) -> str:
    while True:
        name = input(msg)
        if validateName(name):
            return name
        print("Please enter a valid name! (2-15 chars, starts with Capital, not taken)")

def askNumber(msg: str) -> int:
    while True:
        user_input = input(msg)
        if user_input.isdigit():
            number = int(user_input)
            if validateNumber(number):
                return number
        print("Please enter a valid number from 1 to 10!")
    

def givePokemonToPlayer(player: str, count: int) -> None:
    if player in players:
        for i in range(count):
            pokemon = getRandomPokemon()
            players[player]["pokemon"].append(pokemon)
    else:
        print(f"Error: {player} does not exist in the players dictionary.")

def getRandomPokemon() -> Pokemon:
    return Pokemon()

def returnPokemonProperties(pokemon:Pokemon) -> list:
    return [pokemon.name, pokemon.level]

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")