import os
import pygame

BASE_IMG_PATH = 'data/images/'


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(f'{path}/{img_name}'))
    return images


def load_spritesheet(path, rows, columns):
    spritesheet = load_image(path)
    width = spritesheet.get_width() / columns
    height = spritesheet.get_height() / rows
    images = []
    for i in range(rows):
        for j in range(columns):
            img = spritesheet.subsurface((j*width, i*height), (width, height))
            images.append(img)
    return images


def load_tileset(path, rows, columns):
    tiles = load_spritesheet(f'{path}/tileset.png', rows, columns)
    decor = load_images(f'{path}/decor')
    return tiles + decor


def transition(screen, display, txt, font, pos, level=-1):
    if level == 2:
        transition(screen, display, 'DOUBLE JUMP UNLOCKED', font, (pos[0] - 45, pos[1]))

    elif level == 3:
        transition(screen, display, 'BOSS FIGHT', font, (pos[0] - 15, pos[1]))
        return

    for i in range(600):
        display.fill((0, 0, 0))
        display.blit(font.render(txt, True, (255, 255, 255)), pos)
        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        pygame.display.update()


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]


class Button:
    def __init__(self, path):
        self.x = 0
        self.y = 0

        self.img_1 = load_image(f'{path}/unselected.png')
        self.img_2 = load_image(f'{path}/selected.png')
        self.curr_image = self.img_1

        self.width = self.curr_image.get_width()
        self.height = self.curr_image.get_height()

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        mx, my = pygame.mouse.get_pos()

        if self.collided((mx, my)):
            self.curr_image = self.img_2
        else:
            self.curr_image = self.img_1

    def draw(self, screen, x=0, y=0):
        self.x = x
        self.y = y

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        screen.blit(self.curr_image, self.rect)

    def collided(self, mouse):
        return self.rect.collidepoint(mouse)
