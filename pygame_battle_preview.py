import pygame
import json
import random
import os
import sys

# --- 1. INITIALISATIE ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Battle: Shop & Data Edition")
clock = pygame.time.Clock()

# Kleuren
BG_LIGHT, HEADER_BLUE, WHITE = (240, 242, 245), (28, 100, 242), (255, 255, 255)
TEXT_DARK, ACCENT_GOLD = (17, 24, 39), (255, 191, 0)
SUCCESS_GREEN, DANGER_RED = (49, 196, 141), (249, 128, 128)
GRAY_TEXT = (75, 85, 99)
BUTTON_COLOR = (59, 130, 246)
BUTTON_HOVER = (37, 99, 235)

# --- 2. ASSETS & FONTS ---
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

# --- 3. LOGICA & DATA ---
def load_data():
    try:
        with open("pokemon.json", "r") as f: db = json.load(f)
        with open("trainers.json", "r") as f: t_data = json.load(f)
        return db, t_data
    except:
        print("Bestanden missen! Zorg voor pokemon.json en trainers.json")
        return [], {"trainers": {}}

db, trainers_json = load_data()

def get_move_type(move_name):
    types = {
        "Fire": ["Ember", "Flamethrower", "Fire Blast"],
        "Water": ["Water Gun", "Surf", "Hydro Pump", "Bubble"],
        "Grass": ["Vine Whip", "Razor Leaf", "Solar Beam", "Absorb"],
        "Electric": ["Thunder Shock", "Thunderbolt"]
    }
    for t, moves in types.items():
        if move_name in moves: return t
    return "Normal"

def get_moves_by_type(p_types):
    if "Fire" in p_types: return ["Ember", "Flamethrower", "Quick Attack", "Tackle"]
    if "Water" in p_types: return ["Water Gun", "Surf", "Bubble", "Tackle"]
    if "Grass" in p_types: return ["Vine Whip", "Razor Leaf", "Absorb", "Tackle"]
    return ["Tackle", "Quick Attack", "Slam", "Scratch"]

def get_poke(base, diff):
    p = base.copy()
    hp = 120 if diff != "Hard" else 220
    p.update({"max_hp": hp, "current_hp": hp, "moves": get_moves_by_type(p.get("type", ["Normal"]))})
    path = f"assets/{p['num']}.png"
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        p["sprite"] = pygame.transform.scale(img, (220, 220))
    else:
        p["sprite"] = pygame.Surface((200, 200), pygame.SRCALPHA)
        pygame.draw.circle(p["sprite"], (200, 200, 200), (100, 100), 80)
    return p

# --- 4. BATTLE CLASS ---
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
        
        # Speler beurt
        dmg, msg = self.calc_dmg(move, e)
        e["current_hp"] -= dmg
        self.log = f"{p['name']} gebruikt {move}! {msg}"

        if e["current_hp"] <= 0:
            e["current_hp"] = 0
            self.e_idx += 1
            if self.e_idx >= 6: self.finished, self.winner = True, "player"
            return

        # Vijand beurt
        e_move = random.choice(e["moves"])
        dmg_e, msg_e = self.calc_dmg(e_move, p)
        p["current_hp"] -= dmg_e
        if p["current_hp"] <= 0:
            p["current_hp"] = 0
            self.p_idx += 1
            if self.p_idx >= 6: self.finished, self.winner = True, "enemy"

    def calc_dmg(self, move, defender):
        m_type = get_move_type(move)
        mult = 2.0 if m_type in defender.get("weaknesses", []) else 1.0
        return int(random.randint(18, 28) * mult), ("Super effectief!" if mult > 1 else "")

# --- 5. UI FUNCTIES ---
def draw_btn(text, rect, mouse_pos, color=BUTTON_COLOR):
    h = rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, BUTTON_HOVER if h else color, rect, border_radius=12)
    t = font_main.render(text, True, WHITE)
    screen.blit(t, (rect.centerx - t.get_width()//2, rect.centery - t.get_height()//2))
    return h

# --- 6. INITIAL STATE ---
player_team = [get_poke(random.choice(db), "Easy") for _ in range(6)] if db else []
current_state = "INTRO"
wallet = 0
scroll_y = 0
active_battle = None
max_scroll = min(0, HEIGHT - (len(trainers_json.get("trainers", {})) * 130) - 150)

# --- 7. MAIN LOOP ---
while True:
    screen.fill(BG_LIGHT)
    mouse = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if current_state == "INTRO": current_state = "MAIN_MENU"
            
            elif current_state == "MAIN_MENU":
                if pygame.Rect(WIDTH//2-125, 200, 250, 60).collidepoint(mouse): current_state = "MENU"
                if pygame.Rect(WIDTH//2-125, 280, 250, 60).collidepoint(mouse): current_state = "SHOP"
                if pygame.Rect(WIDTH//2-125, 360, 250, 60).collidepoint(mouse): pygame.quit(); sys.exit()

            elif current_state == "SHOP":
                if pygame.Rect(20, 25, 100, 45).collidepoint(mouse): current_state = "MAIN_MENU"
                # Heal Team ($200)
                if pygame.Rect(100, 200, 600, 80).collidepoint(mouse) and wallet >= 200:
                    wallet -= 200
                    for pk in player_team: pk["current_hp"] = pk["max_hp"]
                # Power Up ($500)
                if pygame.Rect(100, 300, 600, 80).collidepoint(mouse) and wallet >= 500:
                    wallet -= 500
                    for pk in player_team: pk["max_hp"] += 20; pk["current_hp"] += 20

            elif current_state == "MENU":
                if pygame.Rect(20, 25, 100, 45).collidepoint(mouse): current_state = "MAIN_MENU"
                for i, (name, info) in enumerate(trainers_json.get("trainers", {}).items()):
                    r = pygame.Rect(50, 110 + i*130 + scroll_y, 700, 110)
                    if r.collidepoint(mouse) and r.top > 90:
                        active_battle = Battle(player_team, name, info, db)
                        current_state = "BATTLE"

            elif current_state == "BATTLE":
                if active_battle.finished:
                    if active_battle.winner == "player": wallet += active_battle.prize_money
                    current_state = "MENU"
                else:
                    for r, m in move_btns:
                        if r.collidepoint(mouse): active_battle.turn(m)

        if event.type == pygame.MOUSEBUTTONDOWN and current_state == "MENU":
            if event.button == 4: scroll_y = min(0, scroll_y + 50)
            if event.button == 5: scroll_y = max(max_scroll, scroll_y - 50)

    # --- RENDERING PER STATE ---
    if current_state == "INTRO":
        screen.fill(HEADER_BLUE)
        txt = font_title.render("POKÉMON JSON BATTLES", True, WHITE)
        screen.blit(txt, (WIDTH//2-txt.get_width()//2, 250))
        if pygame.time.get_ticks() % 1000 < 500:
            s = font_main.render("KLIK OM TE STARTEN", True, ACCENT_GOLD)
            screen.blit(s, (WIDTH//2-s.get_width()//2, 400))

    elif current_state == "MAIN_MENU":
        pygame.draw.rect(screen, HEADER_BLUE, (0, 0, 800, 150))
        screen.blit(font_title.render("HOOFDMENU", True, WHITE), (300, 55))
        draw_btn("VECHTEN", pygame.Rect(WIDTH//2-125, 200, 250, 60), mouse)
        draw_btn("POKÉ MART", pygame.Rect(WIDTH//2-125, 280, 250, 60), mouse, SUCCESS_GREEN)
        draw_btn("STOPPEN", pygame.Rect(WIDTH//2-125, 360, 250, 60), mouse, DANGER_RED)
        screen.blit(font_main.render(f"Kapitaal: ${wallet}", True, GRAY_TEXT), (340, 480))

    elif current_state == "SHOP":
        pygame.draw.rect(screen, SUCCESS_GREEN, (0, 0, 800, 95))
        draw_btn("TERUG", pygame.Rect(20, 25, 100, 45), mouse, (30, 150, 100))
        screen.blit(font_title.render(f"POKÉ MART - Saldo: ${wallet}", True, WHITE), (150, 28))
        
        # Shop Items
        draw_btn("GENEES TEAM ($200)", pygame.Rect(100, 200, 600, 80), mouse)
        draw_btn("TEAM POWER UP +20 HP ($500)", pygame.Rect(100, 300, 600, 80), mouse)

    elif current_state == "MENU":
        for i, (name, info) in enumerate(trainers_json.get("trainers", {}).items()):
            y = 110 + i*130 + scroll_y
            r = pygame.Rect(50, y, 700, 110)
            if r.bottom > 95:
                h = r.collidepoint(mouse) and r.top > 95
                pygame.draw.rect(screen, WHITE if not h else (240, 250, 255), r, border_radius=15)
                pygame.draw.rect(screen, (200, 210, 230), r, 2, border_radius=15)
                screen.blit(font_main.render(name, True, HEADER_BLUE), (75, y+15))
                screen.blit(font_desc.render(info.get("description", ""), True, GRAY_TEXT), (75, y+65))
                screen.blit(font_title.render(f"${info.get('prize_money', 0)}", True, ACCENT_GOLD), (600, y+30))
        pygame.draw.rect(screen, HEADER_BLUE, (0, 0, 800, 95))
        draw_btn("TERUG", pygame.Rect(20, 25, 100, 45), mouse, (40, 80, 200))
        screen.blit(font_title.render("Trainer Selectie", True, WHITE), (150, 28))

    elif current_state == "BATTLE":
        if battle_bg_img: screen.blit(battle_bg_img, (0, 0))
        else: pygame.draw.rect(screen, (135, 206, 235), (0, 0, 800, 450))
        p, e = active_battle.player_team[min(active_battle.p_idx, 5)], active_battle.enemy_team[min(active_battle.e_idx, 5)]
        screen.blit(p["sprite"], (90, 210))
        screen.blit(pygame.transform.flip(e["sprite"], True, False), (530, 45))
        
        for x, y, pk in [(40, 40, e), (500, 340, p)]:
            pygame.draw.rect(screen, WHITE, (x, y, 260, 85), border_radius=12)
            screen.blit(font_main.render(pk["name"].upper(), True, TEXT_DARK), (x+15, y+12))
            pct = max(0, pk["current_hp"]/pk["max_hp"])
            pygame.draw.rect(screen, (230, 230, 230), (x+15, y+48, 200, 15), border_radius=8)
            pygame.draw.rect(screen, SUCCESS_GREEN if pct > 0.4 else DANGER_RED, (x+15, y+48, int(200*pct), 15), border_radius=8)

        pygame.draw.rect(screen, WHITE, (0, 450, 800, 150))
        pygame.draw.line(screen, HEADER_BLUE, (0, 450), (800, 450), 4)
        screen.blit(font_main.render(active_battle.log, True, HEADER_BLUE), (35, 475))
        
        move_btns = []
        if not active_battle.finished:
            for i, m in enumerate(p["moves"]):
                br = pygame.Rect(450 + (i%2)*165, 485 + (i//2)*55, 155, 48)
                h = draw_btn(m, br, mouse, (240, 245, 255))
                screen.blit(font_main.render(m, True, WHITE if h else HEADER_BLUE), (br.centerx-30, br.centery-10))
                move_btns.append((br, m))
        else:
            if draw_btn("GEVECHT KLAAR", pygame.Rect(300, 500, 200, 55), mouse, ACCENT_GOLD): pass

    pygame.display.flip()
    clock.tick(60)