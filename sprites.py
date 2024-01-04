import pygame
from config import *
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites                          ##### adding the player to the all sprites group
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE                                        ##### setting the tile size to 32x32 bits (referenced in config.py)
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pygame.Surface([self.width, self.height])          ##### creating a surface, rectangle, 32 pix wide and 32 pix high
        self.image.fill(RED)
        self.x_change = 0
        self.y_change = 0
        self.facing = "down"

        self.rect = self.image.get_rect()                                   ##### setting the rectangle to the image (hit box and image of player will be the same size)
        self.rect.x = self.x
        self.rect.y = self.y