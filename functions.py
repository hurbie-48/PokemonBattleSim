import pygame
import json
import random
import os
import sys

# --- 1. CONFIGURATIE & TYPES ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Battle: Elemental Masters")
clock = pygame.time.Clock()

# Kleuren
BG_LIGHT, HEADER_BLUE, WHITE = (240, 242, 245), (28, 100, 242), (255, 255, 255)
TEXT_DARK, ACCENT_GOLD = (17, 24, 39), (255, 191, 0)
SUCCESS_GREEN, DANGER_RED = (49, 196, 141), (249, 128, 128)
GRAY_TEXT = (75, 85, 99)

# Type Chart (Aanvaller: {Verdediger: Multiplier})
TYPE_CHART = {
    "Fire":     {"Grass": 2.0, "Water": 0.5, "Fire": 0.5, "Bug": 2.0, "Ice": 2.0},
    "Water":    {"Fire": 2.0, "Grass": 0.5, "Water": 0.5, "Ground": 2.0, "Rock": 2.0},
    "Grass":    {"Water": 2.0, "Fire": 0.5, "Grass": 0.5, "Ground": 2.0, "Poison": 0.5},
    "Electric": {"Water": 2.0, "Flying": 2.0, "Grass": 0.5, "Electric": 0.5, "Ground": 0.0},
    "Normal":   {"Rock": 0.5, "Steel": 0.5}
}

# --- 2. FONTS & ASSETS ---
font_main = pygame.font.SysFont("segoe ui", 20, bold=True)
font_title = pygame.font.SysFont("segoe ui", 32, bold=True)
font_desc = pygame.font.SysFont("segoe ui", 16, italic=True)
font_small = pygame.font.SysFont("segoe ui", 14)

def load_battle_background():
    path = "assets/background.png"
    if os.path.exists(path):
        img = pygame.image.load(path).convert()
        return pygame.transform.scale(img, (800, 450))
    return None

battle_bg_img = load_battle_background()

# --- 3. LOGICA FUNCTIES ---
def get_moves_for_type(p_types):
    move_pool = {
        "Fire": ["Ember", "Flamethrower", "Fire Blast"],
        "Water": ["Water Gun", "Surf", "Hydro Pump"],
        "Grass": ["Vine Whip", "Razor Leaf", "Solar Beam"],
        "Electric": ["Thunder Shock", "Thunderbolt", "Thunder"],
        "Normal": ["Tackle", "Quick Attack", "Hyper Beam"]
    }
    main_type = p_types[0] if p_types else "Normal"
    moves = random.sample(move_pool.get(main_type, move_pool["Normal"]), 2)
    moves += random.sample(move_pool["Normal"], 2)
    return moves

def get_move_type(move_name):
    fire = ["Ember", "Flamethrower", "Fire Blast"]
    water = ["Water Gun", "Surf", "Hydro Pump"]
    grass = ["Vine Whip", "Razor Leaf", "Solar Beam"]
    elec = ["Thunder Shock", "Thunderbolt", "Thunder"]
    if move_name in fire: return "Fire"
    if move_name in water: return "Water"
    if move_name in grass: return "Grass"
    if move_name in elec: return "Electric"
    return "Normal"

def calculate_damage(move, defender_types):
    m_type = get_move_type(move)
    mult = 1.0
    for dt in defender_types:
        if m_type in TYPE_CHART and dt in TYPE_CHART[m_type]:
            mult *= TYPE_CHART[m_type][dt]
    
    dmg = int(random.randint(22, 35) * mult)
    msg = ""
    if mult > 1.0: msg = "Super effectief!"
    elif mult < 1.0 and mult > 0: msg = "Niet erg effectief..."
    elif mult == 0: msg = "Geen effect..."
    return dmg, msg

def load_data():
    try:
        with open("pokemon.json", "r") as f: db = json.load(f)
        with open("trainers.json", "r") as f: t_data = json.load(f)
        return db, t_data
    except: return [], {"trainers": {}}

def get_poke(base, diff):
    p = base.copy()
    p_types = p.get("type", ["Normal"])
    hp = 120 if diff != "Hard" else 200
    p.update({
        "max_hp": hp, "current_hp": hp, 
        "types": p_types, "moves": get_moves_for_type(p_types),
        "name": str(p.get("name", "Onbekend"))
    })
    path = f"assets/{p['num']}.png"
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        p["sprite"] = pygame.transform.scale(img, (220, 220))
    else:
        p["sprite"] = pygame.Surface((200, 200), pygame.SRCALPHA)
    return p

# --- 4. BATTLE MANAGER ---
class Battle:
    def __init__(self, player_team, t_name, t_info, db):
        self.player_team = player_team
        self.difficulty = t_info.get("difficulty", "Easy")
        self.enemy_team = [get_poke(random.choice(db), self.difficulty) for _ in range(6)]
        self.p_idx, self.e_idx = 0, 0
        self.log = f"Gevecht tegen {t_name}!"
        self.finished, self.winner = False, None
        self.prize_money = t_info.get("prize_money", 0)

    def turn(self, move):
        if self.finished: return
        p, e = self.player_team[self.p_idx], self.enemy_team[self.e_idx]
        
        # Player Turn
        dmg, msg = calculate_damage(move, e["types"])
        e["current_hp"] -= dmg
        self.log = f"{p['name']} gebruikt {move}! {msg}"

        if e["current_hp"] <= 0:
            self.e_idx += 1
            if self.e_idx >= 6: self.finished, self.winner = True, "player"
            return

        # Enemy Turn
        e_move = random.choice(e["moves"])
        dmg_e, msg_e = calculate_damage(e_move, p["types"])
        p["current_hp"] -= dmg_e
        if p["current_hp"] <= 0:
            self.p_idx += 1
            if self.p_idx >= 6: self.finished, self.winner = True, "enemy"

# --- 5. MAIN LOOP ---
db, trainers_json = load_data()
player_team = [get_poke(random.choice(db), "Easy") for _ in range(6)]
current_state = "MENU"
scroll_y, wallet, active_battle = 0, 0, None
max_scroll = min(0, HEIGHT - (len(trainers_json.get("trainers", {})) * 130) - 120)

while True:
    screen.fill(BG_LIGHT)
    mouse = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: scroll_y = min(0, scroll_y + 50)
            if event.button == 5: scroll_y = max(max_scroll, scroll_y - 50)
            if event.button == 1:
                if current_state == "MENU":
                    for i, (name, info) in enumerate(trainers_json.get("trainers", {}).items()):
                        rect = pygame.Rect(50, 110 + i*130 + scroll_y, 700, 110)
                        if rect.collidepoint(mouse) and rect.top > 90:
                            active_battle = Battle(player_team, name, info, db)
                            current_state = "BATTLE"
                elif current_state == "BATTLE":
                    if active_battle.finished:
                        if active_battle.winner == "player": wallet += active_battle.prize_money
                        for pk in player_team: pk["current_hp"] = pk["max_hp"]
                        current_state = "MENU"
                    else:
                        for r, m in move_btns:
                            if r.collidepoint(mouse): active_battle.turn(m)

    if current_state == "MENU":
        for i, (name, info) in enumerate(trainers_json.get("trainers", {}).items()):
            y = 110 + i*130 + scroll_y
            rect = pygame.Rect(50, y, 700, 110)
            if rect.bottom > 95:
                hover = rect.collidepoint(mouse) and rect.top > 95
                pygame.draw.rect(screen, WHITE if not hover else (240, 250, 255), rect, border_radius=15)
                pygame.draw.rect(screen, (200, 210, 230), rect, 2, border_radius=15)
                screen.blit(font_main.render(name, True, HEADER_BLUE), (75, y + 15))
                screen.blit(font_desc.render(info.get("description", ""), True, GRAY_TEXT), (75, y + 65))
                screen.blit(font_title.render(f"${info.get('prize_money', 0)}", True, ACCENT_GOLD), (600, y + 30))

        pygame.draw.rect(screen, HEADER_BLUE, (0, 0, 800, 95))
        screen.blit(font_title.render("Trainer Selectie", True, WHITE), (30, 28))
        wallet_txt = font_main.render(f"Wallet: ${wallet}", True, ACCENT_GOLD)
        screen.blit(wallet_txt, (WIDTH - wallet_txt.get_width() - 30, 38))

    elif current_state == "BATTLE":
        if battle_bg_img: screen.blit(battle_bg_img, (0, 0))
        else: pygame.draw.rect(screen, (135, 206, 235), (0, 0, 800, 450))

        p_idx, e_idx = min(active_battle.p_idx, 5), min(active_battle.e_idx, 5)
        p, e = active_battle.player_team[p_idx], active_battle.enemy_team[e_idx]
        screen.blit(p["sprite"], (90, 210))
        screen.blit(pygame.transform.flip(e["sprite"], True, False), (530, 45))

        # HUDs
        for x, y, poke, align in [(40, 40, e, "L"), (500, 340, p, "R")]:
            pygame.draw.rect(screen, WHITE, (x, y, 260, 85), border_radius=12)
            screen.blit(font_main.render(poke["name"].upper(), True, TEXT_DARK), (x+15, y+12))
            pct = max(0, poke["current_hp"] / poke["max_hp"])
            pygame.draw.rect(screen, (230, 230, 230), (x+15, y+48, 200, 15), border_radius=8)
            pygame.draw.rect(screen, SUCCESS_GREEN if pct > 0.4 else DANGER_RED, (x+15, y+48, int(200*pct), 15), border_radius=8)

        pygame.draw.rect(screen, WHITE, (0, 450, 800, 150))
        pygame.draw.line(screen, HEADER_BLUE, (0, 450), (800, 450), 4)
        screen.blit(font_main.render(active_battle.log, True, HEADER_BLUE), (35, 475))
        
        move_btns = []
        if not active_battle.finished:
            for i, m in enumerate(p["moves"]):
                br = pygame.Rect(450 + (i%2)*165, 485 + (i//2)*55, 155, 48)
                pygame.draw.rect(screen, HEADER_BLUE if br.collidepoint(mouse) else (240, 245, 255), br, border_radius=12)
                txt = font_main.render(m, True, WHITE if br.collidepoint(mouse) else HEADER_BLUE)
                screen.blit(txt, (br.centerx - txt.get_width()//2, br.centery - txt.get_height()//2))
                move_btns.append((br, m))
        else:
            btn = pygame.Rect(300, 500, 200, 55)
            pygame.draw.rect(screen, ACCENT_GOLD, btn, border_radius=12)
            screen.blit(font_main.render("KLAAR", True, WHITE), (365, 515))

    pygame.display.flip()
    clock.tick(60)