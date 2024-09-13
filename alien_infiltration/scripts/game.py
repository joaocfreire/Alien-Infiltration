import sys
import random
from alien_infiltration.scripts.utils import *
from alien_infiltration.scripts.tilemap import Tilemap
from alien_infiltration.scripts.entities import Player, WalkingEnemy, FlyingEnemy, Boss


LEVEL_LIMIT = 2880
OFFSETS = [0, 8, 4, 4]


class Game:
    def __init__(self, controls):
        pygame.init()

        pygame.display.set_caption('alien infiltration')
        self.screen = pygame.display.set_mode((1366, 768))
        self.display = pygame.Surface((400, 225), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((400, 225))

        self.controls = controls

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            'tileset_0': load_tileset('environments/tilesets/0', 5, 5),
            'tileset_1': load_tileset('environments/tilesets/1', 3, 8),
            'tileset_2': load_tileset('environments/tilesets/2', 2, 5),
            'barrier': load_images('environments/tilesets/barrier'),
            'backgrounds': load_images('environments/backgrounds'),
            'life_bar/player': load_images('life_bar/player'),
            'life_bar/boss': load_images('life_bar/boss'),
            'screens': load_images('screens'),
            'walking_enemy/idle': Animation(load_spritesheet('entities/alien_walking_enemy/idle.png', 1, 4), img_dur=8),
            'walking_enemy/run': Animation(load_spritesheet('entities/alien_walking_enemy/run.png', 1, 6), img_dur=6),
            'walking_enemy/die': Animation(load_spritesheet('entities/alien_walking_enemy/die.png', 1, 8), loop=False),
            'walking_enemy_recolor/idle': Animation(load_spritesheet('entities/alien_walking_enemy_recolor/idle.png', 1, 4), img_dur=8),
            'walking_enemy_recolor/run': Animation(load_spritesheet('entities/alien_walking_enemy_recolor/run.png', 1, 6), img_dur=6),
            'walking_enemy_recolor/die': Animation(load_spritesheet('entities/alien_walking_enemy_recolor/die.png', 1, 8), loop=False),
            'flying_enemy/idle': Animation(load_spritesheet('entities/alien_flying_enemy/idle.png', 1, 8), img_dur=4),
            'flying_enemy/die': Animation(load_spritesheet('entities/alien_flying_enemy/die.png', 1, 8), loop=False),
            'flying_enemy_recolor/idle': Animation(load_spritesheet('entities/alien_flying_enemy_recolor/idle.png', 1, 8), img_dur=4),
            'flying_enemy_recolor/die': Animation(load_spritesheet('entities/alien_flying_enemy_recolor/die.png', 1, 8), loop=False),
            'boss/idle': Animation(load_spritesheet('entities/boss/idle.png', 4, 8), img_dur=7),
            'boss/shoot': Animation(load_spritesheet('entities/boss/shoot.png', 4, 8), img_dur=4, loop=False),
            'boss/damage': Animation(load_spritesheet('entities/boss/damage.png', 4, 8), img_dur=8, loop=False),
            'boss/die': Animation(load_spritesheet('entities/boss/die.png', 2, 8), img_dur=8, loop=False),
            'player/idle': Animation(load_spritesheet('entities/player/idle.png', 1, 4), img_dur=15),
            'player/run': Animation(load_spritesheet('entities/player/run.png', 2, 5)),
            'player/jump': Animation(load_spritesheet('entities/player/jump.png', 1, 6), img_dur=10),
            'player/smoke': Animation(load_spritesheet('entities/player/smoke.png', 1, 8), loop=False),
            'player/shoot': Animation(load_spritesheet('entities/player/shoot.png', 1, 2), img_dur=10),
            'player/run_shoot': Animation(load_spritesheet('entities/player/run_shoot.png', 2, 5)),
            'player/jump_shoot': Animation(load_spritesheet('entities/player/jump_shoot.png', 1, 6), img_dur=10),
            'player/die': Animation(load_spritesheet('entities/player/die.png', 1, 3), img_dur=25, loop=False),
            'player_projectile/idle': Animation(load_spritesheet('entities/player_projectile/idle.png', 1, 2)),
            'player_projectile/impact': Animation(load_spritesheet('entities/player_projectile/impact.png', 1, 2), img_dur=10, loop=False),
            'boss_projectile/idle': Animation(load_spritesheet('entities/boss_projectile/idle.png', 1, 4)),
            'explosion': Animation(load_spritesheet('explosion/explosion.png', 1, 9)),
            }

        self.sfx = {
            'player/jump': pygame.mixer.Sound('data/sfx/player_jump.wav'),
            'player/shoot': pygame.mixer.Sound('data/sfx/player_shoot.wav'),
            'player/die': pygame.mixer.Sound('data/sfx/player_die.wav'),
            'enemies/die': pygame.mixer.Sound('data/sfx/enemie_die.wav'),
            'boss/shoot': pygame.mixer.Sound('data/sfx/boss_shoot.wav'),
            'boss/damage': pygame.mixer.Sound('data/sfx/boss_damage.wav'),
            'boss/die': pygame.mixer.Sound('data/sfx/boss_die.wav'),
            'explosion': pygame.mixer.Sound('data/sfx/explosion.wav'),
            'projectile/impact': pygame.mixer.Sound('data/sfx/projectile_impact.wav'),
            'coin': pygame.mixer.Sound('data/sfx/coin.wav'),
            'button': pygame.mixer.Sound('data/sfx/button_click.wav')
        }

        self.sfx['player/jump'].set_volume(0.9)
        self.sfx['player/shoot'].set_volume(0.1)
        self.sfx['player/die'].set_volume(0.5)
        self.sfx['enemies/die'].set_volume(0.4)
        self.sfx['boss/shoot'].set_volume(0.5)
        self.sfx['boss/damage'].set_volume(0.5)
        self.sfx['boss/die'].set_volume(0.2)
        self.sfx['explosion'].set_volume(0.2)
        self.sfx['projectile/impact'].set_volume(0.2)
        self.sfx['coin'].set_volume(0.2)
        self.sfx['button'].set_volume(0.2)

        self.musics = [
            'data/musics/dark_happy_world.wav',
            'data/musics/bipedal_mech.wav',
            'data/musics/going_up.wav',
            'data/musics/boss_fight_2.wav',
            'data/musics/game_over.wav',
            'data/musics/heros_determination.wav'
        ]

        self.music_start = False

        self.font = pygame.font.Font('data/retro_gaming.ttf', 10)

        self.life = 3
        self.time = 18060
        self.score = 0

        self.scroll = [0, 0]
        self.screenshake = 0
        self.transition = -50

        self.level = 0
        self.offset = OFFSETS[self.level]

        self.enemies = []
        self.projectiles = []

        self.double_jump = False
        self.player = Player(self, (50, 50), (32, 32), self.offset)

        self.boss = None
        self.boss_projectiles = []

        self.easter_egg = None

        self.tilemap = Tilemap(self, tile_size=32)
        self.load_level(self.level)

    def load_level(self, map_id):
        pygame.mixer.music.stop()
        self.music_start = False

        transition(self.screen, self.display, f'LEVEL {self.level + 1}', self.font,
                   (self.display.get_width()//2 - 25, self.display.get_height()//2), self.level)
        self.tilemap.load(f'data/maps/{map_id}.json')

        self.offset = OFFSETS[self.level]

        self.double_jump = False if self.level < 2 else True

        self.player = Player(self, (50, 50), (32, 32), self.offset)
        self.boss = None

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1), ('spawners', 2), ('spawners', 3),
                                             ('spawners', 4), ('spawners', 5), ('spawners', 6)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            elif spawner['variant'] == 1:
                self.enemies.append(WalkingEnemy(self, spawner['pos'], (32, 32), 0, self.offset + 5))
            elif spawner['variant'] == 2:
                self.enemies.append(WalkingEnemy(self, spawner['pos'], (32, 32), 1, self.offset + 5))
            elif spawner['variant'] == 3:
                self.enemies.append(FlyingEnemy(self, spawner['pos'], (32, 32), 0, self.offset - 26))
            elif spawner['variant'] == 4:
                self.enemies.append(FlyingEnemy(self, spawner['pos'], (32, 32), 1, self.offset - 26))
            elif spawner['variant'] == 5:
                self.boss = Boss(self, spawner['pos'], (32, 32), self.offset - 150)

        self.easter_egg = pygame.Rect(1376, 383, 32, 32) if self.level == 0 else None

        self.time = 18060
        self.score = 0

        self.projectiles = []
        self.scroll = [0, 0]
        self.transition = -50

    def game_over(self):
        self.display.fill((0, 0, 0, 0))

        self.music_start = False
        pygame.mixer.music.load(self.musics[-2])
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play()

        while True:
            self.display.blit(pygame.transform.scale(self.assets['screens'][0], self.display.get_size()), (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True
                    if event.key == pygame.K_ESCAPE:
                        return False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()

    def end_game(self):
        self.display.fill((0, 0, 0))

        self.music_start = False
        pygame.mixer.music.load(self.musics[-1])
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play()

        while True:
            self.display.blit(pygame.transform.scale(self.assets['screens'][1], self.display.get_size()), (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        return

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()

    def quit(self):
        click = False

        paused = load_image('menu/paused.png')

        buttons = {
            'resume': Button('menu/buttons/resume.png', 'menu/selected_buttons/resume.png'),
            'quit': Button('menu/buttons/quit.png', 'menu/selected_buttons/quit.png'),
        }

        while True:
            self.screen.blit(pygame.transform.scale(load_image('menu/background.png'), self.screen.get_size()), (0, 0))

            self.screen.blit(paused, ((self.screen.get_width() - paused.get_width()) / 2, 120))
            i = 10
            for b in buttons:
                buttons[b].update()
                buttons[b].draw(self.screen, (self.screen.get_width() - buttons[b].width) / 2,
                                self.screen.get_height() / 2 + i)
                i += 120

            mx, my = pygame.mouse.get_pos()

            if buttons['resume'].collided((mx, my)):
                if click:
                    self.sfx['button'].play()
                    return False

            if buttons['quit'].collided((mx, my)):
                if click:
                    self.sfx['button'].play()
                    return True

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()

    def run(self):
        collided = False
        while True:
            if not self.music_start:
                pygame.mixer.music.load(self.musics[self.level])
                pygame.mixer.music.set_volume(0.05)
                pygame.mixer.music.play(-1)
                self.music_start = True

            self.display.fill((0, 0, 0, 0))
            self.display_2.blit(pygame.transform.scale(self.assets['backgrounds'][self.level], self.display.get_size()),
                                (0, 0))

            self.screenshake = max(0, self.screenshake - 1)

            if self.time == 60:
                self.player.die()

            if self.player.pos[0] == LEVEL_LIMIT:
                self.transition += 1
                if self.transition > 50:
                    self.level += 1
                    self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1

            if self.player.dead and self.player.count_die <= 25:
                self.transition = min(50, self.transition + 1)
                if self.player.count_die == 1:
                    self.life -= 1
                    if self.life == 0:
                        restart = self.game_over()
                        if not restart:
                            return
                        self.life = 3
                        self.level = 0
                    self.load_level(self.level)

            if self.score == 10000 and not self.boss:
                self.transition = min(50, self.transition + 0.2)
                if self.transition == 50:
                    self.end_game()
                    return

            if self.easter_egg is not None:
                if self.player.rect().colliderect(self.easter_egg):
                    if not collided:
                        self.sfx['coin'].play()
                        collided = True
                    self.transition += 1.3
                    if self.transition > 50:
                        self.level = 3
                        self.load_level(self.level)

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 10
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 10
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            self.display.blit(self.font.render(f'TIME: {self.time//60}', True, (255, 255, 255)), (10, 8))
            self.display.blit(self.font.render(f'SCORE: {self.score}', True, (255, 255, 255)), (10, 23))

            for enemy in self.enemies.copy():
                enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if enemy.dead and enemy.count_die == 1:
                    self.enemies.remove(enemy)
                if self.player.rect().colliderect(enemy.rect()) and not self.player.dead and not enemy.dead:
                    self.screenshake = max(16, self.screenshake)
                    self.player.die()

            if self.boss is not None:
                self.boss.render(self.display, offset=render_scroll)
                self.boss.update(self.tilemap, (0, 0))
                if self.player.rect().colliderect(self.boss.hitbox) and not self.player.dead and not self.boss.dead:
                    self.screenshake = max(16, self.screenshake)
                    self.player.die()
                if self.boss.dead and self.boss.count_die == 1:
                    self.boss = None

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            for projectile in self.projectiles.copy():
                projectile.update(self.tilemap, (0, 0))
                projectile.render(self.display, offset=render_scroll)
                if (projectile.hit and projectile.count == 1) or (projectile.distance > 64):
                    self.projectiles.remove(projectile)
                for enemy in self.enemies:
                    if enemy.rect().colliderect(projectile.rect()) and not projectile.hit and not enemy.dead:
                        self.screenshake = max(16, self.screenshake)
                        try:
                            self.projectiles.remove(projectile)
                        except ValueError:
                            pass
                        self.score += 100
                        enemy.die()
                if self.boss is not None:
                    if projectile.rect().colliderect(self.boss.hitbox) and not self.boss.invulnerability:
                        self.screenshake = max(16, self.screenshake)
                        self.projectiles.remove(projectile)
                        self.score += 100
                        self.boss.damage()

            for boss_projectile in self.boss_projectiles:
                boss_projectile.update(self.tilemap, (0, 0))
                boss_projectile.render(self.display, offset=render_scroll)
                if boss_projectile.distance > 500:
                    self.boss_projectiles.remove(boss_projectile)
                elif self.player.rect().colliderect(boss_projectile) and not self.player.dead:
                    self.screenshake = max(16, self.screenshake)
                    self.boss_projectiles.remove(boss_projectile)
                    self.player.die()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and not self.player.dead:

                    if self.controls == 'ARROWKEYS':
                        if event.key == pygame.K_LEFT:
                            self.movement[0] = True
                        if event.key == pygame.K_RIGHT:
                            self.movement[1] = True
                        if event.key == pygame.K_UP:
                            self.player.jump()

                    elif self.controls == 'WASD':
                        if event.key == pygame.K_a:
                            self.movement[0] = True
                        if event.key == pygame.K_d:
                            self.movement[1] = True
                        if event.key == pygame.K_w:
                            self.player.jump()

                    if event.key == pygame.K_SPACE:
                        self.player.shoot()
                    if event.key == pygame.K_ESCAPE:
                        quit = self.quit()
                        if quit:
                            return

                if event.type == pygame.KEYUP:
                    if self.controls == 'ARROWKEYS':
                        if event.key == pygame.K_LEFT:
                            self.movement[0] = False
                        if event.key == pygame.K_RIGHT:
                            self.movement[1] = False

                    elif self.controls == 'WASD':
                        if event.key == pygame.K_a:
                            self.movement[0] = False
                        if event.key == pygame.K_d:
                            self.movement[1] = False

            display_mask = pygame.mask.from_surface(self.display)
            display_sillhoette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display_2.blit(display_sillhoette, offset)

            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255),
                                   (self.display.get_width() // 2, self.display.get_height() // 2),
                                   (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))

            self.display_2.blit(self.display, (0, 0))
            if not self.transition:
                self.display_2.blit(self.assets['life_bar/player'][self.life], (5, 195))
                if self.boss is not None:
                    img = self.assets['life_bar/boss'][self.boss.life]
                    self.display_2.blit(img, ((self.display.get_width() - img.get_width())/2, 6))

            screenshake_offset = (
                random.random() * self.screenshake - self.screenshake / 2,
                random.random() * self.screenshake - self.screenshake / 2)

            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), screenshake_offset)

            pygame.display.update()

            self.time -= 1
            self.clock.tick(60)
