import os
import random
import json
import math

from Trainer import Trainer
from Player import Player
from Pokemon import Pokemon

def color_text(text: str, color: str) -> str:
    colors = {
        "red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m",
        "blue": "\033[94m", "magenta": "\033[95m", "cyan": "\033[96m",
        "gold": "\033[93m", "bold": "\033[1m", "reset": "\033[0m"
    }
    return f"{colors.get(color, colors['reset'])}{text}{colors['reset']}"

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

Maak je klaar trainer...
De battle gaat beginnen!
""")

def show_player_stats(player: Player) -> None:
    print("-" * 55)
    header_text = f"{player.name} | Balance: ${player.money}"
    print(color_text(header_text.center(55), "blue"))
    print("-" * 55)
    print(f"{'#':<2} {'Pokemon':<15} | {'Lvl':<4} | {'HP':<10} | {'Atk':<5} | {'Def':<5}")
    print("~" * 55)
    for i, p in enumerate(player.pokemon):
        status_color = "cyan" if p.is_alive() else "red"
        hp_text = f"{max(0, p.hp)}/{p.max_hp}"
        print(f"{i+1:<2} {color_text(f'{p.name:<15}', status_color)} | {p.level:<4} | {hp_text:<10} | {p.attack:<5} | {p.defense:<5}")
    print("-" * 55 + "\n")

def choose_pokemon(player: Player) -> Pokemon:
    """Lets the player choose an alive Pokemon from their team."""
    show_player_stats(player)
    while True:
        try:
            keuze = int(input(f"Welke Pokémon kies je? (1-{len(player.pokemon)}): "))
            selected = player.pokemon[keuze-1]
            if selected.is_alive():
                return selected
            else:
                print(color_text("Deze Pokémon is flauwgevallen! Kies een andere.", "red"))
        except (ValueError, IndexError):
            print(color_text("Ongeldige keuze. Voer een nummer in uit de lijst.", "red"))

def execute_turn(attacker, defender, move_name: str) -> None:
    damage = max(1, attacker.attack - (defender.defense // 2))
    defender.hp -= damage
    atk_display = color_text(attacker.name, "yellow")
    move_display = color_text(move_name, "bold")
    print(f"{atk_display} gebruikt {move_display}! {defender.name} verliest {damage} HP.")

def battle(player, trainer) -> bool:
    print(color_text(f"\n--- DE BATTLE TUSSEN {player.name} EN {trainer.name} BEGINT! ---", "bold"))
    
    # Player chooses their first Pokemon
    print(f"\n{trainer.name} daagt je uit! Kies je eerste Pokémon.")
    p_poke = choose_pokemon(player)
    t_poke = trainer.get_active_pokemon()

    print(f"\n{player.name} stuurt {color_text(p_poke.name, 'cyan')} in!")
    print(f"{trainer.name} stuurt {color_text(t_poke.name, 'red')} in!")

    while player.has_usable_pokemon() and trainer.has_usable_pokemon():
        # Inner loop for current 1v1
        while p_poke.is_alive() and t_poke.is_alive():
            print(f"\n{color_text(p_poke.name, 'cyan')} HP: {max(0, p_poke.hp)}/{p_poke.max_hp}")
            print(f"{color_text(t_poke.name, 'red')} HP: {max(0, t_poke.hp)}/{t_poke.max_hp}")
            
            print("\nWat wil je doen?")
            for i, move in enumerate(p_poke.moves):
                print(f"{i+1}. {move}")
            
            keuze = input("Kies een move (1-3): ")
            move_index = int(keuze) - 1 if keuze.isdigit() and 1 <= int(keuze) <= 3 else 0
            player_move = p_poke.moves[move_index]

            if p_poke.speed >= t_poke.speed:
                execute_turn(p_poke, t_poke, player_move)
                if t_poke.is_alive():
                    execute_turn(t_poke, p_poke, random.choice(t_poke.moves))
            else:
                execute_turn(t_poke, p_poke, random.choice(t_poke.moves))
                if p_poke.is_alive():
                    execute_turn(p_poke, t_poke, player_move)

        # Handle faint scenarios
        if t_poke.is_fainted():
            print(color_text(f"\n{t_poke.name} van {trainer.name} is verslagen!", "green"))
            if trainer.has_usable_pokemon():
                t_poke = trainer.get_active_pokemon()
                print(f"{trainer.name} stuurt {color_text(t_poke.name, 'red')} in!")

        if p_poke.is_fainted():
            print(color_text(f"\n{p_poke.name} is uitgeschakeld!", "red"))
            if player.has_usable_pokemon():
                print("Kies een nieuwe Pokémon om verder te vechten.")
                p_poke = choose_pokemon(player)
                print(f"{player.name} stuurt {color_text(p_poke.name, 'cyan')} in!")

    if player.has_usable_pokemon():
        print(color_text(f"\nGEFELICITEERD! Je hebt {trainer.name} verslagen!", "gold"))
        return True
    return False

# Rest of the helper functions remain the same as your provided code
def calculate_pokemon_stats(level: int) -> dict:
    base, iv = 50, 31
    inner = math.floor((2 * base + iv) * level / 100)
    return {
        "hp": inner + level + 10, "attack": inner + 5,
        "defense": inner + 5, "speed": inner + 5 
    }

def clear_screen() -> None:
    os.system("cls") if os.name == "nt" else os.system("clear")

def get_random_pokemon(count: int) -> list[Pokemon]:
    try:
        with open("pokemon.json", "r") as f:
            data = json.load(f)
        names = [p["name"] for p in data]
    except FileNotFoundError:
        names = ["Bulbasaur", "Charmander", "Squirtle"]

    team = []
    for _ in range(count):
        lvl = random.randint(2, 5)
        stats = calculate_pokemon_stats(lvl)
        team.append(Pokemon(random.choice(names), lvl, stats["hp"], stats["attack"], stats["defense"], stats["speed"]))
    return team

def load_trainers_from_json(file_path: str) -> list[Trainer]:
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        trainers_list = []
        for name, info in data["trainers"].items():
            new_trainer = Trainer(name, info["description"], get_random_pokemon(3), info["prize_money"])
            trainers_list.append(new_trainer)
        return trainers_list
    except: return []

def show_all_trainers(trainers: list[Trainer]) -> None:
    print("Hier zijn de beschikbare trainers:\n")
    for t in trainers:
        if not t.is_beaten:
            print("-" * 55)
            print(color_text(f"TRAINER: {t.name}".center(55), "bold"))
            print(f"Info: {t.description}")
            print(f"Bounty: {color_text(f'${t.price_money}', 'yellow')}")
            print("-" * 55)

def ask_name(msg: str) -> str:
    name = input(msg)
    while not (1 < len(name) < 16 and not any(char.isdigit() for char in name)):
        print(color_text("Vul a.u.b een naam in van 2-15 karakters zonder cijfers.", "red"))
        name = input(msg)
    return name

def get_money_reward(trainer: Trainer) -> int:
    """Returns the prize money from the trainer."""
    return trainer.price_money