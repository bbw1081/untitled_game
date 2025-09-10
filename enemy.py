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
        self.VERTICAL_JUMP_SPEED = 27

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
        