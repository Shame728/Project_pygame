import pygame
from settings import *


tile_images = {
    'wall': '../graphics/wall.png',
    'empty': '../graphics/floor.png',
}

tile_width = tile_height = TILESIZE


class Tile(pygame.sprite.Sprite):
    def __init__(self, type, pos, groups):
        super().__init__(groups)
        self.name = type
        self.image = pygame.image.load(tile_images[self.name]).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.width = tile_width
        self.rect.height = tile_height
        self.hitbox = self.rect.copy()
