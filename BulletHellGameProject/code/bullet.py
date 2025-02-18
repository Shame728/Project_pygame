from settings import *
from entity import Entity
from support import *


class Bullet(Entity):
    def __init__(self, name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, direction=None):
        super().__init__(groups)
        self.name = f'{name}_bullet'
        self.sprite_type = 'bullet'
        self.status = 'move'

        self.image = pygame.image.load(f'../graphics/{self.name}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)
        self.obstacle_sprites = obstacle_sprites

        if direction:
            bullet_vec = pygame.math.Vector2(self.rect.center)
            player_vec = pygame.math.Vector2(direction)
            self.direction = (player_vec - bullet_vec)

        self.bullet_info = monster_data[f'{name}']
        self.speed = self.bullet_info['bullet_speed']
        self.attack_damage = self.bullet_info['damage']

        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles

        self.death_sound = pygame.mixer.Sound('../audio/death.wav')
        self.attack_sound = pygame.mixer.Sound('../audio/hit.wav')
        self.clown_collide_sound = pygame.mixer.Sound('../audio/collide.wav')
        self.death_sound.set_volume(0.2)
        self.attack_sound.set_volume(0.6)
        self.clown_collide_sound.set_volume(0.3)

    def get_player_distance(self, player):
        bullet_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - bullet_vec).magnitude()

        return distance

    def ghost_bullet_movement(self, player):
        bullet_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)

        direction = (player_vec - bullet_vec).normalize()
        return direction

    def demondoor_bullet_movement(self):
        direction = pygame.math.Vector2(0, 1)
        return direction

    def update(self):
        self.move(self.speed)

    def bullet_update(self, player):
        if self.name != 'player_bullet':
            distance = self.get_player_distance(player)

            if distance <= 50:
                self.damage_player(self.attack_damage)
                self.attack_sound.play()
                self.kill()
            else:
                if self.name == 'ghost_bullet':
                    self.direction = self.ghost_bullet_movement(player)
        else:
            pass


class PlayerBullet(Entity):
    def __init__(self, name, pos, groups, obstacle_sprites, damage_enemy, trigger_death_particles, enemies):
        super().__init__(groups)
        self.name = f'{name}_bullet'
        self.sprite_type = 'bullet'
        self.status = 'move'

        self.pos = pos
        self.groups = groups
        self.obstacle_sprites = obstacle_sprites
        self.damage_enemy = damage_enemy
        self.trigger_death_particles = trigger_death_particles
        self.enemies = enemies

        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(pygame.display.get_window_size()[0] / 2, pygame.display.get_window_size()[1] / 2)
        if mouse_pos != player_pos:
            self.direction = (mouse_pos - player_pos).normalize()


        center = self.pos + self.direction * 50
        self.image = pygame.image.load(f'../graphics/{self.name}.png').convert_alpha()
        self.rect = self.image.get_rect(center=center)
        self.hitbox = self.rect.inflate(0, 0)
        self.obstacle_sprites = obstacle_sprites

        self.bullet_info = monster_data[f'{name}']
        self.speed = self.bullet_info['bullet_speed']
        self.attack_damage = self.bullet_info['damage']
        self.attack_type = self.bullet_info['attack_type']

        self.death_sound = pygame.mixer.Sound('../audio/death.wav')
        self.attack_sound = pygame.mixer.Sound('../audio/hit.wav')
        self.clown_collide_sound = pygame.mixer.Sound('../audio/collide.wav')
        self.death_sound.set_volume(0.2)
        self.attack_sound.set_volume(0.6)
        self.clown_collide_sound.set_volume(0.3)

    def update(self):
        self.move(self.speed)

    def bullet_update(self, player):
        for enemy in self.enemies:
            if self.rect.colliderect(enemy.rect):
                self.kill()
                self.damage_enemy(self.attack_damage, enemy)
