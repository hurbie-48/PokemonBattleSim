from pokemon import *
import json
import os
import platform

players = {}
DATA_FILE = "players_data.json"
POKEMON_SOURCE = "pokemon.json"
TRAINER_SOURCE = "trainers.json"
ASCII_FILE = "ascii.txt"

import os

def showAscii():
    if not os.path.exists(ASCII_FILE):
        return

    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"

    with open(ASCII_FILE, "r") as f:
        for line in f:
            pokemon_part = line[:75]
            battle_sim_part = line[75:]
            print(f"{YELLOW}{pokemon_part}{RED}{battle_sim_part}{RESET}", end="")
            
        print("\n" + "-"*169 + "\n\n\n\n")

def showTrainers() -> None:
    if not os.path.exists(TRAINER_SOURCE):
        print("Trainer data file not found.")
        return

    with open(TRAINER_SOURCE, "r") as f:
        content = json.load(f)
        trainers = content.get("trainers", {})

    print(f"{'NAAM':<10} | {'MOEILIJKHEID':<12} | {'PRIJS':<10}")
    print("-" * 40)

    for name, info in trainers.items():
        difficulty = info['difficulty']
        prize = f"${info['prize_money']}"
        description = info['description']
        
        print(f"{name:<10} | {difficulty:<12} | {prize:<10}")
        print(f"   \"{description}\"\n")

def askTrainer(msg: str) -> str:
    if not os.path.exists(TRAINER_SOURCE):
        print("Trainer data file not found.")
        return ""

    with open(TRAINER_SOURCE, "r") as f:
        content = json.load(f)
        trainers = content.get("trainers", {})

    trainer_names = list(trainers.keys())
    
    while True:
        choice = input(msg)
        if choice in trainer_names:
            # show selected trainer's info
            info = trainers[choice]
            difficulty = info.get('difficulty', 'Unknown')
            prize = info.get('prize_money', 0)
            description = info.get('description', '')
            # print summary message in Dutch to match user expectation
            print(f"\nJe hebt {choice} gekozen!")
            print(f"Moeilijkheidsgraad: {difficulty}")
            print(f"Prijzengeld: ${prize}")
            print(f"Beschrijving: {description}\n")
            return choice
        print(f"Please choose a valid trainer: {', '.join(trainer_names)}")
            

def load_pokemon_atlas():
    if os.path.exists(POKEMON_SOURCE):
        with open(POKEMON_SOURCE, "r") as f:
            data = json.load(f)
            
            if isinstance(data, dict):
                return list(data.values())
            
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                return data[0]
                
            return data
    return []


def jsonExists() -> bool:
    if os.path.exists(DATA_FILE):
        return True

def save_to_json():
    serializable_players = {}
    for p_id, info in players.items():
        pokemon_list = []
        for p in info["pokemon"]:
            pokemon_list.append({
                "name": p.name, 
                "level": p.level
            })
            
        serializable_players[p_id] = {
            "name": info["name"],
            "pokemon": pokemon_list
        }
    
    with open(DATA_FILE, "w") as f:
        json.dump(serializable_players, f, indent=4)

def load_from_json():
    global players
    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r") as f:
        raw_data = json.load(f)
    
    for p_id, info in raw_data.items():
        reconstructed_pokemon = []
        for p_data in info["pokemon"]:
            p = Pokemon()
            p.name = p_data["name"]
            p.level = p_data["level"]
            reconstructed_pokemon.append(p)
            
        players[p_id] = {
            "name": info["name"],
            "pokemon": reconstructed_pokemon
        }

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
    if POKEMON_POOL:
        random_data = random.choice(POKEMON_POOL)
        return Pokemon(random_data)
    return Pokemon()

def returnPokemonProperties(pokemon:Pokemon) -> list:
    return [pokemon.name, pokemon.level]

def clearScreen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")



POKEMON_POOL = load_pokemon_atlas()