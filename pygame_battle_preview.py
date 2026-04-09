import pygame
import json
import random
import os
import sys

# --- 1. INITIALISATIE ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Adventure: The Final Masterpiece")
clock = pygame.time.Clock()

# Kleuren & Stijl
BG_LIGHT, HEADER_BLUE, WHITE = (240, 242, 245), (28, 100, 242), (255, 255, 255)
TEXT_DARK, ACCENT_GOLD = (17, 24, 39), (255, 191, 0)
SUCCESS_GREEN, DANGER_RED = (49, 196, 141), (249, 128, 128)
GRAY_TEXT = (75, 85, 99)
TOOLTIP_BG = (17, 24, 39)

TYPE_COLORS = {
    "Fire": (239, 68, 68),
    "Water": (59, 130, 246),
    "Grass": (34, 197, 94),
    "Normal": (156, 163, 175)
}

# --- 2. FONTS & ASSETS ---
font_main = pygame.font.SysFont("segoe ui", 20, bold=True)
font_title = pygame.font.SysFont("segoe ui", 32, bold=True)
font_small = pygame.font.SysFont("segoe ui", 13, bold=True)
font_tiny = pygame.font.SysFont("segoe ui", 11, bold=True)

def load_battle_background():
    path = os.path.join("assets", "background.png")
    if os.path.exists(path):
        img = pygame.image.load(path).convert()
        return pygame.transform.scale(img, (800, 450))
    return None

battle_bg_img = load_battle_background()

# --- 3. HELPER FUNCTIES ---
def draw_hp_bar(x, y, current, maximum):
    width = 230
    pygame.draw.rect(screen, (200, 200, 200), (x, y, width, 12), border_radius=6)
    pct = max(0, current / maximum)
    color = SUCCESS_GREEN if pct > 0.4 else (ACCENT_GOLD if pct > 0.15 else DANGER_RED)
    if pct > 0:
        pygame.draw.rect(screen, color, (x, y, int(width * pct), 12), border_radius=6)

def draw_type_icon(x, y, p_type):
    color = TYPE_COLORS.get(p_type, TYPE_COLORS["Normal"])
    rect = pygame.Rect(x, y, 65, 20)
    pygame.draw.rect(screen, color, rect, border_radius=5)
    txt = font_tiny.render(p_type.upper(), True, WHITE)
    screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

def draw_stat_icon(x, y, icon_type):
    if icon_type == "adv":
        pygame.draw.line(screen, WHITE, (x, y+10), (x+10, y), 2)
        pygame.draw.rect(screen, DANGER_RED, (x, y+8, 4, 4))
    else:
        pygame.draw.polygon(screen, (100, 149, 237), [(x, y), (x+10, y), (x+10, y+8), (x+5, y+11), (x, y+8)])

def draw_btn(text, rect, mouse_pos, color=HEADER_BLUE, active=True):
    is_h = rect.collidepoint(mouse_pos) and active
    if is_h: pygame.draw.rect(screen, WHITE, rect.inflate(6, 6), border_radius=14)
    c = [min(255, v + 40) for v in color] if is_h else (color if active else (160, 160, 160))
    pygame.draw.rect(screen, c, rect, border_radius=12)
    if text:
        txt = font_main.render(text, True, WHITE)
        screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
    return is_h

# --- 4. DATA LOGICA ---
def load_data():
    try:
        with open("pokemon.json", "r") as f: db = json.load(f)
        with open("trainers.json", "r") as f: t_data = json.load(f)
        return db, t_data
    except: return [], {"trainers": {}}

db, trainers_json = load_data()

def get_advantage_info(p_types):
    t = p_types[0] if p_types else "Normal"
    return {"Fire": "Grass", "Water": "Fire", "Grass": "Water"}.get(t, "None")

def get_move_type(move_name):
    types = {"Fire": ["Ember", "Flamethrower", "Fire Blast"], "Water": ["Water Gun", "Surf", "Hydro Pump"], "Grass": ["Vine Whip", "Razor Leaf", "Solar Beam"]}
    for t, moves in types.items():
        if move_name in moves: return t
    return "Normal"

def get_poke(base, diff):
    p = base.copy()
    hp = 120 if diff != "Hard" else 220
    p.update({"max_hp": hp, "current_hp": hp, "moves": ["Tackle", "Quick Attack", "Slam", "Scratch"]})
    if "Fire" in p.get("type", []): p["moves"] = ["Ember", "Flamethrower", "Fire Blast", "Quick Attack"]
    elif "Water" in p.get("type", []): p["moves"] = ["Water Gun", "Surf", "Hydro Pump", "Tackle"]
    elif "Grass" in p.get("type", []): p["moves"] = ["Vine Whip", "Razor Leaf", "Solar Beam", "Tackle"]
    path = f"assets/{p['num']}.png"
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        p["sprite"] = pygame.transform.scale(img, (220, 220))
    else:
        p["sprite"] = pygame.Surface((200, 200), pygame.SRCALPHA)
        pygame.draw.circle(p["sprite"], (200, 200, 200), (100, 100), 80)
    return p

# --- 5. BATTLE LOGICA ---
class Battle:
    def __init__(self, player_team, t_name, t_info, db):
        self.player_team = player_team
        self.enemy_team = [get_poke(random.choice(db), t_info.get("difficulty", "Easy")) for _ in range(6)]
        self.p_idx = next((i for i, pk in enumerate(player_team) if pk["current_hp"] > 0), 0)
        self.e_idx = 0
        self.log = f"Gevecht tegen {t_name}!"
        self.finished, self.winner = False, None
        self.prize_money = t_info.get("prize_money", 0)
        self.show_switch_menu = False

    def turn(self, move):
        if self.finished or self.player_team[self.p_idx]["current_hp"] <= 0: return
        p, e = self.player_team[self.p_idx], self.enemy_team[self.e_idx]
        
        m_type = get_move_type(move)
        mult = 2.0 if m_type in e.get("weaknesses", []) else 1.0
        dmg = int(random.randint(22, 30) * mult)
        e["current_hp"] = max(0, e["current_hp"] - dmg)
        self.log = f"{p['name']} gebruikt {move}! {'Super effectief!' if mult > 1 else ''}"

        if e["current_hp"] <= 0:
            if self.e_idx < 5:
                self.e_idx += 1
                self.log = f"Vijand KO! {self.enemy_team[self.e_idx]['name']} komt eraan."
            else:
                self.finished, self.winner = True, "player"
                self.log = "Winst! Alle vijanden verslagen."
            return
        
        dmg_in = random.randint(15, 25)
        p["current_hp"] = max(0, p["current_hp"] - dmg_in)
        if p["current_hp"] <= 0:
            self.log = f"{p['name']} is verslagen! WISSEL SNEL!"
            if not any(pk["current_hp"] > 0 for pk in self.player_team):
                self.finished, self.winner = True, "enemy"
                self.log = "Team verloren... Je hebt geen Pokémon meer."

# --- 6. INITIAL STATE ---
player_team = [get_poke(random.choice(db), "Easy") for _ in range(6)] if db else []
current_state = "MAIN_MENU"
wallet = 200
active_battle = None

# --- 7. MAIN LOOP ---
while True:
    screen.fill(BG_LIGHT)
    mouse = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if current_state == "MAIN_MENU":
                if pygame.Rect(275, 220, 250, 60).collidepoint(mouse): current_state = "TRAINER_MENU"
                if pygame.Rect(275, 300, 250, 60).collidepoint(mouse): current_state = "SHOP"
            
            elif current_state == "SHOP":
                if pygame.Rect(20, 25, 100, 45).collidepoint(mouse): 
                    current_state = "MAIN_MENU"
                # Klik op de Koop-knop of item kaart
                if pygame.Rect(100, 200, 600, 100).collidepoint(mouse) and wallet >= 200:
                    wallet -= 200
                    for pk in player_team:
                        pk["current_hp"] = pk["max_hp"]

            elif current_state == "TRAINER_MENU":
                if pygame.Rect(20, 25, 100, 45).collidepoint(mouse): current_state = "MAIN_MENU"
                for i, (name, info) in enumerate(trainers_json.get("trainers", {}).items()):
                    if pygame.Rect(50, 110 + i*130, 700, 100).collidepoint(mouse):
                        active_battle = Battle(player_team, name, info, db)
                        current_state = "BATTLE"

            elif current_state == "BATTLE":
                if active_battle.finished:
                    if pygame.Rect(250, 510, 300, 60).collidepoint(mouse):
                        if active_battle.winner == "player": wallet += active_battle.prize_money
                        current_state = "TRAINER_MENU"
                elif active_battle.show_switch_menu:
                    for i in range(6):
                        if pygame.Rect(50 + (i%2)*360, 470 + (i//2)*40, 340, 35).collidepoint(mouse):
                            if player_team[i]["current_hp"] > 0:
                                active_battle.p_idx = i; active_battle.show_switch_menu = False
                else:
                    if pygame.Rect(35, 520, 150, 45).collidepoint(mouse): active_battle.show_switch_menu = True
                    p_hp = active_battle.player_team[active_battle.p_idx]["current_hp"]
                    for i, move in enumerate(active_battle.player_team[active_battle.p_idx]["moves"]):
                        if pygame.Rect(380 + (i%2)*200, 475 + (i//2)*55, 185, 48).collidepoint(mouse) and p_hp > 0:
                            active_battle.turn(move)

    # --- SCHERMEN TEKENEN ---
    if current_state == "MAIN_MENU":
        pygame.draw.rect(screen, HEADER_BLUE, (0, 0, 800, 180))
        screen.blit(font_title.render("POKÉMON ADVENTURE", True, WHITE), (240, 70))
        draw_btn("TRAINER LIJST", pygame.Rect(275, 220, 250, 60), mouse)
        draw_btn("POKÉ MART", pygame.Rect(275, 300, 250, 60), mouse, SUCCESS_GREEN)
        screen.blit(font_main.render(f"Geld: ${wallet}", True, GRAY_TEXT), (350, 500))

    elif current_state == "SHOP":
        pygame.draw.rect(screen, SUCCESS_GREEN, (0, 0, 800, 95))
        draw_btn("TERUG", pygame.Rect(20, 25, 100, 45), mouse)
        screen.blit(font_title.render("POKÉ MART", True, WHITE), (320, 25))
        
        # Item Kaart
        item_rect = pygame.Rect(100, 200, 600, 100)
        draw_btn("", item_rect, mouse, WHITE) # Witte kaart
        pygame.draw.rect(screen, SUCCESS_GREEN, item_rect, 3, border_radius=12)
        
        screen.blit(font_main.render("TEAM FULL HEAL", True, TEXT_DARK), (130, 220))
        screen.blit(font_small.render("Herstel alle HP van je team naar 100%.", True, GRAY_TEXT), (130, 255))
        
        buy_color = SUCCESS_GREEN if wallet >= 200 else (160, 160, 160)
        draw_btn("$200", pygame.Rect(550, 225, 100, 50), mouse, buy_color)
        screen.blit(font_main.render(f"Beschikbaar geld: ${wallet}", True, TEXT_DARK), (100, 320))

    elif current_state == "TRAINER_MENU":
        pygame.draw.rect(screen, HEADER_BLUE, (0, 0, 800, 95))
        draw_btn("TERUG", pygame.Rect(20, 25, 100, 45), mouse)
        for i, (name, info) in enumerate(trainers_json.get("trainers", {}).items()):
            draw_btn(f"{name} [{info.get('pokemon_type')}] - ${info.get('prize_money')}", pygame.Rect(50, 110 + i*130, 700, 100), mouse)

    elif current_state == "BATTLE":
        p, e = active_battle.player_team[active_battle.p_idx], active_battle.enemy_team[active_battle.e_idx]
        if battle_bg_img: screen.blit(battle_bg_img, (0, 0))
        else: pygame.draw.rect(screen, (135, 206, 235), (0, 0, 800, 450))

        # Enemy UI
        pygame.draw.rect(screen, WHITE, (40, 40, 260, 115), border_radius=15)
        screen.blit(font_small.render(f"ENEMY: {e['name'].upper()}", True, TEXT_DARK), (55, 50))
        draw_type_icon(55, 75, e.get("type", ["Normal"])[0])
        draw_hp_bar(55, 115, e['current_hp'], e['max_hp'])

        # You UI
        pygame.draw.rect(screen, WHITE, (500, 300, 260, 115), border_radius=15)
        screen.blit(font_small.render(f"YOU: {p['name'].upper()}", True, TEXT_DARK), (515, 310))
        draw_type_icon(515, 335, p.get("type", ["Normal"])[0])
        draw_hp_bar(515, 375, p['current_hp'], p['max_hp'])

        # Sprites
        if e['current_hp'] > 0: screen.blit(pygame.transform.flip(e["sprite"], True, False), (500, 50))
        if p['current_hp'] > 0: screen.blit(p["sprite"], (150, 210))

        # Dialoog venster
        pygame.draw.rect(screen, WHITE, (0, 450, 800, 150))
        screen.blit(font_main.render(active_battle.log, True, TEXT_DARK), (35, 470))

        if active_battle.finished:
            draw_btn("GEVECHT VERLATEN", pygame.Rect(250, 510, 300, 60), mouse, ACCENT_GOLD)
        elif active_battle.show_switch_menu:
            pygame.draw.rect(screen, (240, 240, 240), (20, 460, 760, 130), border_radius=10)
            hovered_pk = None
            for i, pk in enumerate(active_battle.player_team):
                r = pygame.Rect(50 + (i%2)*360, 470 + (i//2)*40, 340, 35)
                is_h = draw_btn(f"{pk['name']} (HP: {int(pk['current_hp'])})", r, mouse, SUCCESS_GREEN if pk["current_hp"] > 0 else DANGER_RED)
                if is_h: hovered_pk = pk
            if hovered_pk:
                tx, ty = mouse[0]+15, mouse[1]-100
                pygame.draw.rect(screen, TOOLTIP_BG, (tx, ty, 180, 100), border_radius=10)
                draw_type_icon(tx+10, ty+10, hovered_pk.get("type", ["Normal"])[0])
                draw_stat_icon(tx+10, ty+45, "adv")
                screen.blit(font_tiny.render(f"STERK: {get_advantage_info(hovered_pk.get('type'))}", True, SUCCESS_GREEN), (tx+25, ty+42))
                draw_stat_icon(tx+10, ty+70, "weak")
                screen.blit(font_tiny.render(f"ZWAK: {hovered_pk.get('weaknesses',['None'])[0]}", True, DANGER_RED), (tx+25, ty+67))
        else:
            draw_btn("WISSEL", pygame.Rect(35, 520, 150, 45), mouse)
            p_alive = p['current_hp'] > 0
            for i, m in enumerate(p["moves"]):
                r = pygame.Rect(380 + (i%2)*200, 475 + (i//2)*55, 185, 48)
                draw_btn(m, r, mouse, HEADER_BLUE, active=p_alive)

    pygame.display.flip()
    clock.tick(60)