import pygame
from settings import *
from tile import Tile
from weapon import Weapon
from player import Player, Sphere
from enemy import Enemy
from particles import AnimationPlayer
from ui import UI


class Level:
    def __init__(self, current_level, health, exp, bullet_resets):
        self.game_over = False
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = DrawSprites()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.health = health
        self.exp = exp
        self.bullet_resets = bullet_resets

        self.animation_player = AnimationPlayer()
        self.ui = UI()

        self.level_complete = False
        self.level_complete_data = None
        self.current_level = current_level

        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(self.current_level):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile('wall', (x, y), [self.visible_sprites, self.obstacle_sprites])
                else:
                    Tile('empty', (x, y), [self.visible_sprites])
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites,
                                         self.damage_enemy, self.trigger_death_particles,
                                         self.enemy_sprites, self.bullet_sprites,
                                         self.health, self.exp, self.bullet_resets)
                    self.sphere = Sphere(self.player, self.visible_sprites)
                elif col == 'b':
                    Enemy('bug', (x, y), [self.visible_sprites, self.enemy_sprites],
                          self.obstacle_sprites, self.damage_player, self.trigger_death_particles, 10,
                          self.bullet_sprites)
                elif col == 'c':
                    Enemy('clown', (x, y), [self.visible_sprites, self.enemy_sprites],
                          self.obstacle_sprites, self.damage_player, self.trigger_death_particles, 10,
                          self.bullet_sprites)
                elif col == 'g':
                    Enemy('ghost', (x, y), [self.visible_sprites, self.enemy_sprites],
                          self.obstacle_sprites, self.damage_player, self.trigger_death_particles, 10,
                          self.bullet_sprites)
                elif col == 'd':
                    Enemy('demondoor', (x, y), [self.visible_sprites, self.enemy_sprites],
                          self.obstacle_sprites, self.damage_player, self.trigger_death_particles, 10,
                          self.bullet_sprites)

    def damage_player(self, amount):
        if self.player.vulnerable and not self.player.godmod:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.trigger_death_particles(self.player.rect.center, 'sparkle')

        if self.player.health <= 0:
            self.game_over = True

    def damage_enemy(self, amount, enemy):
        if enemy.vulnerable:
            enemy.health -= amount
            enemy.vulnerable = False
            enemy.hit_time = pygame.time.get_ticks()

        if enemy.health <= 0:
            enemy.kill()
            self.trigger_death_particles(enemy.rect.center, 'smoke')
            self.player.exp += 100

    def clear_all_bullets(self):
        for bullet in self.bullet_sprites:
            bullet.kill()

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.visible_sprites.bullet_update(self.player)

        if not self.enemy_sprites:
            self.level_complete = True
            self.level_complete_data = [self.player.health, self.player.exp, self.player.bullet_resets]


class DrawSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in self.sprites():
            if sprite.name == 'empty':
                pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if sprite.name != 'empty':
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

    def bullet_update(self, player):
        bullet_sprites = [sprite for sprite in self.sprites() if
                          hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'bullet']
        for bullet in bullet_sprites:
            bullet.bullet_update(player)
