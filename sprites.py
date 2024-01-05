import pygame
from config import *
import math
import random


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])                ###Adding _surface to the sprite
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite
    
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

        
        self.x_change = 0
        self.y_change = 0
        self.facing = "down"
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(1, 642, self.width, self.height)          ##### creating a surface, rectangle, 32 pix wide and 32 pix high

        self.rect = self.image.get_rect()                                   ##### setting the rectangle to the image (hit box and image of player will be the same size)
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.character_spritesheet.get_sprite(1, 642, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(65, 642, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(129, 642, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(193, 642, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(257, 642, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(321, 642, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(385, 642, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(449, 642, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(513, 642, self.width, self.height)]

        self.up_animations = [self.game.character_spritesheet.get_sprite(1, 515, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(65, 515, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(129, 515, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(193, 515, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(257, 515, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(321, 515, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(385, 515, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(449, 515, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(513, 515, self.width, self.height)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(1, 578, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(65, 578, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(129, 578, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(193, 578, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(257, 578, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(321, 578, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(385, 578, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(449, 578, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(513, 578, self.width, self.height)]

        self.right_animations = [self.game.character_spritesheet.get_sprite(1, 705, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(65, 705, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(129, 705, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(193, 705, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(257, 705, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(321, 705, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(385, 705, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(449, 705, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(513, 705, self.width, self.height)]

    def update(self):
            self.movement()
            self.animate()
            self.collide_enemy()

            self.rect.x += self.x_change
            self.collide_blocks("x")
            self.rect.y += self.y_change
            self.collide_blocks("y")

            self.x_change = 0
            self.y_change = 0

    def movement(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                for sprite in self.game.all_sprites:
                    sprite.rect.x += PLAYER_SPEED
                self.x_change -= PLAYER_SPEED
                self.facing = "left"
            if keys[pygame.K_RIGHT]:
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= PLAYER_SPEED
                self.x_change += PLAYER_SPEED
                self.facing = "right"
            if keys[pygame.K_UP]:
                for sprite in self.game.all_sprites:
                    sprite.rect.y += PLAYER_SPEED
                self.y_change -= PLAYER_SPEED
                self.facing = "up"
            if keys[pygame.K_DOWN]:
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= PLAYER_SPEED
                self.y_change += PLAYER_SPEED
                self.facing = "down"

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)           ###### checking if the player collides with a block comparing the hit box
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

    def animate(self):
        
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 642, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 515, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 578, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 705, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(["left", "right"])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 35)

        self.direction = ""

        self.image = self.game.enemy_spritesheet.get_sprite(14 , 140, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.enemy_spritesheet.get_sprite(14, 140, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(65, 140, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(129, 140, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(193, 140, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(257, 140, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(321, 140, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(385, 140, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(449, 140, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(513, 140, self.width, self.height)]

        self.up_animations = [self.game.enemy_spritesheet.get_sprite(14, 10, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(65, 10, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(129, 10, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(193, 10, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(257, 10, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(321, 10, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(385, 10, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(449, 10, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(513, 10, self.width, self.height)]

        self.left_animations = [self.game.enemy_spritesheet.get_sprite(14, 65, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(65, 65, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(129, 65, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(193, 65, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(257, 65, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(321, 65, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(385, 65, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(449, 65, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(513, 65, self.width, self.height)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(14, 195, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(65, 195, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(129, 195, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(193, 195, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(257, 195, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(321, 195, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(385, 195, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(449, 195, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(513, 195, self.width, self.height)]

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement (self):
        if self.facing == "left":
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "right"
        if self.facing == "right":
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = "left"


    def animate(self):
        
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(14, 140, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(14, 10, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(14, 65, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(14, 195, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(789, 393, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(40, 829, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('04B_30__.ttf', fontsize)
        self.content = content
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg
        self.bg = bg
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)
        
    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.animation_loop = 0

        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        self.down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        self.up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]


    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing

        if direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += .5
            if self.animation_loop >= 5:
                self.kill()
        if direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += .5
            if self.animation_loop >= 5:
                self.kill()
        if direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += .5
            if self.animation_loop >= 5:
                self.kill()
        if direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += .5
            if self.animation_loop >= 5:
                self.kill()
