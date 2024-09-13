import sys
import pygame
from scripts.game import Game
from scripts.utils import load_image, Button


class Menu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('alien infiltration')
        self.screen = pygame.display.set_mode((1366, 768))

        self.control = 'ARROWKEYS'
        self.click = False

        self.sound_button = pygame.mixer.Sound('data/sfx/button_click.wav')
        self.sound_button.set_volume(0.2)
        self.music_start = False

    def main(self):

        logo = load_image('menu/logo.png')

        buttons = {
            'play': Button('menu/buttons/play.png', 'menu/selected_buttons/play.png'),
            'controls': Button('menu/buttons/controls.png', 'menu/selected_buttons/controls.png'),
            'exit': Button('menu/buttons/exit.png', 'menu/selected_buttons/exit.png')
        }

        while True:

            if not self.music_start:
                pygame.mixer.music.load('data/musics/up_and_right.wav')
                pygame.mixer.music.set_volume(0.08)
                pygame.mixer.music.play(-1)
                self.music_start = True

            self.screen.blit(pygame.transform.scale(load_image('menu/background.png'), self.screen.get_size()), (0, 0))

            self.screen.blit(logo, ((self.screen.get_width() - logo.get_width()) / 2, 120))
            i = 10
            for b in buttons:
                buttons[b].update()
                buttons[b].draw(self.screen, (self.screen.get_width() - buttons[b].width) / 2,
                                self.screen.get_height() / 2 + i)
                i += 120

            mx, my = pygame.mouse.get_pos()

            if buttons['play'].collided((mx, my)):
                if self.click:
                    self.sound_button.play()
                    Game(self.control).run()
                    self.music_start = False

            if buttons['controls'].collided((mx, my)):
                if self.click:
                    self.sound_button.play()
                    self.click = False
                    self.control = self.controls()

            if buttons['exit'].collided((mx, my)):
                if self.click:
                    self.sound_button.play()
                    return

            self.click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True

            pygame.display.update()

    def controls(self):

        controls_logo = load_image('menu/controls.png')
        attack_pause = load_image('menu/attack_pause.png')

        buttons = {
            'arrowkeys': Button('menu/buttons/arrow_keys.png', 'menu/selected_buttons/arrow_keys.png'),
            'wasd': Button('menu/buttons/wasd.png', 'menu/selected_buttons/wasd.png'),
            'back': Button('menu/buttons/back.png', 'menu/selected_buttons/back.png')
        }

        while True:
            self.screen.blit(pygame.transform.scale(load_image('menu/background.png'), self.screen.get_size()), (0, 0))

            self.screen.blit(controls_logo, ((self.screen.get_width() - controls_logo.get_width()) / 2, 120))
            i = 10
            for b in buttons:
                buttons[b].update()
                buttons[b].draw(self.screen, (self.screen.get_width() - buttons[b].width) / 2,
                                self.screen.get_height() / 2 + i)
                i += 120

            self.screen.blit(attack_pause, (self.screen.get_width() - attack_pause.get_width() - 20,
                                            self.screen.get_height() - 45))

            mx, my = pygame.mouse.get_pos()

            if buttons['arrowkeys'].collided((mx, my)):
                if self.click:
                    self.sound_button.play()
                    return 'ARROWKEYS'

            if buttons['wasd'].collided((mx, my)):
                if self.click:
                    self.sound_button.play()
                    return 'WASD'

            if buttons['back'].collided((mx, my)):
                if self.click:
                    self.sound_button.play()
                    return self.control

            self.click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True

            pygame.display.update()


Menu().main()
