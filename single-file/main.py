import pygame, asyncio, random

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pygame-ce",
#     "random",
#     "asyncio"
# ]

pygame.init()

"""Global vars"""

#version number for main menu
VERSION_NUMBER = "PRE_RELEASEv0.5.6"

#game running variable (set to false when user quits)
running = True

#display surface values
#a tile is 32 x 32 pixels; current 40 tiles wide and 23 tiles high
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 736

#set FPS
FPS = 60

#set tile map(s)
#TILE MAP KEY
# 0 -> air, 1 -> dirt, 2 -> grass, 8->enemy, 9 -> player spawn
tile_map_lvl1 = [
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
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

#load in assets
pixel_font = pygame.font.Font("PixelIntv-OPxd.ttf", 24)
ammo_pickup_image = pygame.image.load("ammo_pickup.png")
bullet_image = pygame.image.load("bullet.png")
enemy_image = pygame.transform.scale(pygame.image.load("enemy.png"), (32, 32))
health_pickup_image = pygame.image.load("health_pickup.png")
melee_attack_image = pygame.transform.scale(pygame.image.load("melee_atk.png"), (32*2.5, 32))
player_image = pygame.transform.scale(pygame.image.load("player.png"), (32, 32))
dirt_image = pygame.transform.scale(pygame.image.load("dirt.png"), (32, 32))
grass_image = pygame.transform.scale(pygame.image.load("grass.png"), (32, 32))

vector = pygame.math.Vector2

async def main():

    """INITIALIZE THE GAME"""

    #set display
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
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
    for i in range(len(tile_map_lvl1)):
        #then loop through each column in a row
        for j in range(len(tile_map_lvl1[i])):
            if tile_map_lvl1[i][j] == 1: #dirt
                Tile(j*32, i*32, 1, my_main_tile_group)
            elif tile_map_lvl1[i][j] == 2: #grass
                Tile(j*32, i*32, 2, my_main_tile_group, my_platform_group)
            elif tile_map_lvl1[i][j] == 9: #player
                my_player = Player(j*32, i*32, my_player_group, my_platform_group, my_player_bullet_group, my_melee_group)

    """CREATE GAME INSTANCE AND RUN MAIN GAME LOOP"""
    #create the game
    my_game = Game(my_player, my_player_bullet_group, my_melee_group, my_enemy_group, my_enemy_bullet_group, my_ammo_group, my_health_group, my_platform_group, DISPLAY_SURFACE)
    #show main menu
    my_game.menu("untitled_game", "press enter to begin or space for controls", VERSION_NUMBER)

    #main game loop
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
        await asyncio.sleep(0)

class Ammo(pygame.sprite.Sprite):
    """Represents an ammo pickup on the ground"""

    def __init__(self, x, y, ammo_group):
        """Initialzie the ammo"""
        super().__init__()

        #load image and get rect
        self.image = ammo_pickup_image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        #set timeout values
        self.frame_count = 0
        self.time_passed = 0
        self.kill_time = 10

        #create a mask for better collision accuracy
        self.mask = pygame.mask.from_surface(self.image)

        #add self to the ammo group
        ammo_group.add(self)

    def update(self):
        """Destroy the ammo after a set period of time"""
        self.frame_count += 1
        if self.frame_count == FPS:
            self.time_passed += 1
        
        if self.time_passed == self.kill_time:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    """A class to represent a bullet shot by the enemy"""

    def __init__(self, x, y, bullet_group, npc):
        """Initialize the bullet"""
        super().__init__()

        #set constant variables
        self.VELOCITY = 30
        self.RANGE = 500

        #load image and get rect
        self.image = bullet_image
        if npc.velocity.x < 0: #if the player is facing left flip the direction
            self.image = pygame.transform.flip(self.image, True, False)
            self.VELOCITY = -1*self.VELOCITY
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.startingx = x
        self.startingy = y

        self.mask = pygame.mask.from_surface(self.image)

        bullet_group.add(self)

    def update(self):
        """Update the bullet's location"""
        self.rect.x += self.VELOCITY
        #if the bullet had passed RANGE, kill it
        if abs(self.rect.x - self.startingx) > self.RANGE:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    """A class to represnt an enemy"""

    def __init__(self, x, y, platform_group, enemy_group, bullet_group, player, min_speed, max_speed):
        """Initialize the enemy character"""
        super().__init__()

        #set constants
        self.VERTICAL_ACCEL = 2 #gravity
        self.VERTICAL_JUMP_SPEED = 27

        #load image and get rect
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)
        
        #attach groups
        self.platform_group = platform_group
        self.player = player
        self.bullet_group = bullet_group

        #load in kinematcs
        self.position = vector(self.rect.x, self.rect.y)
        self.direction = random.choice((-1, 1))
        self.speed = random.randint(min_speed, max_speed)
        self.velocity = vector(self.direction*self.speed, 0)
        self.accel = vector(0, self.VERTICAL_ACCEL)

        #set up fire rate
        self.fire_rate = random.randint(min_speed, max_speed)
        self.frame_count = 0
        self.time_passed = 0

        self.jump_rate = self.fire_rate - 1
        self.jumped = False
        
        #add self to enemy group
        enemy_group.add(self)

    def update(self):
        """Update the enemy's position"""
        self.move()
        self.check_collisions()
        self.check_fire()
        self.check_jump()

    def move(self):
        """Move the enemy based on simple AI"""        
        #update kinematics values
        self.velocity.x = self.direction*self.speed
        self.velocity += self.accel
        self.position += self.velocity + 0.5*self.accel

        #stop the enemy if they are hitting the wall
        if self.position.x < 0:
            self.direction = 1
        if self.position.x > WINDOW_WIDTH - 32:
            self.direction = -1

        #update rect
        self.rect.bottomleft = self.position

    def check_collisions(self):
        """Check for collisions with the ground"""
        if self.velocity.y > 0: #moving down
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
            if collided_platforms:
                self.position.y = collided_platforms[0].rect.top + 1
                self.velocity.y = 0
        
        if self.velocity.y < 0: #moving up
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
            if collided_platforms:
                self.position.y = collided_platforms[0].rect.bottom + 34
                self.velocity.y = 0

    def check_fire(self):
        """Checks if the enemy should fire their weapon"""
        self.frame_count += 1
        if self.frame_count == FPS:
            self.frame_count = 0
            self.time_passed += 1

        if self.time_passed == self.fire_rate:
            EnemyBullet(self.rect.centerx, self.rect.centery, self.bullet_group, self)
            self.time_passed = 0
            self.jumped = False

    def check_jump(self):
        """Checks to see if the enemy should jump"""
        #if the player is above the enemy, if the jump rate is met, and if the enemy hasn't jumped this cycle
        if (self.player.position.y < self.position.y) and (self.time_passed == self.jump_rate) and not self.jumped:
            if pygame.sprite.spritecollide(self, self.platform_group, False, pygame.sprite.collide_mask): #if on ground
                self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED
                self.jumped = True

    def death_animation(self):
        """run the death animation for the enemy"""
        self.kill() #TODO implement this, won't happen until later when animations are actually created
        vector = pygame.math.Vector2

class Game():
    """A class to handle all of the high-level game functions"""
    def __init__(self, player, player_bullet_group, melee_group, enemy_group, enemy_bullet_group, ammo_group, health_group, platform_group, display_surface):
        """Initialize the game"""

        #load in game assets
        self.pixel_font = pixel_font

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
        score_rect.bottomleft = (32, WINDOW_HEIGHT - 32)

        ammo_text = self.pixel_font.render("Ammo: " + str(self.player.ammo), True, WHITE)
        ammo_rect = ammo_text.get_rect()
        ammo_rect.bottomright = (WINDOW_WIDTH - 32, WINDOW_HEIGHT - 32)
        
        health_text = self.pixel_font.render("Health: " + str(self.player.health), True, WHITE)
        health_rect = health_text.get_rect()
        health_rect.bottomleft = (32, WINDOW_HEIGHT)

        round_text = self.pixel_font.render("Round: " + str(self.round), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.bottomright = (WINDOW_WIDTH - 32, WINDOW_HEIGHT)

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
            if self.round >= 6:
                Enemy(random.randint(32, WINDOW_WIDTH - 32), -100, self.platform_group, 
                  self.enemy_group, self.enemy_bullet_group, self.player, 6, 8)
            else:
                Enemy(random.randint(32, WINDOW_WIDTH - 32), -100, self.platform_group, 
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
        name_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        start_text = self.pixel_font.render(sub_text, True, WHITE)
        start_rect = start_text.get_rect()
        start_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64)

        #blit text 
        self.display_surface.fill((0,0,0))
        self.display_surface.blit(name_text, name_rect)
        self.display_surface.blit(start_text, start_rect)

        if version_text:
            version_text = self.pixel_font.render(version_text, True, WHITE)
            version_rect = version_text.get_rect()
            version_rect.bottomright = (WINDOW_WIDTH, WINDOW_HEIGHT)
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

class HealthPickup(pygame.sprite.Sprite):
    """A class to represent a health pickup dropped by an enemy"""

    def __init__(self, x, y, health_group):
        """Initialize the Health pickup"""
        super().__init__()

        #load image and get rect
        self.image = health_pickup_image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        #load in timeout values
        self.frame_count = 0
        self.time_passed = 0
        self.kill_time = 10

        #create a mask
        self.mask = pygame.mask.from_surface(self.image)

        #add self to health group
        health_group.add(self)

    def update(self):
        """Check to see if the health pack has timed out"""
        self.frame_count += 1
        if self.frame_count == FPS:
            self.time_passed +=1
        
        if self.time_passed == self.kill_time:
            self.kill()

class MeleeAtk(pygame.sprite.Sprite):
    """A class to represent a melee attack that was performed by the player"""

    def __init__(self, melee_group, player):
        """Initialize the melee attack"""
        super().__init__()

        self.frame_count = 0
        self.max_frame_count = 2

        self.player = player

        #load in image and get rect
        self.image = melee_attack_image
        self.rect = self.image.get_rect()
        if self.player.velocity.x > 0: #moving right
            self.rect.bottomleft = (self.player.rect.right, self.player.rect.bottom)
        else: #moving left
            self.rect.bottomright = (self.player.rect.left, self.player.rect.bottom)

        self.mask = pygame.mask.from_surface(self.image)

        melee_group.add(self)

    def update(self):
        """Update the melee attack's location"""
        self.frame_count += 1
        if self.frame_count > self.max_frame_count:
            self.kill()
        else:
            if self.player.velocity.x > 0: #moving right
                self.rect.bottomleft = (self.player.rect.right, self.player.rect.bottom)
            else: #moving left
                self.rect.bottomright = (self.player.rect.left, self.player.rect.bottom)

class PlayerBullet(pygame.sprite.Sprite):
    """A class to represent a bullet that was fired by the player"""

    def __init__(self, x, y, bullet_group, player):
        """Initialize the bullet"""
        super().__init__()

        #set constant variables
        self.VELOCITY = 30
        self.RANGE = 500

        #load image and get rect
        self.image = bullet_image
        if player.velocity.x < 0: #if the player is facing left flip the direction
            self.image = pygame.transform.flip(self.image, True, False)
            self.VELOCITY = -1*self.VELOCITY
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.startingx = x
        self.startingy = y

        self.mask = pygame.mask.from_surface(self.image)

        bullet_group.add(self)

    def update(self):
        """Update the bullet's location"""
        self.rect.x += self.VELOCITY
        #if the bullet had passed RANGE, kill it
        if abs(self.rect.x - self.startingx) > self.RANGE:
            self.kill()

class Player(pygame.sprite.Sprite):
    """A class to represent the player"""

    def __init__(self, x, y, player_group, platform_group, bullet_group, melee_group):
        """Initialize the player character"""
        super().__init__()

        #set constants
        self.HORIZONTAL_ACCEL = 2
        self.HORIZONTAL_FRICTION = 0.2
        self.VERTICAL_ACCEL = 0.8 #gravity
        self.VERTICAL_JUMP_SPEED = 18 #determines how high the player can jump
        self.STARTING_HEALTH = 100
        self.STARTING_AMMO = 10
        self.MAX_AMMO = 25
        
        #load image and get rect
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)
        self.startingx = x
        self.startingy = y

        #create a mask for more accurate collisions
        self.mask = pygame.mask.from_surface(self.image)

        #attach sprite groups
        self.platform_group = platform_group
        self.bullet_group = bullet_group
        self.melee_group = melee_group

        #create kinematics vectors
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.accel = vector(0, self.VERTICAL_ACCEL)

        #set additional values
        self.health = self.STARTING_HEALTH
        self.ammo = self.STARTING_AMMO
        
        player_group.add(self)
    
    def update(self):
        """Update the player"""
        self.move()
        self.check_collisions()

    def move(self):
        """Move the player based on keyboard input"""
        #reset the acceleration vector
        self.accel = vector(0, self.VERTICAL_ACCEL)

        #check for key press and set the horizontal accel
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.accel.x = -1 * self.HORIZONTAL_ACCEL
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.accel.x = self.HORIZONTAL_ACCEL

        #calculate new kinematics values
        self.accel.x -= self.velocity.x * self.HORIZONTAL_FRICTION
        self.velocity += self.accel
        self.position += self.velocity + 0.5*self.accel

        #stop the player if they are hitting the wall
        if self.position.x < 0:
            self.position.x = 0
        if self.position.x > WINDOW_WIDTH - 32:
            self.position.x = WINDOW_WIDTH - 32

        self.rect.bottomleft = self.position

    def check_collisions(self):
        """Check for collisions between the player and various other objects"""
        #collisions check between player and platforms when falling
        if self.velocity.y > 0: #falling
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False, pygame.sprite.collide_mask)
            if collided_platforms:
                self.position.y = collided_platforms[0].rect.top + 1 #add one to keep player on the ground
                self.velocity.y = 0

        #collision check between player and platforms when jumping
        if self.velocity.y < 0: #moving up
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False, pygame.sprite.collide_mask)
            if collided_platforms:
                self.position.y = collided_platforms[0].rect.bottom + 34
                self.velocity.y = 0

    def jump(self):
        """Make the player jump"""
        #player can only jump if on the ground
        if pygame.sprite.spritecollide(self, self.platform_group, False):
            self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED

    def ranged_atk(self):
        """Make the player shoot a projectile"""
        if self.ammo > 0:
            PlayerBullet(self.rect.centerx, self.rect.centery, self.bullet_group, self)
            self.ammo -= 1

    def melee_atk(self):
        """Make the player do a melee attack"""
        MeleeAtk(self.melee_group, self)

    def death_animation(self):
        """Play the player's death animation"""
        pass #TODO implement animations

    def reset_pos(self):
        """Reset the player's position"""
        #reset kinematics vectors
        self.position = vector(self.startingx, self.startingy)
        self.velocity = vector(0, 0)
        self.accel = vector(0, self.VERTICAL_ACCEL)

        #reset rect position
        self.rect.bottomleft = self.position

    def reset(self):
        """Fully reset player"""
        self.health = self.STARTING_HEALTH
        self.ammo = self.STARTING_AMMO
        self.reset_pos()

class Tile(pygame.sprite.Sprite):
    """A class to represent a tile on the playing field"""

    def __init__(self, x, y, tile_code, main_group, sub_group=None):
        super().__init__()
        #load in image
        if tile_code == 1: #dirt
            self.image = dirt_image
        elif tile_code == 2: #grass
            self.image = grass_image
            sub_group.add(self)

        #add tile to main group
        main_group.add(self)            

        #get rect
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        #create mask for more accureate collisions
        self.mask = pygame.mask.from_surface(self.image)

if (__name__ == "__main__"):
    #run main function
    asyncio.run(main())

    #once main function breaks, quit pygame
    pygame.quit()