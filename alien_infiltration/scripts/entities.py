import random
import pygame


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size, offset=0):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.offset = offset
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')
        self.animation = self.game.assets[f'{self.type}/{self.action}'].copy()

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[f'{self.type}/{self.action}'].copy()

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_arround(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_arround(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.velocity[1] = min([5, self.velocity[1] + 0.1])

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False),
                  (self.pos[0] - offset[0] + self.anim_offset[0],
                   self.pos[1] - offset[1] + self.anim_offset[1] + self.offset))


class WalkingEnemy(PhysicsEntity):
    def __init__(self, game, pos, size, color=0, offset=0):
        if color == 0:
            super().__init__(game, 'walking_enemy', pos, size, offset)
        elif color == 1:
            super().__init__(game, 'walking_enemy_recolor', pos, size, offset)
        self.walking = 0
        self.flip = True
        self.dead = False
        self.count_die = 0

    def update(self, tilemap, movement=(0, 0)):
        dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1] - self.offset)

        if self.walking and abs(dis[1]) > 32:
            if tilemap.solid_check((self.rect().centerx + (-12 if self.flip else 16), self.pos[1] + 32)):
                if self.collisions['right'] or self.collisions['left']:
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)

        if tilemap.solid_check((self.rect().x + (0 if self.flip else 36), self.pos[1] + 32)) and abs(dis[1]) <= 32:
            if -160 < dis[0] < 0:
                movement = (movement[0] - 0.5, movement[1])
            elif 0 < dis[0] < 160:
                movement = (movement[0] + 0.5, movement[1])

        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)

        if self.dead:
            self.set_action('die')
            self.count_die -= 1
            if self.count_die == 0:
                self.dead = False

        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

        super().update(tilemap, movement=movement)

    def die(self):
        self.dead = True
        self.count_die = 40
        self.game.sfx['enemies/die'].play()

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)


class FlyingEnemy(PhysicsEntity):
    def __init__(self, game, pos, size, color=0, offset=0):
        if color == 0:
            super().__init__(game, 'flying_enemy', pos, size, offset)
        elif color == 1:
            super().__init__(game, 'flying_enemy_recolor', pos, size, offset)
        self.walking = 0
        self.flip = True
        self.dead = False
        self.count_die = 0

    def update(self, tilemap, movement=(0, 0)):
        dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1] - self.offset)

        if self.walking and abs(dis[1]) > 32:
            if tilemap.solid_check((self.rect().centerx + (-12 if self.flip else 32), self.pos[1] + 32)):
                if self.collisions['right'] or self.collisions['left']:
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)

        if tilemap.solid_check((self.rect().x + (0 if self.flip else 56), self.pos[1] + 32)) and abs(dis[1]) <= 32:
            if -160 < dis[0] < 0:
                movement = (movement[0] - 0.5, movement[1])
            elif 0 < dis[0] < 160:
                movement = (movement[0] + 0.5, movement[1])

        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)

        if self.dead:
            self.set_action('die')
            self.count_die -= 1
            if self.count_die == 0:
                self.dead = False

        else:
            self.set_action('idle')

        super().update(tilemap, movement=movement)

    def die(self):
        self.dead = True
        self.count_die = 40
        self.game.sfx['enemies/die'].play()

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)


class Player(PhysicsEntity):
    def __init__(self, game, pos, size, offset=0):
        super().__init__(game, 'player', pos, size, offset)
        self.air_time = 0
        self.jumps = 2 if self.game.double_jump else 1

        self.jump_pos = (0, 0)
        self.smoke = self.game.assets['player/smoke'].copy()
        self.count_smoke = 0

        self.shooting = False
        self.count_shot = 0

        self.dead = False
        self.count_die = 0

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        self.air_time += 1

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 2 if self.game.double_jump else 1

        if self.count_smoke:
            self.count_smoke -= 1
            self.smoke.update()
            self.game.display.blit(self.smoke.img(), (self.jump_pos[0] - self.smoke.img().get_width() / 4 - self.game.scroll[0] + 8, self.jump_pos[1] - self.game.scroll[1] + self.game.offset)) if self.flip else self.game.display.blit(self.smoke.img(), (self.jump_pos[0] - self.smoke.img().get_width() / 4 - self.game.scroll[0], self.jump_pos[1] - self.game.scroll[1] + self.game.offset))

        if self.air_time == 120:
            self.game.screenshake = max(16, self.game.screenshake)
            self.die()

        if self.dead:
            self.set_action('die')
            self.count_die -= 1
            if self.count_die == 0:
                self.dead = False

        elif self.shooting:

            if self.count_shot == 20 and len(self.game.projectiles) <= 2:

                if self.air_time > 4:
                    self.set_action('jump_shoot')
                    self.game.projectiles.append(PlayerProjectile(self.game, [self.rect().centerx - 16 if self.flip else self.rect().centerx + 16, self.rect().centery + self.offset - 3], (9, 4), self.flip))
                elif movement[0] != 0:
                    self.set_action('run_shoot')
                    self.game.projectiles.append(PlayerProjectile(self.game, [self.rect().centerx - 16 if self.flip else self.rect().centerx + 16, self.rect().centery + self.offset - 1], (9, 4), self.flip))
                else:
                    self.set_action('shoot')
                    self.game.projectiles.append(PlayerProjectile(self.game, [self.rect().centerx - 16 if self.flip else self.rect().centerx + 16, self.rect().centery + self.offset - 6], (9, 4), self.flip))
                self.game.sfx['player/shoot'].play()

            self.count_shot -= 1
            if self.count_shot == 0:
                self.shooting = False

                if self.air_time > 4:
                    self.set_action('jump')
                elif movement[0] != 0:
                    self.set_action('run')
                else:
                    self.set_action('idle')

        elif self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

    def jump(self):
        if self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5

            self.count_smoke = 40
            self.smoke = self.game.assets['player/smoke'].copy()
            self.jump_pos = self.pos.copy()

            self.game.sfx['player/jump'].play()

    def shoot(self):
        self.shooting = True
        self.count_shot = 20

    def die(self):
        self.dead = True
        self.count_die = 75
        self.game.movement = [False, False]
        pygame.mixer.music.stop()
        self.game.sfx['player/die'].play()

    def render(self, surf, offset=(0, 0)):
        if self.flip and self.shooting and self.action in ('shoot', 'run_shoot', 'jump_shoot'):
            surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False),
                      (self.pos[0] - offset[0] + self.anim_offset[0] - 17,
                       self.pos[1] - offset[1] + self.anim_offset[1] + self.offset))
        else:
            super().render(surf, offset=offset)


class PlayerProjectile(PhysicsEntity):
    def __init__(self, game, pos, size, flip=False):
        super().__init__(game, 'player_projectile', pos, size)
        self.flip = flip
        self.velocity = [2, 0]
        self.distance = 0
        self.hit = False
        self.count = 0

    def update(self, tilemap, movement=(0, 0)):

        self.distance += 1

        if self.flip:
            self.pos[0] -= self.velocity[0]
        else:
            self.pos[0] += self.velocity[0]

        if tilemap.solid_check(self.rect()):
            self.hit = True
            self.count = 20
            self.velocity[0] = 0
            self.pos[0] = self.rect().centerx + 1 if self.flip else self.rect().centerx + self.offset - 23
            self.pos[1] = self.rect().centery - 9
            self.game.sfx['projectile/impact'].play()

        if self.hit:
            self.set_action('impact')
            self.count -= 1
            if self.count == 0:
                self.hit = False
        else:
            self.set_action('idle')

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)


class Boss(PhysicsEntity):
    def __init__(self, game, pos, size, offset=0):
        super().__init__(game, 'boss', pos, size, offset)

        self.hitbox = pygame.Rect(410, 66, 192, 192)

        self.shooting = False
        self.count_shot = 0

        self.damaged = False
        self.count_damage = 0

        self.dead = False
        self.count_die = 0

        self.explosion_pos = (0, 0)
        self.explosion = self.game.assets['explosion'].copy()
        self.exploded = False
        self.count_explosion = 0

        self.life = 10
        self.invulnerability = False
        self.countdown = 300

    def update(self, tilemap, movement=(0, 0)):

        if self.life == 0 and not self.dead:
            self.die()

        self.countdown -= 1
        if self.countdown == 0 and not self.dead:
            self.shoot()

        if self.exploded:
            if self.count_explosion % 23 == 0:
                self.game.sfx['explosion'].play()
            self.count_explosion -= 1
            self.explosion.update()
            self.game.display.blit(pygame.transform.scale(self.explosion.img(), (224, 256)),
                                   (self.explosion_pos[0] - self.game.scroll[0] - 20,
                                    self.explosion_pos[1] + self.explosion.img().get_height() - self.game.scroll[1] - 300))
            if self.count_explosion == 0:
                self.exploded = False

        elif self.dead:
            self.set_action('die')
            self.count_die -= 1
            self.game.score += 90
            if self.count_die == 0:
                self.dead = False
                self.explode()

        elif self.damaged:
            self.set_action('damage')
            self.count_damage -= 1
            if self.count_damage == 0:
                self.damaged = False

        elif self.shooting:
            if self.count_shot == 100:
                self.set_action('shoot')

            elif self.count_shot == 20:
                self.game.boss_projectiles.append(BossProjectile(self.game, [self.rect().centerx - 20,
                                                                             self.rect().centery - 85], (90, 33)))
                self.game.sfx['boss/shoot'].play()

            self.count_shot -= 1
            if self.count_shot == 0:
                self.countdown = 300
                self.shooting = False
                self.invulnerability = False

        else:
            self.set_action('idle')

        if not self.exploded:
            super().update(tilemap, movement=movement)

    def shoot(self):
        self.shooting = True
        self.count_shot = 100

    def damage(self):
        self.damaged = True
        self.invulnerability = True
        self.count_damage = 128
        self.life -= 1
        self.game.sfx['boss/damage'].play()

    def die(self):
        self.dead = True
        self.count_die = 100
        pygame.mixer.music.stop()
        self.game.sfx['boss/die'].play()

    def explode(self):
        self.exploded = True
        self.count_explosion = 207
        self.explosion = self.game.assets['explosion'].copy()
        self.explosion_pos = self.pos.copy()

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)


class BossProjectile(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'boss_projectile', pos, size)
        self.velocity = [3, 0]
        self.distance = 0

    def update(self, tilemap, movement=(0, 0)):

        self.distance += 1
        self.pos[0] -= self.velocity[0]
        self.set_action('idle')
        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)
