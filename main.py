import pygame, random

from player import Player
from tile import Tile
from enemy import Enemy
from player_bullet import PlayerBullet
from enemy_bullet import EnemyBullet
from melee_atk import MeleeAtk
from ammo import Ammo
from health_pickup import HealthPickup

"""GAME SETUP"""
#initialize pygame
pygame.init()

#use 2d vectors
vector = pygame.math.Vector2

#set display surface
#a tile is 32 x 32; currently 40 tiles wide and 23 tiles high
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 736
DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("")

#set fps and clock
FPS = 60
CLOCK = pygame.time.Clock()

"""Create the game class"""
#load in game assets
pixel_font = pygame.font.Font("assets\PixelIntv-OPxd.ttf", 24)

class Game():
    """A class to handle all of the high-level game functions"""
    def __init__(self, player, player_bullet_group, melee_group, enemy_group, enemy_bullet_group, ammo_group, health_group):
        """Initialize the game"""

        #create game variables
        self.score = 0
        self.round = 1
        
        #pass in sprite groups
        self.player = player
        self.player_bullet_group = player_bullet_group
        self.melee_group = melee_group
        self.enemy_group = enemy_group
        self.enemy_bullet_group = enemy_bullet_group
        self.ammo_group = ammo_group
        self.health_group = health_group

    def update(self):
        """Update the game"""
        self.check_collisions()
        self.check_game_over()

    def draw(self):
        """draw the HUD"""
        #define colors
        WHITE = (255, 255, 255)

        #set text
        score_text = pixel_font.render("Score: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.bottomleft = (32, WINDOW_HEIGHT - 32)

        ammo_text = pixel_font.render("Ammo: " + str(self.player.ammo), True, WHITE)
        ammo_rect = ammo_text.get_rect()
        ammo_rect.bottomright = (WINDOW_WIDTH - 32, WINDOW_HEIGHT - 32)\
        
        health_text = pixel_font.render("Health: " + str(self.player.health), True, WHITE)
        health_rect = health_text.get_rect()
        health_rect.bottomleft = (32, WINDOW_HEIGHT)

        #draw the HUD
        DISPLAY_SURFACE.blit(score_text, score_rect)
        DISPLAY_SURFACE.blit(ammo_text, ammo_rect)
        DISPLAY_SURFACE.blit(health_text, health_rect)

    def check_collisions(self):
        """Check for collisions that affect gameplay"""
        #check for collisions between the enemy and the player's attacks
        collide_dict_a = pygame.sprite.groupcollide(self.player_bullet_group, self.enemy_group, True, False, pygame.sprite.collide_mask)
        if collide_dict_a:
            for enemies in collide_dict_a.values():
                for enemy in enemies:
                    self.score += 10 * self.round
                    Ammo(enemy.rect.x, enemy.rect.bottom, self.ammo_group)
                    if random.randint(1, 4) == 1:
                        HealthPickup(enemy.rect.x, enemy.rect.bottom, self.health_group)
                    enemy.death_animation()

        collide_dict_b = pygame.sprite.groupcollide(self.melee_group, self.enemy_group, True, False, pygame.sprite.collide_mask)
        if collide_dict_b:
            for enemies in collide_dict_b.values():
                for enemy in enemies:
                    self.score += 15 * self.round
                    Ammo(enemy.rect.x, enemy.rect.bottom, self.ammo_group)
                    if random.randint(1, 4) == 1:
                        HealthPickup(enemy.rect.x, enemy.rect.bottom, self.health_group)
                    enemy.death_animation()

        #check for collisions between the player and the enemy attacks
        collide_list = pygame.sprite.spritecollide(self.player, self.enemy_bullet_group, True, pygame.sprite.collide_mask)
        if collide_list:
            for hit in collide_list:
                self.player.health -= 10

        #check for collisions between the player and the ammo
        collide_list_b = pygame.sprite.spritecollide(self.player, self.ammo_group, True, pygame.sprite.collide_mask)
        if collide_list_b:
            for i in collide_list_b:
                self.player.ammo += random.randint(1, 5)
                if self.player.ammo > self.player.STARTING_AMMO:
                    self.player.ammo = self.player.STARTING_AMMO

        #check for collisions between the player and the enemy
        collide_list_c = pygame.sprite.spritecollide(self.player, self.enemy_group, False, pygame.sprite.collide_mask)
        if collide_list_c:
            for enemy in collide_list_c:
                self.player.health -= 20
                #move the player to not take continuous damage
                self.player.position.x -= 256 * enemy.direction
                self.player.rect.bottomleft = self.player.position

        #check for collisions between the enemy and the ammo pickups
        collide_dict_c = pygame.sprite.groupcollide(self.enemy_group, self.ammo_group, False, True, pygame.sprite.collide_mask)
        if collide_dict_c:
            #TODO probably play some kind of sound effect
            pass

        #check for collisions between player and health pickups
        collide_list_d = pygame.sprite.spritecollide(self.player, self.health_group, True, pygame.sprite.collide_mask)
        if collide_list_d:
            for i in collide_list_d:
                self.player.health += 15

        #check for collisions between enemies and health pickups
        collide_dict_d = pygame.sprite.groupcollide(self.enemy_group, self.health_group, False, True, pygame.sprite.collide_mask)
        if collide_dict_d:
            #TODO add some kind of sound effect 
            pass

    def check_round_completion(self):
        """Check to see if the player has completed the round"""
        pass

    def check_game_over(self):
        """Check to see if the player has died"""
        if self.player.health <= 0:
            self.player.death_animation()
            self.death_screen()

    def start_next_round(self):
        """Start the next round of the game"""
        pass

    def main_menu(self):
        """Display the main menu"""
        pass

    def death_screen(self):
        """Display the death screen"""
        pass

    def intermission_screen(self):
        """Display the screen that will be shown between rounds"""
        pass

    def reset_game(self):
        """Completley reset the game"""
        pass

"""DEFINE GROUPS"""
my_main_tile_group = pygame.sprite.Group()
my_platform_group = pygame.sprite.Group()
my_player_group = pygame.sprite.Group()
my_player_bullet_group = pygame.sprite.Group()
my_melee_group = pygame.sprite.Group()
my_enemy_group = pygame.sprite.Group()
my_enemy_bullet_group = pygame.sprite.Group()
my_ammo_group = pygame.sprite.Group()
my_health_group = pygame.sprite.Group()

"""Create a tile map and instantiate the tiles"""
#TILE MAP KEY
# 0 -> air, 1 -> dirt, 2 -> grass, 8->enemy, 9 -> player spawn
tile_map = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

#generate tiles from tile map
#first loop through each of the rows
for i in range(len(tile_map)):
    #then loop through each column in a row
    for j in range(len(tile_map[i])):
        if tile_map[i][j] == 1: #dirt
            Tile(j*32, i*32, 1, my_main_tile_group)
        elif tile_map[i][j] == 2: #grass
            Tile(j*32, i*32, 2, my_main_tile_group, my_platform_group)
        elif tile_map[i][j] == 9: #player
            my_player = Player(j*32, i*32, my_player_group, my_platform_group, my_player_bullet_group, my_melee_group)\
            
my_enemy_group.add(Enemy(WINDOW_WIDTH - 100, 0, my_platform_group, my_enemy_group, my_enemy_bullet_group, my_player, 2, 5))

my_game = Game(my_player, my_player_bullet_group, my_melee_group, my_enemy_group, my_enemy_bullet_group, my_ammo_group, my_health_group)

"""MAIN GAME LOOP"""
running = True
while running:
    for event in pygame.event.get():
        #check for user quit
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            #player intends to jump
            if event.key == pygame.K_SPACE:
                my_player.jump()
            #player intends to use ranged atk
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                my_player.ranged_atk()
            #player intends to use melee atk
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                my_player.melee_atk()

    #draw bg
    DISPLAY_SURFACE.fill((0,0,0))

    #update and draw sprites
    my_main_tile_group.update()
    my_main_tile_group.draw(DISPLAY_SURFACE)

    my_player_group.update()
    my_player_group.draw(DISPLAY_SURFACE)

    my_player_bullet_group.update()
    my_player_bullet_group.draw(DISPLAY_SURFACE)

    my_enemy_bullet_group.update()
    my_enemy_bullet_group.draw(DISPLAY_SURFACE)

    my_melee_group.update()
    my_melee_group.draw(DISPLAY_SURFACE)

    my_enemy_group.update()
    my_enemy_group.draw(DISPLAY_SURFACE)
    
    my_ammo_group.update()
    my_ammo_group.draw(DISPLAY_SURFACE)

    my_health_group.update()
    my_health_group.draw(DISPLAY_SURFACE)

    my_game.update()
    my_game.draw()

    #update display and tick clock
    pygame.display.update()
    CLOCK.tick(FPS)

pygame.quit()