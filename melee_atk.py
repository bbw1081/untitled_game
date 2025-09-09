import pygame

class MeleeAtk(pygame.sprite.Sprite):
    """A class to represent a melee attack that was performed by the player"""
    def __init__(self, melee_group, player):
        """Initialize the melee attack"""
        super().__init__()

        self.frame_count = 0

        self.player = player

        #load in image and get rect
        self.image = pygame.transform.scale(pygame.image.load("assets/melee_atk.png"), (64, 32))
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
        if self.frame_count >= 2:
            self.kill()
        else:
            if self.player.velocity.x > 0: #moving right
                self.rect.bottomleft = (self.player.rect.right, self.player.rect.bottom)
            else: #moving left
                self.rect.bottomright = (self.player.rect.left, self.player.rect.bottom)

        