import pygame

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
