import pygame
from settings import *
from support import import_folder
from entity import Entity
from bullet import PlayerBullet


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, damage_enemy, trigger_death_particles, enemies, bullets,
                 health, exp, bullet_resets):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/player/down_idle/idle_down.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        self.import_player_assets()
        self.status = 'down'
        self.name = 'player'
        self.sprite_type = 'player'

        self.can_attack = True
        self.attack_cooldown = 200
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites
        self.damage_enemy = damage_enemy
        self.trigger_death_particles = trigger_death_particles

        self.bullet_resets = bullet_resets
        self.can_reset_bullets = True
        self.reset_bullets_cooldown = 200
        self.reset_bullets_time = None

        self.enemy_sprites = enemies
        self.bullet_sprites = bullets
        self.bullet_groups = (groups[0], bullets)

        self.health = health
        self.exp = exp
        self.speed = 3

        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        self.godmod = False
        self.can_switch_godmod = True
        self.godmod_switch_time = None
        self.godmod_duration_cooldown = 200

    def import_player_assets(self):
        character_path = '../graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        if keys[pygame.K_g] and self.can_switch_godmod:
            self.godmod = True if not self.godmod else False
            self.can_switch_godmod = False
            self.godmod_switch_time = pygame.time.get_ticks()

            if self.godmod:
                self.speed = 10

        if keys[pygame.K_SPACE] and self.can_reset_bullets and self.bullet_resets > 0:
            self.bullet_resets -= 1
            self.can_reset_bullets = False
            self.reset_bullets_time = pygame.time.get_ticks()

            for bullet in self.bullet_sprites:
                bullet.kill()

        if pygame.mouse.get_pressed()[0] and self.can_attack:
            PlayerBullet(self.name, (self.hitbox.centerx, self.hitbox.centery), self.bullet_groups,
                         self.obstacle_sprites, self.damage_enemy, self.trigger_death_particles, self.enemy_sprites)
            self.can_attack = False
            self.attack_time = pygame.time.get_ticks()

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.can_reset_bullets:
            if current_time - self.reset_bullets_time >= self.reset_bullets_cooldown:
                self.can_reset_bullets = True

        if not self.can_switch_godmod:
            if current_time - self.godmod_switch_time >= self.godmod_duration_cooldown:
                self.can_switch_godmod = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)


class Sphere(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        self.player = player
        self.distance = 50
        self.direction = pygame.Vector2(1, 0)
        self.name = 'sphere'

        super().__init__(groups)
        self.gun_surf = pygame.image.load('../graphics/magic_sphere.png').convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_rect(center=self.player.rect.center + self.direction * self.distance)

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(pygame.display.get_window_size()[0] / 2, pygame.display.get_window_size()[1] / 2)
        if mouse_pos != player_pos:
            self.direction = (mouse_pos - player_pos).normalize()

    def update(self):
        self.get_direction()
        self.rect.center = self.player.rect.center + self.direction * self.distance
