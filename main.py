import pygame, random, config

from player import Player
from tile import Tile
from enemy import Enemy
from ammo import Ammo
from health_pickup import HealthPickup
from game import Game

def main():

    """INITIALIZE THE GAME"""
    #initialize pygame
    pygame.init()
    #set display
    DISPLAY_SURFACE = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption("untitled_game")
    #create clock
    CLOCK = pygame.time.Clock()

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

    """GENERATE TILES FROM TILE MAP"""
    #first loop through each of the rows
    for i in range(len(config.tile_map_lvl1)):
        #then loop through each column in a row
        for j in range(len(config.tile_map_lvl1[i])):
            if config.tile_map_lvl1[i][j] == 1: #dirt
                Tile(j*32, i*32, 1, my_main_tile_group)
            elif config.tile_map_lvl1[i][j] == 2: #grass
                Tile(j*32, i*32, 2, my_main_tile_group, my_platform_group)
            elif config.tile_map_lvl1[i][j] == 9: #player
                my_player = Player(j*32, i*32, my_player_group, my_platform_group, my_player_bullet_group, my_melee_group)

    """CREATE GAME INSTANCE AND RUN MAIN GAME LOOP"""
    #create the game
    my_game = Game(my_player, my_player_bullet_group, my_melee_group, my_enemy_group, my_enemy_bullet_group, my_ammo_group, my_health_group, my_platform_group, DISPLAY_SURFACE)
    #show main menu
    my_game.menu("untitled_game", "press enter to begin or space for controls", config.VERSION_NUMBER)

    #main game loop
    config.running = True
    while config.running:
        for event in pygame.event.get():
            #check for user quit
            if event.type == pygame.QUIT:
                config.running = False
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
        CLOCK.tick(config.FPS)

if (__name__ == "__main__"):
    #run main function
    main()

    #once main function breaks, quit pygame
    pygame.quit()