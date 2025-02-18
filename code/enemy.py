from settings import *
from entity import Entity
from bullet import Bullet
from support import *


class Enemy(Entity):
    def __init__(self, name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp, bullets):
        super().__init__(groups)
        self.bullet_groups = (groups[0], bullets)
        self.sprite_type = 'enemy'
        self.name = name

        self.status = 'idle'
        self.facing = 'left'
        self.import_graphics(name)

        self.image = self.left_animations['idle'][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)
        self.obstacle_sprites = obstacle_sprites

        monster_info = monster_data[self.name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.resistance = monster_info['resistance']
        self.notice_radius = monster_info['notice_radius']

        self.can_attack = True
        self.attack_time = None

        self.attack_cooldown = 500 if self.name != 'demondoor' else 1000

        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

        # sounds
        self.death_sound = pygame.mixer.Sound('../audio/death.wav')
        self.hit_sound = pygame.mixer.Sound('../audio/hit.wav')
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound.set_volume(0.6)
        self.hit_sound.set_volume(0.6)
        self.attack_sound.set_volume(0.6)

    def import_graphics(self, name):
        self.left_animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'../graphics/enemies/{name}/left/'
        for animation in self.left_animations.keys():
            self.left_animations[animation] = import_folder(main_path + animation)

        self.right_animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'../graphics/enemies/{name}/right/'
        for animation in self.right_animations.keys():
            self.right_animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.notice_radius:
            if distance <= 100:
                self.kill()
                player.exp += 100
            self.status = 'attack'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack' and self.can_attack:
            self.can_attack = False
            self.attack_time = pygame.time.get_ticks()
            if self.name == 'demondoor':
                Bullet(self.name, (self.hitbox.centerx - 10, self.hitbox.centery), self.bullet_groups,
                       self.obstacle_sprites, self.damage_player,
                       self.trigger_death_particles, player.hitbox.center)
                Bullet(self.name, (self.hitbox.centerx - 30, self.hitbox.centery), self.bullet_groups,
                       self.obstacle_sprites, self.damage_player,
                       self.trigger_death_particles, player.hitbox.center)
                Bullet(self.name, (self.hitbox.centerx, self.hitbox.centery - 10), self.bullet_groups,
                       self.obstacle_sprites, self.damage_player,
                       self.trigger_death_particles, player.hitbox.center)
                Bullet(self.name, (self.hitbox.centerx, self.hitbox.centery - 30), self.bullet_groups,
                       self.obstacle_sprites, self.damage_player,
                       self.trigger_death_particles, player.hitbox.center)
            elif self.name == 'ghost':
                Bullet(self.name, (self.hitbox.x, self.hitbox.y), self.bullet_groups,
                       self.obstacle_sprites, self.damage_player, self.trigger_death_particles)
            else:
                Bullet(self.name, (self.hitbox.centerx, self.hitbox.y), self.bullet_groups,
                       self.obstacle_sprites, self.damage_player,
                       self.trigger_death_particles, player.hitbox.center)
            self.attack_sound.play()
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.left_animations[self.status] if self.facing == 'left' else self.right_animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.name)
            self.add_exp(self.exp)
            self.death_sound.play()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
