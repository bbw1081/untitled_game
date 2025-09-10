import pygame, random

from player import Player
from tile import Tile
from enemy import Enemy
from ammo import Ammo
from health_pickup import HealthPickup

"""GAME SETUP"""
#initialize pygame
pygame.init()

#use 2d vectors
vector = pygame.math.Vector2

#set global running to properly interface with pause menus
global running 

#version number for main menu text
VERSION_NUMBER = "PRE_RELEASEv0.5.0"

#set display surface
#a tile is 32 x 32; currently 40 tiles wide and 23 tiles high
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 736
DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("untitled_game")

#set fps and clock
FPS = 60
CLOCK = pygame.time.Clock()

"""Create the game class"""
#load in game assets
pixel_font = pygame.font.Font("assets/PixelIntv-OPxd.ttf", 24)

class Game():
    """A class to handle all of the high-level game functions"""
    def __init__(self, player, player_bullet_group, melee_group, enemy_group, enemy_bullet_group, ammo_group, health_group, platform_group):
        """Initialize the game"""

        #create game variables
        self.score = 0
        self.round = 0
        self.is_game_over = False
        self.collection_time = 0
        
        #pass in sprite groups
        self.player = player
        self.player_bullet_group = player_bullet_group
        self.melee_group = melee_group
        self.enemy_group = enemy_group
        self.enemy_bullet_group = enemy_bullet_group
        self.ammo_group = ammo_group
        self.health_group = health_group
        self.platform_group = platform_group

    def update(self):
        """Update the game"""
        self.check_collisions()
        self.check_game_over()
        self.check_round_completion()

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
        ammo_rect.bottomright = (WINDOW_WIDTH - 32, WINDOW_HEIGHT - 32)
        
        health_text = pixel_font.render("Health: " + str(self.player.health), True, WHITE)
        health_rect = health_text.get_rect()
        health_rect.bottomleft = (32, WINDOW_HEIGHT)

        round_text = pixel_font.render("Round: " + str(self.round), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.bottomright = (WINDOW_WIDTH - 32, WINDOW_HEIGHT)

        #draw the HUD
        DISPLAY_SURFACE.blit(score_text, score_rect)
        DISPLAY_SURFACE.blit(ammo_text, ammo_rect)
        DISPLAY_SURFACE.blit(health_text, health_rect)
        DISPLAY_SURFACE.blit(round_text, round_rect)

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
                if self.player.ammo > self.player.MAX_AMMO:
                    self.player.ammo = self.player.MAX_AMMO

        #check for collisions between the player and the enemy
        collide_list_c = pygame.sprite.spritecollide(self.player, self.enemy_group, False, pygame.sprite.collide_mask)
        if collide_list_c:
            for enemy in collide_list_c:
                self.player.health -= 20
                #move the player to not take continuous damage
                self.player.position.x -= 256 * enemy.direction
                self.player.rect.bottomleft = self.player.position

        #check for collisions between player and health pickups
        collide_list_d = pygame.sprite.spritecollide(self.player, self.health_group, True, pygame.sprite.collide_mask)
        if collide_list_d:
            for i in collide_list_d:
                self.player.health += 15
                if self.player.health >= self.player.STARTING_HEALTH:
                    self.player.health = self.player.STARTING_HEALTH

    def check_round_completion(self):
        """Check to see if the player has completed the round"""
        if not self.enemy_group:
            if self.collection_time >= FPS:
                self.collection_time = 0
                self.menu("You defeated all the enemies!", "Press enter to start round " + str(self.round + 1))
            else:
                self.collection_time += 1

    def check_game_over(self):
        """Check to see if the player has died"""
        if self.player.health <= 0:
            self.player.death_animation()
            self.is_game_over = True
            self.menu("You Died! Your final score is " + str(self.score), "Press enter to play again")

    def start_next_round(self):
        """Start the next round of the game"""
        #increase round number
        self.round += 1

        #empty groups
        self.player_bullet_group.empty()
        self.melee_group.empty()
        self.enemy_group.empty()
        self.enemy_bullet_group.empty()
        self.ammo_group.empty()
        self.health_group.empty()

        #create the enemies
        for i in range(self.round):
            if self.round >= 4:
                Enemy(random.randint(32, WINDOW_WIDTH - 32), -100, self.platform_group, 
                  self.enemy_group, self.enemy_bullet_group, self.player, 5, 9)
            else:
                Enemy(random.randint(32, WINDOW_WIDTH - 32), -100, self.platform_group, 
                    self.enemy_group, self.enemy_bullet_group, self.player, 2 + self.round, 5+self.round)
            
        #reset the player's position
        self.player.reset_pos()

    def menu(self, main_text, sub_text, version_text=None):
        """Display the main menu"""
        global running

        #set colors
        WHITE = (255, 255, 255)

        #render text
        name_text = pixel_font.render(main_text, True, WHITE)
        name_rect = name_text.get_rect()
        name_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        start_text = pixel_font.render(sub_text, True, WHITE)
        start_rect = start_text.get_rect()
        start_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64)

        #blit text 
        DISPLAY_SURFACE.fill((0,0,0))
        DISPLAY_SURFACE.blit(name_text, name_rect)
        DISPLAY_SURFACE.blit(start_text, start_rect)

        if version_text:
            version_text = pixel_font.render(VERSION_NUMBER, True, WHITE)
            version_rect = version_text.get_rect()
            version_rect.bottomright = (WINDOW_WIDTH, WINDOW_HEIGHT)
            DISPLAY_SURFACE.blit(version_text, version_rect)

        #update the display and pause the game
        pygame.display.update()

        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                #check for user start
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                        if self.is_game_over:
                            self.reset_game()
                        else:
                            self.start_next_round()

                #check for user quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    def reset_game(self):
        """Completley reset the game"""
        #reset game values
        self.round = 0
        self.score = 0
        self.is_game_over = False

        #empty groups
        self.player_bullet_group.empty()
        self.melee_group.empty()
        self.enemy_group.empty()
        self.enemy_bullet_group.empty()
        self.ammo_group.empty()
        self.health_group.empty()

        #reset the player
        self.player.reset()

        #start the next round
        self.start_next_round()

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

"""CREATE AND LOOP THROUGH TILE MAP"""
#TILE MAP KEY
# 0 -> air, 1 -> dirt, 2 -> grass, 8->enemy, 9 -> player spawn
tile_map = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
            my_player = Player(j*32, i*32, my_player_group, my_platform_group, my_player_bullet_group, my_melee_group)
            
"""CREATE GAME INSTANCE"""
my_game = Game(my_player, my_player_bullet_group, my_melee_group, my_enemy_group, my_enemy_bullet_group, my_ammo_group, my_health_group, my_platform_group)
my_game.menu("untitled_game", "press enter to begin", VERSION_NUMBER)

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
