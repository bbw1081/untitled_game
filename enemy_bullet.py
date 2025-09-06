import pygame

class EnemyBullet(pygame.sprite.Sprite):
    """A class to represent a bullet shot by the enemy"""

    def __init__(self, x, y, bullet_group, npc):
        """Initialize the bullet"""
        super().__init__()

        #set constant variables
        self.VELOCITY = 30
        self.RANGE = 500

        #load image and get rect
        self.image = pygame.image.load("assets/bullet.png")
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
