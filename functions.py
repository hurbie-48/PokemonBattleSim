import pygame
import random
import json
import os

# --- 1. INITIALISATIE & CLASSES ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Battle Simulator")
clock = pygame.time.Clock()

# Kleuren & Fonts
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)
BLUE, GOLD, RED = (0, 102, 204), (255, 215, 0), (200, 0, 0)
font_title = pygame.font.SysFont("arial", 50, bold=True)
font_std = pygame.font.SysFont("arial", 22)
font_bold = pygame.font.SysFont("arial", 22, bold=True)

# --- 2. GAME STATE MANAGER ---
class GameState:
    MENU = 0
    TRAINER_SELECT = 1
    BATTLE = 2
    GAME_OVER = 3

class Game:
    def __init__(self):
        self.state = GameState.MENU
        self.money = 20
        self.player_name = ""
        self.trainers = self.load_trainers()
        self.selected_trainer = None
        self.player_team = self.get_random_team(6)
        
    def load_trainers(self):
        # Dummy data gebaseerd op jouw JSON structuur
        return [
            {"name": "Joey", "desc": "Houdt van Rattata", "bounty": 100, "beaten": False},
            {"name": "Brock", "desc": "Rots-vaste trainer", "bounty": 500, "beaten": False},
            {"name": "Misty", "desc": "Water-specialist", "bounty": 450, "beaten": False}
        ]

    def get_random_team(self, count):
        # Hier laad je normaal je Pokemon class
        return [{"name": "Starter", "hp": 100, "max_hp": 100} for _ in range(count)]

game = Game()

# --- 3. SCHERM FUNCTIES ---

def draw_welcome():
    screen.fill(BLUE)
    title = font_title.render("POKÉMON BATTLE SIM", True, WHITE)
    instr = font_std.render("Druk op SPATIE om de trainer naam in te voeren", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
    screen.blit(instr, (WIDTH//2 - instr.get_width()//2, 400))

def draw_trainer_select():
    screen.fill((240, 240, 240))
    header = font_bold.render(f"Welkom Trainer! | Geld: ${game.money}", True, BLACK)
    screen.blit(header, (50, 30))
    
    subtitle = font_std.render("Kies een trainer om uit te dagen:", True, BLACK)
    screen.blit(subtitle, (50, 70))

    for i, t in enumerate(game.trainers):
        if not t["beaten"]:
            rect = pygame.Rect(50, 120 + (i * 90), 700, 70)
            pygame.draw.rect(screen, WHITE, rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, rect, 2, border_radius=10)
            
            name_txt = font_bold.render(f"TRAINER: {t['name']}", True, BLUE)
            desc_txt = font_std.render(t["desc"], True, BLACK)
            bounty_txt = font_bold.render(f"${t['bounty']}", True, (150, 150, 0))
            
            screen.blit(name_txt, (70, 130 + (i * 90)))
            screen.blit(desc_txt, (70, 155 + (i * 90)))
            screen.blit(bounty_txt, (680, 140 + (i * 90)))
            t["rect"] = rect # Opslaan voor klik-detectie

def draw_battle_placeholder():
    screen.fill(BLACK)
    txt = font_title.render(f"BATTLE VS {game.selected_trainer['name']}", True, RED)
    screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 200))
    instr = font_std.render("Druk op 'W' om te winnen (test)", True, WHITE)
    screen.blit(instr, (WIDTH//2 - instr.get_width()//2, 400))

# --- 4. DE HOOFD LOOP ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if game.state == GameState.MENU and event.key == pygame.K_SPACE:
                game.state = GameState.TRAINER_SELECT
            
            if game.state == GameState.BATTLE:
                if event.key == pygame.K_w: # Simulatie van winst
                    game.money += game.selected_trainer["bounty"]
                    game.selected_trainer["beaten"] = True
                    game.state = GameState.TRAINER_SELECT

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.state == GameState.TRAINER_SELECT:
                for t in game.trainers:
                    if not t["beaten"] and t["rect"].collidepoint(mouse_pos):
                        game.selected_trainer = t
                        game.state = GameState.BATTLE

    # Teken logica op basis van de State
    if game.state == GameState.MENU:
        draw_welcome()
    elif game.state == GameState.TRAINER_SELECT:
        draw_trainer_select()
    elif game.state == GameState.BATTLE:
        draw_battle_placeholder() # Vervang dit door je battle_sim code

    pygame.display.flip()
    clock.tick(60)

pygame.quit()