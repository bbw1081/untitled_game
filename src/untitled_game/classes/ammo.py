import pygame, config

class Ammo(pygame.sprite.Sprite):
    """Represents an ammo pickup on the ground"""

    def __init__(self, x, y, ammo_group):
        """Initialzie the ammo"""
        super().__init__()

        #load image and get rect
        self.image = pygame.image.load("src/untitled_game/assets/ammo_pickup.png")
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
        if self.frame_count == config.FPS:
            self.time_passed += 1
        
        if self.time_passed == self.kill_time:
            self.kill()
