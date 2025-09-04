import pygame

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

"""DEFINE CLASSES"""
class Game():
    """A class to handle all of the high-level game functions"""
    def __init__(self):
        """Initialize the game"""
        pass

    def update(self):
        """Update the game"""
        pass

    def draw(self):
        """draw the HUD"""
        pass

    def check_collisions(self):
        """Check for collisions that affect gameplay"""
        pass

    def check_round_completion(self):
        """Check to see if the player has completed the round"""
        pass

    def check_game_over(self):
        """Check to see if the player has died"""
        pass

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

class Tile(pygame.sprite.Sprite):
    """A class to represent a tile on the playing field"""
    def __init__(self, x, y, tile_code, main_group, sub_group=None):
        super().__init__()
        #load in image
        if tile_code == 1: #dirt
            self.image = pygame.transform.scale(pygame.image.load("assets/dirt.png"), (32, 32))
        elif tile_code == 2: #grass
            self.image = pygame.transform.scale(pygame.image.load("assets/grass.png"), (32, 32))
            sub_group.add(self)


        #add tile to main group
        main_group.add(self)

        #get rect
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        #create mask for more accureate collisions
        self.mask = pygame.mask.from_surface(self.image)

class Player(pygame.sprite.Sprite):
    """A class to represent the player"""
    def __init__(self, x, y, player_group, platform_group, bullet_group):
        """Initialize the player character"""
        super().__init__()

        #set constants
        self.HORIZONTAL_ACCEL = 2
        self.HORIZONTAL_FRICTION = 0.1
        self.VERTICAL_ACCEL = 0.8 #gravity
        self.VERTICAL_JUMP_SPEED = 18 #determines how high the player can jump
        self.STARTING_HEALTH = 100
        self.STARTING_AMMO = 35
        
        #load image and get rect
        self.image = pygame.transform.scale(pygame.image.load("assets/player.png"), (32, 32))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)
        self.startingx = x
        self.startingy = y

        #create a mask for more accurate collisions
        self.mask = pygame.mask.from_surface(self.image)

        #attach sprite groups
        self.platform_group = platform_group
        self.bullet_group = bullet_group

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
        if keys[pygame.K_a]:
            self.accel.x = -1 * self.HORIZONTAL_ACCEL
        elif keys[pygame.K_d]:
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

    def jump(self):
        """Make the player jump"""
        #player can only jump if on the ground
        if pygame.sprite.spritecollide(self, self.platform_group, False):
            self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED

    def ranged_atk(self):
        """Make the player shoot a projectile"""
        Bullet(self.rect.centerx, self.rect.centery, self.bullet_group, self)

class Enemy(pygame.sprite.Sprite):
    """A class to represnt an enemy"""
    def __init__(self):
        """Initialize the enemy character"""
        pass

class Bullet(pygame.sprite.Sprite):
    """A class to represent a bullet that was fired either by the player or by an enemy"""
    def __init__(self, x, y, bullet_group, player):
        """Initialize the bullet"""
        super().__init__()

        #set constant variables
        self.VELOCITY = 30
        self.RANGE = 500

        #load image and get rect
        self.image = pygame.image.load("assets/bullet.png")
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

class Ammo(pygame.sprite.Sprite):
    """A class to represent an ammo pickup on the ground"""
    def __init__(self):
        """Initialzie the ammo"""
        pass

"""DEFINE GROUPS"""
my_main_tile_group = pygame.sprite.Group()
my_platform_group = pygame.sprite.Group()

my_player_group = pygame.sprite.Group()

my_bullet_group = pygame.sprite.Group()

"""Create a tile map and instantiate the tiles"""
#TILE MAP KEY
# 0 -> air, 1 -> dirt, 2 -> grass, 9 -> player spawn
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
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
            my_player = Player(j*32, i*32, my_player_group, my_platform_group, my_bullet_group)


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
            if event.key == pygame.K_w:
                my_player.ranged_atk()

    #draw bg
    DISPLAY_SURFACE.fill((0,0,0))

    #update and draw sprites
    my_main_tile_group.update()
    my_main_tile_group.draw(DISPLAY_SURFACE)

    my_player_group.update()
    my_player_group.draw(DISPLAY_SURFACE)

    my_bullet_group.update()
    my_bullet_group.draw(DISPLAY_SURFACE)

    #update display and tick clock
    pygame.display.update()
    CLOCK.tick(FPS)

pygame.quit()