import pygame

#TODO, figure this stuff out

class MeleeAtk(pygame.sprite.Sprite):
    """A class to represent a melee attack that was performed by the player"""
    def __init__(self, x, y, melee_group, player):
        """Initialize the melee attack"""
        super().__init__()

        #set constant variables
        self.VELOCITY = 60
        self.RANGE = 50

        #load in image and get rect
        self.image = pygame.image.load("assets/melee_atk.png")
        if player.velocity.x < 0: #if the player is facing left flip the direction
            self.VELOCITY = -1*self.VELOCITY
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.startingx = x
        self.startingy = y

        melee_group.add(self)

    def update(self):
        """Update the melee attack's location"""
        self.rect.x += self.VELOCITY
        #if the melee attack has passed RANGE, kill it
        if abs(self.rect.x - self.startingx) > self.RANGE:
            self.kill()
