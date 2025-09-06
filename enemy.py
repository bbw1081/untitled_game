import pygame, random
from enemy_bullet import EnemyBullet

vector = pygame.math.Vector2
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 736
FPS = 60

class Enemy(pygame.sprite.Sprite):
    """A class to represnt an enemy"""
    def __init__(self, x, y, platform_group, enemy_group, bullet_group, player, min_speed, max_speed):
        """Initialize the enemy character"""
        super().__init__()

        #set constants
        self.VERTICAL_ACCEL = 2 #gravity

        #load image and get rect
        self.image = pygame.transform.scale(pygame.image.load("assets/enemy.png"), (32, 32))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)
        
        #attach groups
        self.platform_group = platform_group
        self.player = player
        self.bullet_group = bullet_group

        #load in kinematcs
        self.position = vector(self.rect.x, self.rect.y)
        if self.position.x < self.player.position.x:
            self.direction = 1
        else:
            self.direction = -1
        self.speed = random.randint(min_speed, max_speed)
        self.velocity = vector(self.direction*self.speed, 0)
        self.accel = vector(0, self.VERTICAL_ACCEL)

        #set up fire rate
        self.fire_rate = random.randint(min_speed, max_speed)
        self.frame_count = 0
        self.time_passed = 0
        
        #add self to enemy group
        enemy_group.add(self)

    def update(self):
        """Update the enemy's position"""
        self.move()
        self.check_collisions()
        self.check_fire()

    def move(self):
        """Move the enemy based on simple AI"""
        #find the direction to the player
        if self.position.x < self.player.position.x:
            self.direction = 1
        else:
            self.direction = -1
        
        #update kinematics values
        self.velocity.x = self.direction*self.speed
        self.velocity += self.accel
        self.position += self.velocity + 0.5*self.accel

        #stop the enemy if they are hitting the wall
        if self.position.x < 0:
            self.position.x = 0
        if self.position.x > WINDOW_WIDTH - 32:
            self.position.x = WINDOW_WIDTH - 32

        #update rect
        self.rect.bottomleft = self.position

    def check_collisions(self):
        """Check for collisions with the ground"""
        collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
        if collided_platforms:
            self.position.y = collided_platforms[0].rect.top + 1
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
        