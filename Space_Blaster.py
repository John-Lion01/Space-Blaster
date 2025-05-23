# -*- coding: utf-8 -*-
# #####################################################################
# Name : Space Blaster
# Purpose :  jeu de tir en 2D; vaisseau spatial;
# Author : DJANTA M. Jean
# Createdd : 16/04/2025
# Last Updated : 09/05/2025
# #######################################################################

 
# Modules
import pygame
import sys
import random
import os
import json

# --- Constantes ---
WIDTH, HEIGHT = 800, 600
FPS = 60
LEVEL_COUNT = 500

# COLORS 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE_NAVY = (0, 0, 128)
BLEU_NUIT = (10, 10, 30)
BLEU_CLAIRE = (0, 255, 255)
VERT_VIF = (0, 200, 0)
GRIS_FONCE = (60, 60, 60)
GRIS_CLAIRE = (200, 200, 200)
RED = (255, 0, 0)
BLUE_SKY = (0, 191, 255)
VIOLET = (128, 0, 128)
YELLOW = (255, 255, 0)
BLEU_TRES_FONCE = (0, 0, 30)

# --- Initialisation ---
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Space Blaster ")
clock = pygame.time.Clock()

# --- Chemins de ressouces---
BASE_PATH = os.path.dirname(__file__)
SOUND_PATH = os.path.join(BASE_PATH, "sounds")
IMAGE_PATH = os.path.join(BASE_PATH, "images")
SAVE_FILE = os.path.join(BASE_PATH, "sauvegarde.json")

# --- Chargement des ressources ---
pygame.mixer.music.load(os.path.join(SOUND_PATH, "space_theme.mp3"))
sound_shoot = pygame.mixer.Sound(os.path.join(SOUND_PATH, "laser.mp3"))
sound_explosion = pygame.mixer.Sound(os.path.join(SOUND_PATH, "explosion.wav"))

player_img = pygame.transform.scale(
    pygame.image.load(os.path.join(IMAGE_PATH, "Vaisseau.jpg")).convert_alpha(), (64, 80)
)

font = pygame.font.SysFont("Arial", 28)
menu_font = pygame.font.SysFont(None, 48)
title_font = pygame.font.SysFont(None, 80)
info_font = pygame.font.SysFont(None, 36)

# Sauvegarde pour l'exécutable Sous Windows → devient : C:\Users\nom_utilisateur\.mon_jeu:
# import shutil
# def chemin_sauvegarde():
#     dossier = os.path.expanduser("~/.Space_Blaster")
#     os.makedirs(dossier, exist_ok=True)  # Créé le dossier s'il n'existe pas
#     return os.path.join(dossier, "sauvegarde.json")

# def initialiser_sauvegarde():
#     chemin = chemin_sauvegarde()
#     if not os.path.exists(chemin):
#         shutil.copy(os.path.join(os.getenv('APPDATA'), "Space_Blaster", "save_template.json"), chemin)

# initialiser_sauvegarde()

# def sauvegarder_progression(data):
#     with open(chemin_sauvegarde(), "w") as f:
#         json.dump(data, f, indent=4)

# def charger_progression():
#     chemin = chemin_sauvegarde()
#     if os.path.exists(chemin):
#         with open(chemin, "r") as f:
#             return json.load(f)
#     else:
#         return {"niveau_max": 1, "score_max": 0}  # Ou valeurs par défaut

# --- Sauvegarde ---
def charger_progression():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            return json.load(f)
    return {"niveau_max": 1, "score_max": 0}

def sauvegarder_progression(data):
    with open(SAVE_FILE, 'w') as f:
        # print("Sauvegarde................", data)
        json.dump(data, f, indent=4)

save_data = charger_progression()
niveau_max = save_data.get("niveau_max", 1)
score_max_sauvegarde = save_data.get("score_max", 0)

# --- Fonctions d'affichage---
def draw_text(text, x, y, color=WHITE):
    screen.blit(font.render(text, True, color), (x, y))

def draw_centered_text(text, y, font, color=WHITE):
    rendered = font.render(text, True, color)
    screen.blit(rendered, (WIDTH // 2 - rendered.get_width() // 2, y))

def show_level_select_screen():
    global level
    selecting = True 
    button_size = 60
    margin = 10
    cols = 10
    rows = 7
    while selecting:
        screen.fill(BLEU_NUIT)
        draw_centered_text("Choisis ton niveau", 30, menu_font)
        for i in range(min(LEVEL_COUNT, cols * rows)):
            col = i % cols
            row = i // cols
            x = 50 + col * (button_size + margin)
            y = 80 + row * (button_size + margin)
            rect = pygame.Rect(x, y, button_size, button_size)
            level_num = i + 1
            color = VERT_VIF if level_num <= niveau_max else GRIS_FONCE
            pygame.draw.rect(screen, color, rect)
            label = font.render(str(level_num), True, WHITE)
            screen.blit(label, (x + 8, y + 5))
            if pygame.mouse.get_pressed()[0] and rect.collidepoint(pygame.mouse.get_pos()) and level_num <= niveau_max:
                level = level_num
                selecting = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()        

# --- Classes ---
class Player:
    def __init__(self):
        self.image = player_img
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 40))
        # self.speed = Player.speed(self, level)
        self.lives = 3
        self.triple_shot = False
        self.triple_timer = 0
        self.bomb = False

    def move(self, keys, level):
        if keys[pygame.K_LEFT]:
            self.rect.x -= Player.speed(self, level)
        if keys[pygame.K_RIGHT]:
            self.rect.x += Player.speed(self, level)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
        
    def speed(self, level) :
        return 5+(0.2*level)

    def reset(self):
        self.__init__()

class Projectile:
    def __init__(self, x, y, speed=7, width=5, height=15, damage=1):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.damage = damage

    def move(self):
        self.rect.y -= self.speed
        return self.rect.bottom > 0
    
    def draw(self, surface, color=RED):
        pygame.draw.rect(surface, color, self.rect)
        
    def nbr_projectile(level) :
        if level <= 5:
            lv_shot_count = 1
        elif level <= 10:
            lv_shot_count = 2
        elif level <= 20:
            lv_shot_count = 3
        else:
            lv_shot_count = 4
        return lv_shot_count

    def generate_projectiles(player_rect, level, triple_bonus_active):
        shot_count = Projectile.nbr_projectile(level)
        if triple_bonus_active :
            shot_count += 1
        offsets = {
            1: [0],
            2: [-7, 7],
            3: [-10, 0, 10],
            4: [-17, -10, 10, 17],
            5: [-17, -10, 0,  10, 17]
        }[shot_count]

        new_projectiles = []
        for offset in offsets:
            x = player_rect.centerx + offset - 2
            y = player_rect.top
            new_projectiles.append(Projectile(x, y))

        return new_projectiles

class Enemy:
    
    TYPES = {
            "standard": {"color": GREEN, "size": (40, 30), "speed": 2, "hp": 1},
            "fast": {"color": RED, "size": (30, 30), "speed": 3, "hp": 1},
            "armored": {"color": BLUE_NAVY, "size": (60, 50), "speed": 1.5, "hp": 3},
    }
    
    def add_speed(level) :
        add = level*0.1
        return add

    def __init__(self, level):
        if level%10 == 0:
            # Pour les niveaux 10, 20, 30, 40, 50, 60, 70........
            self.type = 'standard'
            self.attrs ={"color": RED, 'size': (70, 70), "speed": 3, "hp": 10}
        else :
            self.type = random.choices(
                population=["standard", "fast", "armored"],
                weights=[0.6, 0.25, 0.15]
            )[0]
            self.attrs = Enemy.TYPES[self.type]

        x = random.randint(0+2, WIDTH - self.attrs['size'][0]-2)
        self.rect = pygame.Rect(x, -self.attrs["size"][1], *self.attrs["size"])
        self.color = self.attrs["color"]
        self.speed = self.attrs["speed"] + Enemy.add_speed(level)
        self.hp = self.attrs["hp"]


    def move(self, level):
        self.rect.y += self.speed
        return self.rect.top < HEIGHT

class Bonus:
    COLORS = {'life': BLUE_SKY, 'triple_shot': VIOLET, 'bomb': YELLOW}

    def __init__(self, x, y, bonus_type):
        self.type = bonus_type
        # self.rect = pygame.Rect(x, y, 30, 30)
        # self.y = y
        # self.x = x
        self.ray = 20
        self.rect = pygame.Rect(x, y, self.ray * 2, self.ray * 2)

    def move(self):
        vitesse = pygame.Vector2(0, 4)
        # self.y += 3
        self.rect.move_ip(vitesse)
        return self.rect.top < HEIGHT

    def draw(self):
        pygame.draw.circle(screen, self.COLORS[self.type], self.rect.center, self.ray)

class Explosion:
    def __init__(self, rect):
        self.rect = rect.copy()
        self.timer = 200

    def update(self, dt):
        self.timer -= dt
        return self.timer > 0

# --- Boucle Principale ---
def main():
    global level
    global niveau_max, score_max_sauvegarde
    player = Player()
    projectiles, enemies, bonuses, explosions = [], [], [], []
    score, level = 0, 1
    enemy_per_wave, enemies_spawned = 5 + 1*level, 0
    last_enemy_spawn = pygame.time.get_ticks()
    enemy_spawn_delay = 1000

    running, pause, game_over, start_screen, level_select = True, False, False, True, False
    pause_options = ["Reprendre", "Volume", "Quitter", "Home"]
    selected_option = 0
    volume = 0.2
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)

    while running:
        dt = clock.tick(FPS)
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()
        # Donnée à sauvegarder
        niveau_max = max(niveau_max, level)
        score_max_sauvegarde = max(score, score_max_sauvegarde)
        donnée_a_saugarde = {'niveau_max' : niveau_max, 'score_max' : score_max_sauvegarde}

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_screen:
                    start_screen = False
                    level_select = True
                elif event.key == pygame.K_s :
                    sauvegarder_progression(donnée_a_saugarde)
                elif event.key == pygame.K_p and not game_over:
                    pause = not pause
                    sauvegarder_progression(donnée_a_saugarde)

                if pause :
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(pause_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(pause_options)
                    elif event.key == pygame.K_RETURN :
                        if pause_options[selected_option] == "Reprendre":
                            pause = False
                        elif pause_options[selected_option] == "Quitter":
                            sauvegarder_progression(donnée_a_saugarde)
                            running = False
                        elif pause_options[selected_option] == "Home" :
                            sauvegarder_progression(donnée_a_saugarde)
                            start_screen = True
                            
                    
                    elif pause_options[selected_option] == "Volume":
                        if event.key == pygame.K_LEFT:
                            volume = max(0, volume - 0.1)
                            pygame.mixer.music.set_volume(volume)
                        elif event.key == pygame.K_RIGHT:
                            volume = min(1, volume + 0.1)
                            pygame.mixer.music.set_volume(volume)

        if start_screen:
            screen.fill(BLEU_TRES_FONCE)
            draw_centered_text("🚀 Space Blaster", HEIGHT // 3, title_font)
            draw_centered_text("Appuie sur ESPACE pour commencer", HEIGHT // 2, info_font, GRIS_CLAIRE)
            draw_text(f"Max Score : {score_max_sauvegarde}", 40, 20)
            draw_text(f"Niveau Max : {niveau_max}", WIDTH-250, 20)
            draw_centered_text(f"Développer par : ", HEIGHT-150, info_font)
            draw_centered_text(f" Jean DJANTA ", HEIGHT-120, info_font)
            draw_centered_text(f"jeansdjanta@hotmail.com", HEIGHT-90, info_font)
            pygame.display.flip()
            pause = False # pour ne pas retourner à l'écran de pause
            projectiles.clear()
            enemies.clear()
            explosions.clear()
            bonuses.clear()
            score = 0
            level = 1
            player.reset()
            continue
        
        if level_select :
            show_level_select_screen()
            level_select = False

        # Pause
        if pause:
            screen.fill((20, 20, 40))
            for i, option in enumerate(pause_options):
                color = (255, 255, 0) if i == selected_option else (180, 180, 180)
                txt = f"{option} : {int(volume * 100)}%" if option == "Volume" else option
                draw_centered_text(txt, HEIGHT // 3 + i * 60, menu_font, color)
            pygame.display.flip()
            continue

        # Game over
        if game_over:
            draw_centered_text("GAME OVER - Appuie sur R pour recommencer", HEIGHT // 2 - 50, font, YELLOW)
            draw_text(f"Niveau : {level}", WIDTH//2, HEIGHT//2)
            draw_text(f"Score : {score}", WIDTH//2, HEIGHT//2 + 50)
            if keys[pygame.K_r]:
                player.reset()
                # player.speed += player.speed(level)
                projectiles.clear()
                enemies.clear()
                explosions.clear()
                bonuses.clear()
                score = 0
                level = 1
                game_over = False
            pygame.display.flip()
            continue
        
        # déplacement du joueur
        player.move(keys, level)

        # Tir
        if keys[pygame.K_SPACE]:
            if not projectiles or projectiles[-1].rect.y < player.rect.y - 50 :
                new_projectiles = Projectile.generate_projectiles(player.rect, level, player.triple_shot)
                projectiles.extend(new_projectiles)
                sound_shoot.play()

        # Mise à jour des tirs
        projectiles = [p for p in projectiles if p.move()]

        # Apparition ennemis
        now = pygame.time.get_ticks()
        if now - last_enemy_spawn > enemy_spawn_delay and enemies_spawned < enemy_per_wave:
            enemies.append(Enemy(level))
            enemies_spawned += 1
            last_enemy_spawn = now
            
        # Enemie par vague
        if level <11 :
                enemy_per_wave = 5 +  level
        else :
            enemy_per_wave = level
        
                

        if not enemies and enemies_spawned >= enemy_per_wave:
            level += 1
            # player.speed += 0.5*level
            # Enemy.level_add_speed += 0.1*level
            # enemy_per_wave = 1*level
            enemies_spawned, enemy_spawn_delay = 0, max(300, enemy_spawn_delay - 15*level)

        # Mouvements ennemis et collisions
        new_enemies = []
        for enemy in enemies:
            if enemy.move(level):
                new_enemies.append(enemy)
            else:
                player.lives -= 1
                if player.lives <= 0:
                    sauvegarder_progression(donnée_a_saugarde)
                    game_over = True
        enemies = new_enemies

        # Collisions tirs / ennemis
        for proj in projectiles[:]:
            for enemy in enemies[:]:
                if proj.rect.colliderect(enemy.rect):
                    # niveaux de vie de l'enemy hp défini dans la class Enemy
                    enemy.hp -= proj.damage
                    if enemy.hp <= 0 :
                        explosions.append(Explosion(enemy.rect))
                        score += enemy.attrs['hp']
                        sound_explosion.play()
                        projectiles.remove(proj)
                        enemies.remove(enemy)
                        
                        # Les Bonuses
                        if level < 11 :
                            # Bonus ou pas
                            Gbonus = random.choices([True, False], [0.25, 0.8])[0]
                            # Type de Bonus
                            if Gbonus :
                                bonus_type = random.choices(
                                    population=['life', 'triple_shot', 'bomb'],
                                    weights=[0.25, 0.5, 0.25])[0]
                                bonuses.append(Bonus(enemy.rect.centerx, enemy.rect.centery, bonus_type))
                        elif level < 21 :
                            # Bonus ou pas
                            Gbonus = random.choices([True, False], [0.35, 0.65])[0]
                            # Type de Bonus
                            if Gbonus :
                                bonus_type = random.choices(
                                    population=['life', 'triple_shot', 'bomb'],
                                    weights=[0.35, 0.25, 0.4])[0]
                                bonuses.append(Bonus(enemy.rect.centerx, enemy.rect.centery, bonus_type))
                        else :
                            # Bonus ou pas
                            if level < 31 :
                                Gbonus = random.choices([True, False], [0.45, 0.55])[0]
                            elif level < 41 :
                                Gbonus = random.choices([True, False], [0.60, 0.4])[0]
                            elif level < 51 :
                                Gbonus = random.choices([True, False], [0.75, 0.25])[0]
                            else :
                                Gbonus = random.choices([True, False], [0.90, 0.1])[0]
                            
                            # Type de Bonus
                            if Gbonus :
                                bonus_type = random.choices(
                                    population=['life', 'triple_shot', 'bomb'],
                                    weights=[0.4, 0.1, 0.5])[0]
                                bonuses.append(Bonus(enemy.rect.centerx, enemy.rect.centery, bonus_type))                        
                            
                    break

        # Mises à jour des explosions
        explosions = [e for e in explosions if e.update(dt)]

        # Mouvements et collisions des bonus
        for bonus in bonuses[:]:
            if bonus.move():
                bonus.draw()
                if bonus.rect.colliderect(player.rect):
                    if bonus.type == 'life' and player.lives < 3:
                        player.lives += 1
                    elif bonus.type == 'triple_shot':
                        player.triple_shot = True
                        player.triple_timer = now
                    elif bonus.type == 'bomb':
                        player.bomb = True
                    bonuses.remove(bonus)
            else:
                bonuses.remove(bonus)

        # Gestion des bonus actifs
        if player.triple_shot and now - player.triple_timer > 5000:
            player.triple_shot = False

        if player.bomb:
            for ene in enemies[:] :
                score += ene.hp
            enemies.clear()
            player.bomb = False
            sound_explosion.play()

        # Affichage
        screen.blit(player.image, player.rect)
        for p in projectiles:
            p.draw(screen)
        for enemy in enemies:
            pygame.draw.rect(screen, enemy.color, enemy.rect)
        for e in explosions:
            pygame.draw.ellipse(screen, RED, e.rect)

        draw_text(f"Score : {score}", 10, 10)
        draw_text(f"Vies : {'*'*player.lives}", WIDTH - 120, 10, RED)
        draw_text(f"Niveau : {level}", WIDTH // 2 - 60, 10, BLEU_CLAIRE)
        draw_text(f"v. player : {player.speed(level):.2f}", 10, HEIGHT-35)
        draw_text(f"Nbre Enemie : {enemy_per_wave}", WIDTH/2-150, HEIGHT-35)
        draw_text(f"V. Enemy : + {Enemy.add_speed(level) :.2f}", WIDTH-200, HEIGHT-35)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

# fin Space_blaster