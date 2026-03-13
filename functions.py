import os
import random
import json
import math

from Trainer import Trainer
from Player import Player
from Pokemon import Pokemon


def color_text(text: str, color: str) -> str:
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "gold": "\033[93m",
        "bold": "\033[1m",
        "reset": "\033[0m"
    }
    return f"{colors.get(color, colors['reset'])}{text}{colors['reset']}"


def calculate_pokemon_stats(level: int) -> dict:

    # A base value used to scale the stats relative to level
    # We use 50 as a generic "average" base stat
    base = 50
    iv = 31
    ev = 0

    # Simplified math using only the level provided
    inner = math.floor((2 * base + iv + math.floor(ev / 4)) * level / 100)

    return {
        "hp": inner + level + 10,
        "attack": inner + 5,
        "defense": inner + 5,
        "sp_attack": inner + 5,
        "sp_defense": inner + 5,
        "speed": inner + 5
    }

def clear_screen() -> None:
    # Als iemand op windows zit gebruik cls, en anders clear
    os.system("cls") if os.name == "nt" else os.system("clear")

def welcome() -> None:
    print("""
╔══════════════════════════════════════════════╗
║              ⚔️ POKÉMON BATTLE SIM ⚔️        ║
╚══════════════════════════════════════════════╝

Welkom trainer!

In deze Pokémon Battle Simulator neem jij het op
tegen een andere trainer in een spannende battle.

Je krijgt een random team van 6 Pokémon, 
elk met unieke stats en vaardigheden.
Kies je aanvallen verstandig en probeer
je tegenstander te verslaan!

Elke Pokémon heeft:
- ❤️ HP (health points)
- ⚡ Attack kracht
- 🛡️ Defense

Gebruik je aanvallen slim en win de battle!

Maak je klaar trainer...
De battle gaat beginnen!

""")

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
        print(color_text("Vul a.u.b een naam in van minimaal 2 karakters, maximaal 15 karakters en zonder cijfers.", "red"))
        name = input(msg)
    return name

def get_random_pokemon_names() -> list[str]:
    with open("pokemon.json", "r") as f:
        data = json.load(f)
    pokemon_names = [p["name"] for p in data]
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

        new_pokemon = Pokemon(name=random_name, level=random_level, hp=calculate_pokemon_stats(random_level)["hp"], attack=calculate_pokemon_stats(random_level)["attack"], defense=calculate_pokemon_stats(random_level)["defense"])
        # Maak een nieuwe Pokemon aan met de gegevens en append dit in de lijst
        pokemon.append(new_pokemon)
    # Geef de gehele lijst met pokemon terug
    return pokemon

def create_new_player(name:str, pokemon:list[Pokemon], money:int) -> Player:
    # Maak een nieuwe speler aan
    return Player(name=name, pokemon=pokemon, money=money)

def show_player_stats(player: Player) -> None:
    # Header and Player Info
    print("-" * 55)
    header_text = f"{player.name} | Balance: ${player.money}"
    print(color_text(header_text.center(55), "blue"))
    print("-" * 55)
    
    # Table Header
    print(f"{'Pokemon':<15} | {'Lvl':<6} | {'Attack':<10} | {'Defense':<10}")
    print("~" * 55)

    # Pokemon Rows
    for p in player.pokemon:
        name = color_text(f"{p.name:<15}", "cyan")
        lvl  = f"{p.level:<6}"
        att  = color_text(f"{p.attack:<10}", "red")
        defs = color_text(f"{p.defense:<10}", "blue")
        print(f"{name} | {lvl} | {att} | {defs}")
    print("-" * 55 + "\n")


def show_trainer_stats(trainer: Trainer) -> None:
    # Header and Trainer Info
    print("-" * 55)
    print(color_text(f"TRAINER: {trainer.name}".center(55), "bold"))
    print(f"Info: {trainer.description}")
    # Highlighting the Bounty in Yellow
    print(f"Bounty: {color_text(f'${trainer.price_money}', 'yellow')}")
    print("-" * 55)

    # Table Header (Underlined or Bold looks best here)
    header = f"{'Pokemon':<15} | {'Lvl':<6} | {'Attack':<10} | {'Defense':<10}"
    print(color_text(header, "bold"))
    print("~" * 55)

    # Pokemon Rows with full color support
    for p in trainer.pokemon:
        name = color_text(f"{p.name:<15}", "cyan")
        lvl  = f"{p.level:<6}"
        att  = color_text(f"{p.attack:<10}", "red")
        defs = color_text(f"{p.defense:<10}", "blue")
        
        # Printing the formatted row
        print(f"{name} | {lvl} | {att} | {defs}")
    
    print("-" * 55 + "\n")


def show_all_trainers(trainers:list[Trainer]) -> None:
    print("Hier zijn de bestaande trainers:\n-----\n")
    for trainer in trainers:
        show_trainer_stats(trainer)

def create_new_trainer(name:str, description:str, pokemon:list, price_money:int) -> Trainer:
    # Maak een nieuwe trainer aan
    return Trainer(name=name, description=description, pokemon=pokemon, price_money=price_money)

def ask_trainer(msg:str) -> str:
    trainer_name = input(msg)
    return trainer_name

def check_trainer(trainer_name:str, trainers:list[Trainer]) -> Trainer | bool:
    for trainer in trainers:
        if trainer.name.lower() == trainer_name.lower():
            return trainer
    return False

def load_trainers_from_json(file_path: str) -> list[Trainer]:
    with open(file_path, "r") as f:
        data = json.load(f)

    trainers_list = []
    for name, info in data["trainers"].items():
        pokemon_team = get_random_pokemon(6)
        new_trainer = create_new_trainer(
            name=name,
            description=info["description"],
            pokemon=pokemon_team,
            price_money=info["prize_money"]
        )
        trainers_list.append(new_trainer)

    return trainers_list



def battle(player: Player, trainer: Trainer) -> None:
    print(f"--- De battle tussen {player.name} en {trainer.name} begint! ---")
    
    # We pakken de eerste beschikbare Pokémon van beiden
    p_poke = player.get_active_pokemon()
    t_poke = trainer.get_active_pokemon()

    print(f"{player.name} stuurt {p_poke.name} in!")
    print(f"{trainer.name} stuurt {t_poke.name} in!")

    while p_poke.is_fainted() == False and t_poke.is_fainted() == False:
        # Bepaal de volgorde op basis van speed
        pokemon_speed = p_poke.speed()
        trainer_speed = t_poke.speed()
        if pokemon_speed >= trainer_speed:
            first, second = (p_poke, t_poke), (t_poke, p_poke)
        else:
            first, second = (t_poke, p_poke), (p_poke, t_poke)

        # Eerste beurt
        execute_turn(first[0], first[1])
        
        # Controleer of het gevecht voorbij is na de eerste klap
        if first[1].is_fainted():
            print(f"{first[1].name} is uitgeschakeld!")
            break

        # Tweede beurt
        execute_turn(second[0], second[1])
        
        if second[1].is_fainted():
            print(f"{second[1].name} is uitgeschakeld!")

    print("--- Het gevecht is beëindigd! ---")

def execute_turn(attacker, defender) -> None:
    # Een simpele berekening voor schade
    damage = attacker.attack - (defender.defense // 2)
    damage = max(damage, 1) # Altijd minimaal 1 schade
    
    defender.hp -= damage
    print(f"{attacker.name} valt aan en doet {damage} schade! ({defender.name} HP: {max(defender.hp, 0)})")

def get_money_reward(trainer: Trainer) -> int:
    return trainer.price_money