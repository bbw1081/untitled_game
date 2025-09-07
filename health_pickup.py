import pygame

FPS = 60

class HealthPickup(pygame.sprite.Sprite):
    """A class to represent a health pickup dropped by an enemy"""
    def __init__(self, x, y, health_group):
        """Initialize the Health pickup"""
        super().__init__()

        #load image and get rect
        self.image = pygame.image.load("assets/health_pickup.png")
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
