import json
import random
import os
import time
 

# --- 1. DATA LOGICA ---
# Laad Pokémon en Trainers data vanuit JSON-bestanden
def load_data():
    try:
        with open("pokemon.json", "r") as f: pokemon_data = json.load(f)
        with open("trainers.json", "r") as f: trainers_data = json.load(f)
        return pokemon_data, trainers_data
# Indien bestanden niet gevonden worden, gebruik lege data (voor testdoeleinden)
    except FileNotFoundError:
        return [], {}
    
# haal de json op met de functie load_data() en sla deze op in variabelen  
pokemon_data, trainers_data = load_data()

# Functie om HP te bepalen op basis van moeilijkheidsgraad 
# jijzelf krijgt altijd 120 HP, maar vijanden krijgen meer HP afhankelijk van de moeilijkheidsgraad
def get_hp_for_difficulty(difficulty):
    hp_map = {"Beginner": 100, "Easy": 120, "Medium": 160, "Hard": 240, "Impossible": 320}
    return hp_map.get(difficulty, 120)


# Functie om een Pokémon te maken op basis van een basis Pokémon en moeilijkheidsgraad.
# Deze functie voegt HP toe en wijst moves toe op basis van het type Pokémon.
def get_pokemon(base, difficulty):
    pokemon = base.copy()
    hp = get_hp_for_difficulty(difficulty)
    pokemon.update({"max_hp": hp, "current_hp": hp})

    # Wijs moves toe op basis van type pokemon
    if "Fire" in pokemon.get("type", []): pokemon["moves"] = ["Ember", "Flamethrower", "Fire Blast", "Quick Attack"]
    elif "Water" in pokemon.get("type", []): pokemon["moves"] = ["Water Gun", "Surf", "Hydro Pump", "Tackle"]
    elif "Grass" in pokemon.get("type", []): pokemon["moves"] = ["Vine Whip", "Razor Leaf", "Solar Beam", "Tackle"]
    else: pokemon["moves"] = ["Tackle", "Quick Attack", "Slam", "Scratch"]
    return pokemon

# --- 2. GAME STATE ---
# je hebt een team van 6 pokemon die random worden gekozen uit de pokemon_data, en een wallet met geld en een aantal potions
player_team = [get_pokemon(random.choice(pokemon_data), "Easy") for _ in range(6)]
wallet = 200
potions = 2

# --- 3. HELPER FUNCTIES ---
# Functie om het scherm te wissen (voor een schonere interface)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Functie om een nette header te printen voor verschillende secties van het spel
def print_header(text):
    print("\n" + "="*40)
    print(f" {text.upper()} ")
    print("="*40)

# Functie om de status van het team te tonen, inclusief HP en of een Pokémon KO is
def show_team_status(team):
    for i, p in enumerate(team):
        status = f"{p['current_hp']}/{p['max_hp']} HP" if p['current_hp'] > 0 else "KO"
        print(f"[{i+1}] {p['name']} ({status})")

# --- 4. BATTLE LOGICA ---
# Deze functie regelt het gevecht tussen de speler en een trainer. 
# Het houdt rekening met aanvallen, wisselen, potions gebruiken en vluchten.
def start_battle(trainer_name, trainer_info):
    global wallet, potions
    difficulty = trainer_info.get("difficulty", "Easy")
    enemy_team = [get_pokemon(random.choice(pokemon_data), difficulty) for _ in range(2)]
    
    p_idx = 0 # Actieve pokemon index
    e_idx = 0
    
    print_header(f"Gevecht tegen Trainer {trainer_name}!")
    
    while True:
        p = player_team[p_idx]
        e = enemy_team[e_idx]
        
        clear_screen()
        print(f"TEGENSTANDER: {e['name']} [{e['current_hp']}/{e['max_hp']} HP]")
        print(f"JOUW POKÉMON: {p['name']} [{p['current_hp']}/{p['max_hp']} HP]")
        print("-" * 20)
        
        print("Wat ga je doen?")
        print("1. Aanvallen")
        print("2. Wisselen")
        print(f"3. Potion gebruiken ({potions} over)")
        print("4. Vluchten")
        
        keuze = input("> ")
        
        if keuze == "1":
            # Aanvallen
            print("\nKies een move:")
            for i, m in enumerate(p['moves']): print(f"{i+1}. {m}")
            m_keuze = int(input("> ")) - 1
            move = p['moves'][m_keuze]
            
            # Schade berekenen
            dmg = random.randint(20, 35)
            e['current_hp'] = max(0, e['current_hp'] - dmg)
            print(f"\n{p['name']} gebruikt {move}! Het doet {dmg} schade.")
            time.sleep(1)
            
        elif keuze == "2":
            # Wisselen
            print("\nKies een andere Pokémon:")
            show_team_status(player_team)
            nieuwe_idx = int(input("> ")) - 1
            if player_team[nieuwe_idx]['current_hp'] > 0:
                p_idx = nieuwe_idx
                print(f"Ga door, {player_team[p_idx]['name']}!")
                continue
            else:
                print("Deze Pokémon kan niet vechten!")
                time.sleep(1)
                continue
                
        elif keuze == "3":
            if potions > 0 and p['current_hp'] > 0:
                p['current_hp'] = min(p['max_hp'], p['current_hp'] + 50)
                potions -= 1
                print(f"{p['name']} is genezen!")
            else:
                print("Kan geen potion gebruiken.")
            time.sleep(1)
            
        elif keuze == "4":
            print("Je bent gevlucht!")
            return False

        # Check of enemy KO is
        if e['current_hp'] <= 0:
            print(f"Vijandige {e['name']} is verslagen!")
            e_idx += 1
            if e_idx >= len(enemy_team):
                print("JE HEBT GEWONNEN!")
                wallet += trainer_info.get("prize_money", 50)
                time.sleep(2)
                return True
            time.sleep(1)
            continue

        # Tegenstander valt aan
        dmg_in = random.randint(15, 25)
        p['current_hp'] = max(0, p['current_hp'] - dmg_in)
        print(f"De vijand valt aan en doet {dmg_in} schade!")
        time.sleep(1)
        
        # Check of speler KO is
        if p['current_hp'] <= 0:
            print(f"{p['name']} is uitgeschakeld!")
            if not any(pk['current_hp'] > 0 for pk in player_team):
                print("Je hele team is verslagen... GAME OVER")
                time.sleep(2)
                return False
            print("Wissel van Pokémon!")
            time.sleep(1)

# --- 5. HOOFDMENU ---
def main():
    global wallet, potions
    while True:
        clear_screen()
        print_header("Pokémon Terminal Adventure")
        print(f"Geld: ${wallet} | Potions: {potions}")
        print("\n1. Vecht tegen een Trainer")
        print("2. Poké Mart (Shop)")
        print("3. Team Status")
        print("4. Stop spel")
        
        keuze = input("\nKies een optie: ")
        
        if keuze == "1":
            trainers = trainers_data["trainers"]
            print("\nBeschikbare trainers:")
            t_list = list(trainers.keys())
            for i, t in enumerate(t_list):
                print(f"{i+1}. {t} ({trainers[t]['difficulty']})")
            
            t_keuze = int(input("Kies een trainer nummer: ")) - 1
            t_name = t_list[t_keuze]
            start_battle(t_name, trainers[t_name])
            
        elif keuze == "2":
            print("\n--- SHOP ---")
            print(f"1. Potion ($50)")
            print(f"2. Team Heal ($200)")
            s_keuze = input("Wat wil je kopen? (of druk Enter): ")
            if s_keuze == "1" and wallet >= 50:
                wallet -= 50; potions += 1
            elif s_keuze == "2" and wallet >= 200:
                wallet -= 200
                for p in player_team: p['current_hp'] = p['max_hp']
                
        elif keuze == "3":
            print("\n--- JE TEAM ---")
            show_team_status(player_team)
            input("\nDruk op Enter om door te gaan...")
            
        elif keuze == "4":
            break

if __name__ == "__main__":
    main()