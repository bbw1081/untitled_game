import pygame, random, config

from classes.ammo import Ammo
from classes.health_pickup import HealthPickup
from classes.enemy import Enemy

class Game():
    """A class to handle all of the high-level game functions"""
    def __init__(self, player, player_bullet_group, melee_group, enemy_group, enemy_bullet_group, ammo_group, health_group, platform_group, display_surface):
        """Initialize the game"""

        #load in game assets
        self.pixel_font = pygame.font.Font("src/untitled_game/assets/PixelIntv-OPxd.ttf", 24)

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
        self.display_surface = display_surface

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
        score_text = self.pixel_font.render("Score: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.bottomleft = (32, config.WINDOW_HEIGHT - 32)

        ammo_text = self.pixel_font.render("Ammo: " + str(self.player.ammo), True, WHITE)
        ammo_rect = ammo_text.get_rect()
        ammo_rect.bottomright = (config.WINDOW_WIDTH - 32, config.WINDOW_HEIGHT - 32)
        
        health_text = self.pixel_font.render("Health: " + str(self.player.health), True, WHITE)
        health_rect = health_text.get_rect()
        health_rect.bottomleft = (32, config.WINDOW_HEIGHT)

        round_text = self.pixel_font.render("Round: " + str(self.round), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.bottomright = (config.WINDOW_WIDTH - 32, config.WINDOW_HEIGHT)

        #draw the HUD
        self.display_surface.blit(score_text, score_rect)
        self.display_surface.blit(ammo_text, ammo_rect)
        self.display_surface.blit(health_text, health_rect)
        self.display_surface.blit(round_text, round_rect)

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
            if self.collection_time >= config.FPS:
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
            if self.round >= 6:
                Enemy(random.randint(32, config.WINDOW_WIDTH - 32), -100, self.platform_group, 
                  self.enemy_group, self.enemy_bullet_group, self.player, 6, 8)
            else:
                Enemy(random.randint(32, config.WINDOW_WIDTH - 32), -100, self.platform_group, 
                    self.enemy_group, self.enemy_bullet_group, self.player, 0 + self.round, 3+self.round)
            
        #reset the player's position
        self.player.reset_pos()

    def menu(self, main_text, sub_text, version_text=None):
        """Display the main menu"""

        #set colors
        WHITE = (255, 255, 255)

        #render text
        name_text = self.pixel_font.render(main_text, True, WHITE)
        name_rect = name_text.get_rect()
        name_rect.center = (config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2)

        start_text = self.pixel_font.render(sub_text, True, WHITE)
        start_rect = start_text.get_rect()
        start_rect.center = (config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 + 64)

        #blit text 
        self.display_surface.fill((0,0,0))
        self.display_surface.blit(name_text, name_rect)
        self.display_surface.blit(start_text, start_rect)

        if version_text:
            version_text = self.pixel_font.render(version_text, True, WHITE)
            version_rect = version_text.get_rect()
            version_rect.bottomright = (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
            self.display_surface.blit(version_text, version_rect)

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
                    #display controls screen
                    if event.key == pygame.K_SPACE: 
                        is_paused = False
                        self.menu("Move -> A/D or Left/Right; Jump -> Spacebar", 
                                  "Shoot -> W/Up; Melee -> S/Down", "Press enter to begin")
                #check for user quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    config.running = False

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
