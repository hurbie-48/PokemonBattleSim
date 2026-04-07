import pygame
import json
import random
import os

# --- 1. INITIALISATIE ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Battle Simulator")
clock = pygame.time.Clock()

# Kleuren & Fonts
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)
GREEN, RED, BLUE, YELLOW = (0, 200, 0), (200, 0, 0), (0, 0, 255), (255, 255, 0)
font_name = pygame.font.SysFont("arial", 24, bold=True)
font_ui = pygame.font.SysFont("arial", 20, bold=True)

# --- 2. DATA LADEN ---
def load_data():
    with open("pokemon.json", "r") as f:
        return json.load(f)

pokemon_db = load_data()

# Kies twee Pokémon en geef ze stats (zoals in jouw originele code)
def setup_pokemon(data):
    p = data.copy()
    p["max_hp"] = 100
    p["current_hp"] = 100
    p["level"] = 5
    # We voegen standaard moves toe omdat die niet in de JSON staan
    p["moves"] = ["Tackle", "Quick Attack", "Growl", "Special Move"]
    
    # Laad sprite
    path = f"assets/{p['num']}.png"
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        p["sprite"] = pygame.transform.scale(img, (220, 220))
    else:
        surf = pygame.Surface((200, 200))
        surf.fill((255, 0, 255))
        p["sprite"] = surf
    return p

player = setup_pokemon(random.choice(pokemon_db))
enemy = setup_pokemon(random.choice(pokemon_db))

# --- 3. UI ELEMENTEN ---
menu_rect = pygame.Rect(0, 420, 800, 180)
move_buttons = [
    pygame.Rect(50, 450, 300, 50), pygame.Rect(450, 450, 300, 50),
    pygame.Rect(50, 520, 300, 50), pygame.Rect(450, 520, 300, 50)
]

# --- 4. FUNCTIES ---
def draw_hp_bar(x, y, current, maximum):
    pct = max(0, current / maximum)
    color = GREEN if pct > 0.5 else (YELLOW if pct > 0.2 else RED)
    pygame.draw.rect(screen, GRAY, (x, y, 200, 15)) # Achtergrond
    pygame.draw.rect(screen, color, (x, y, int(200 * pct), 15)) # HP
    pygame.draw.rect(screen, BLACK, (x, y, 200, 15), 2) # Rand

def attack(attacker, defender, move_name):
    damage = random.randint(10, 20)
    defender["current_hp"] -= damage
    return f"{attacker['name']} gebruikte {move_name}! -{damage} HP"

# --- 5. MAIN LOOP ---
running = True
battle_text = f"Een wilde {enemy['name']} verschijnt!"

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, rect in enumerate(move_buttons):
                    if rect.collidepoint(event.pos) and enemy["current_hp"] > 0:
                        # Speler valt aan
                        log1 = attack(player, enemy, player["moves"][i])
                        battle_text = log1
                        
                        # Vijand valt terug aan (na korte pauze of direct)
                        if enemy["current_hp"] > 0:
                            log2 = attack(enemy, player, random.choice(enemy["moves"]))
                            battle_text = log2

    # --- TEKENEN ---
    screen.fill((255, 255, 255))
    
    # Platformen
    pygame.draw.ellipse(screen, (230, 230, 230), (50, 350, 280, 100))
    pygame.draw.ellipse(screen, (230, 230, 230), (480, 180, 250, 80))

    # Pokémon Sprites
    screen.blit(player["sprite"], (80, 200))
    # De vijand sprite spiegelen we voor het effect
    enemy_sprite = pygame.transform.flip(enemy["sprite"], True, False)
    screen.blit(pygame.transform.scale(enemy_sprite, (180, 180)), (520, 60))

    # Namen & HP Balken
    # Vijand (linksboven)
    screen.blit(font_name.render(f"{enemy['name']} Lvl {enemy['level']}", True, BLACK), (50, 50))
    draw_hp_bar(50, 85, enemy["current_hp"], enemy["max_hp"])
    
    # Speler (rechtsonder)
    screen.blit(font_name.render(f"{player['name']} Lvl {player['level']}", True, BLACK), (500, 330))
    draw_hp_bar(500, 365, player["current_hp"], player["max_hp"])

    # UI Menu
    pygame.draw.rect(screen, (245, 245, 245), menu_rect)
    pygame.draw.line(screen, BLACK, (0, 420), (800, 420), 3)
    
    # Tekst log
    log_surf = font_ui.render(battle_text, True, BLACK)
    screen.blit(log_surf, (20, 425))

    # Knoppen
    for i, rect in enumerate(move_buttons):
        # Hover effect
        btn_color = (230, 230, 230) if rect.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(screen, btn_color, rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)
        
        move_label = font_ui.render(player["moves"][i], True, BLACK)
        label_rect = move_label.get_rect(center=rect.center)
        screen.blit(move_label, label_rect)

    # Check Game Over
    if enemy["current_hp"] <= 0:
        battle_text = f"{enemy['name']} is verslagen! Je wint!"
    elif player["current_hp"] <= 0:
        battle_text = "Je Pokémon is flauwgevallen... Verloren!"

    pygame.display.flip()
    clock.tick(60)

pygame.quit()