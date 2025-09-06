import pygame

from player_bullet import PlayerBullet
from melee_atk import MeleeAtk

#use 2d vectors
vector = pygame.math.Vector2

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 736

class Player(pygame.sprite.Sprite):
    """A class to represent the player"""
    def __init__(self, x, y, player_group, platform_group, bullet_group, melee_group):
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
        MeleeAtk(self.rect.centerx, self.rect.centery, self.melee_group, self)
