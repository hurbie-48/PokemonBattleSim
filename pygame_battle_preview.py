import pygame
import json
import random
import os
import sys

# --- 1. INITIALISATIE ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Battle: Trainer Edition")
clock = pygame.time.Clock()

# Kleuren
BG_LIGHT, HEADER_BLUE, WHITE = (240, 242, 245), (28, 100, 242), (255, 255, 255)
TEXT_DARK, ACCENT_GOLD = (17, 24, 39), (255, 191, 0)
SUCCESS_GREEN, DANGER_RED = (49, 196, 141), (249, 128, 128)
GRAY_TEXT = (75, 85, 99) # Iets donkerder voor betere leesbaarheid

# Fonts
font_main = pygame.font.SysFont("segoe ui", 20, bold=True)
font_title = pygame.font.SysFont("segoe ui", 32, bold=True)
font_desc = pygame.font.SysFont("segoe ui", 16, italic=True)
font_small = pygame.font.SysFont("segoe ui", 14)

# --- 2. DATA & ASSETS ---
def load_battle_background():
    bg_path = "assets/background.png"
    if os.path.exists(bg_path):
        img = pygame.image.load(bg_path).convert()
        return pygame.transform.scale(img, (800, 450))
    return None

battle_bg_img = load_battle_background()

def load_data():
    try:
        with open("pokemon.json", "r") as f: db = json.load(f)
        with open("trainers.json", "r") as f: t_data = json.load(f)
        return db, t_data
    except Exception as e:
        print(f"Laadfout: {e}")
        return [], {"trainers": {}}

def get_poke(base, diff):
    p = base.copy()
    hp = 100
    if diff == "Hard": hp = 180
    if diff == "Impossible": hp = 600
    p["name"] = str(p.get("name", "Onbekend"))
    p.update({"max_hp": hp, "current_hp": hp, "moves": ["Tackle", "Bite", "Beam", "Pulse"]})
    path = f"assets/{p['num']}.png"
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        p["sprite"] = pygame.transform.scale(img, (220, 220))
    else:
        p["sprite"] = pygame.Surface((200, 200), pygame.SRCALPHA)
    return p

# --- 3. BATTLE MANAGER ---
class Battle:
    def __init__(self, player_team, t_name, t_info, db):
        self.player_team = player_team
        self.trainer_name = t_name
        self.difficulty = t_info.get("difficulty", "Easy")
        self.prize_money = t_info.get("prize_money", 0)
        self.enemy_team = [get_poke(random.choice(db), self.difficulty) for _ in range(6)]
        self.p_idx, self.e_idx = 0, 0
        self.log = f"Gevecht tegen {t_name} gestart!"
        self.finished, self.winner = False, None

    def turn(self, move):
        if self.finished: return
        p, e = self.player_team[self.p_idx], self.enemy_team[self.e_idx]
        
        # Player Attack
        dmg = random.randint(25, 40)
        e["current_hp"] -= dmg
        self.log = f"{p['name']} valt aan met {move}!"

        if e["current_hp"] <= 0:
            e["current_hp"] = 0
            self.e_idx += 1
            if self.e_idx >= 6:
                self.finished, self.winner = True, "player"
                self.log = "Overwinning! Je krijgt het prijzengeld."
            return

        # Enemy Attack
        dmg_e = random.randint(15, 30)
        p["current_hp"] -= dmg_e
        if p["current_hp"] <= 0:
            p["current_hp"] = 0
            self.p_idx += 1
            if self.p_idx >= 6:
                self.finished, self.winner = True, "enemy"
                self.log = "Helaas... Je team is verslagen."

# --- 4. INITIAL SETUP ---
db, trainers_json = load_data()
player_team = [get_poke(random.choice(db), "Easy") for _ in range(6)]
current_state = "MENU"
scroll_y, wallet_money, active_battle = 0, 0, None
max_scroll = min(0, HEIGHT - (len(trainers_json.get("trainers", {})) * 130) - 120)

# --- 5. MAIN LOOP ---
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
                        if rect.collidepoint(mouse) and rect.top > 85:
                            active_battle = Battle(player_team, name, info, db)
                            current_state = "BATTLE"
                elif current_state == "BATTLE":
                    if active_battle.finished:
                        if active_battle.winner == "player": 
                            wallet_money += active_battle.prize_money
                        for p in player_team: p["current_hp"] = p["max_hp"]
                        current_state = "MENU"
                    else:
                        for r, m in move_btns:
                            if r.collidepoint(mouse): active_battle.turn(m)

    # --- TEKEN MENU ---
    if current_state == "MENU":
        for i, (name, info) in enumerate(trainers_json.get("trainers", {}).items()):
            y_pos = 110 + i*130 + scroll_y
            card_rect = pygame.Rect(50, y_pos, 700, 110)
            
            if card_rect.bottom > 90: # Alleen tekenen als het onder de header uitkomt
                hover = card_rect.collidepoint(mouse) and card_rect.top > 90
                pygame.draw.rect(screen, WHITE if not hover else (240, 248, 255), card_rect, border_radius=15)
                pygame.draw.rect(screen, (200, 210, 230), card_rect, 2, border_radius=15)
                
                # Trainer Naam
                screen.blit(font_main.render(name, True, HEADER_BLUE), (75, y_pos + 15))
                
                # Moeilijkheidsgraad
                diff = info.get("difficulty", "Normal")
                diff_col = DANGER_RED if diff in ["Hard", "Impossible"] else SUCCESS_GREEN
                screen.blit(font_small.render(f"Niveau: {diff}", True, diff_col), (75, y_pos + 42))
                
                # BESCHRIJVING (Description)
                description = info.get("description", "Een trainer die klaar is voor de strijd.")
                # Tekst inkorten als deze te lang is voor de kaart
                if len(description) > 75: description = description[:72] + "..."
                screen.blit(font_desc.render(description, True, GRAY_TEXT), (75, y_pos + 68))
                
                # GELD (Prijs per trainer)
                money_txt = font_title.render(f"${info.get('prize_money', 0)}", True, ACCENT_GOLD)
                screen.blit(money_txt, (WIDTH - money_txt.get_width() - 80, y_pos + 30))

        # STICKY HEADER
        pygame.draw.rect(screen, HEADER_BLUE, (0, 0, 800, 95))
        screen.blit(font_title.render("Trainer Selectie", True, WHITE), (30, 28))
        
        # TOTALE WALLET GELD
        wallet_txt = font_main.render(f"Totaal Geld: ${wallet_money}", True, ACCENT_GOLD)
        screen.blit(wallet_txt, (WIDTH - wallet_txt.get_width() - 30, 38))

    # --- TEKEN BATTLE ---
    elif current_state == "BATTLE":
        if battle_bg_img: screen.blit(battle_bg_img, (0, 0))
        else: pygame.draw.rect(screen, (100, 150, 255), (0, 0, 800, 450))

        p_idx, e_idx = min(active_battle.p_idx, 5), min(active_battle.e_idx, 5)
        p, e = active_battle.player_team[p_idx], active_battle.enemy_team[e_idx]
        
        screen.blit(p["sprite"], (90, 210))
        screen.blit(pygame.transform.flip(e["sprite"], True, False), (530, 45))

        # HUD Enemy
        pygame.draw.rect(screen, WHITE, (40, 40, 260, 85), border_radius=12)
        screen.blit(font_main.render(e["name"].upper(), True, TEXT_DARK), (55, 52))
        pct_e = max(0, e["current_hp"] / e["max_hp"])
        pygame.draw.rect(screen, (230, 230, 230), (55, 88, 200, 15), border_radius=8)
        pygame.draw.rect(screen, SUCCESS_GREEN if pct_e > 0.4 else DANGER_RED, (55, 88, int(200*pct_e), 15), border_radius=8)

        # HUD Player
        pygame.draw.rect(screen, WHITE, (500, 340, 260, 85), border_radius=12)
        screen.blit(font_main.render(p["name"].upper(), True, TEXT_DARK), (515, 352))
        pct_p = max(0, p["current_hp"] / p["max_hp"])
        pygame.draw.rect(screen, (230, 230, 230), (515, 388, 200, 15), border_radius=8)
        pygame.draw.rect(screen, SUCCESS_GREEN if pct_p > 0.4 else DANGER_RED, (515, 388, int(200*pct_p), 15), border_radius=8)

        # UI ONDERIN
        pygame.draw.rect(screen, WHITE, (0, 450, 800, 150))
        pygame.draw.line(screen, HEADER_BLUE, (0, 450), (800, 450), 4)
        screen.blit(font_main.render(active_battle.log, True, HEADER_BLUE), (35, 475))
        
        move_btns = []
        if not active_battle.finished:
            for i, m in enumerate(p["moves"]):
                br = pygame.Rect(450 + (i%2)*165, 485 + (i//2)*55, 155, 48)
                h = br.collidepoint(mouse)
                pygame.draw.rect(screen, HEADER_BLUE if h else (240, 245, 255), br, border_radius=12)
                txt = font_main.render(m, True, WHITE if h else HEADER_BLUE)
                screen.blit(txt, (br.centerx - txt.get_width()//2, br.centery - txt.get_height()//2))
                move_btns.append((br, m))
        else:
            btn = pygame.Rect(300, 500, 200, 55)
            pygame.draw.rect(screen, ACCENT_GOLD, btn, border_radius=12)
            screen.blit(font_main.render("VERLATEN", True, WHITE), (355, 515))

    pygame.display.flip()
    clock.tick(60)