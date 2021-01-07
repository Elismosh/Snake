import os
import random
import sys

import pygame


def load_background():
    colors = ['#449f35', '#60c44f']
    for i in range(tile_in_height):
        for j in range(tile_in_width):
            pygame.draw.rect(screen, colors[(i + j) % 2],
                             (tile_size * j + 2, tile_size * i + 2, tile_size, tile_size), 0)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Snake(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__(all_sprites)
        self.add(snake)
        self.len = 0
        self.direction = 0
        self.name = name
        self.image = load_image(self.name + str(self.direction) + '.png')
        self.x = -1
        self.y = -1
        # if head:
        #     self.x = x
        #     self.y = y
        # else:
        #     self.x = -1
        #     self.y = -1
        self.rect = pygame.Rect(self.x * tile_size + 2, self.y * tile_size + 2, tile_size, tile_size)
        self.mask = pygame.mask.from_surface(self.image)

    def moving(self):
        if self.direction % 2 == 1:
            self.rect = self.rect.move(self.direction, 0)
        else:
            self.rect = self.rect.move(0, self.direction - 1)
        if self.rect.x == head.x and self.rect.y == head.y:
            self.change_direction(head.direction)
        if pygame.sprite.spritecollideany(self, borders):
            pass
        if pygame.sprite.spritecollideany(self, apple):
            pass

    def change_direction(self, dirctn):
        if self == head:
            self.x = self.rect.x
            self.y = self.rect.y
        if self.rect.x == head.x and self.rect.y == head.y:
            if (self.direction + dirctn) % 2 == 1:
                self.direction = dirctn
                if self.direction in [0, 2]:
                    if self.rect.x - self.rect.x // tile_size * tile_size < 25:
                        self.rect.x = self.rect.x // tile_size * tile_size
                    else:
                        self.rect.x = (self.rect.x // tile_size + 1) * tile_size
                else:
                    if self.rect.y - self.rect.y // tile_size * tile_size < 25:
                        self.rect.y = self.rect.y // tile_size * tile_size
                    else:
                        self.rect.y = (self.rect.y // tile_size + 1) * tile_size
                self.image = load_image(self.name + str(self.direction) + '.png')
                self.mask = pygame.mask.from_surface(self.image)

    def update(self, num):
        if num == 10:
            self.moving()
        else:
            self.change_direction(num)


class Border(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(all_sprites)
        self.add(borders)
        # self.image = pygame.Surface([x2 - x1, 1])
        self.rect = pygame.Rect(x, y, w, h)


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.add(apple)
        self.x = random.randrange(tile_in_width)
        self.y = random.randrange(tile_in_height)
        if self.x == 9 and self.y in range(5, 8):
            self.x = 8
        self.image = load_image('apple.png')
        self.rect = pygame.Rect(self.x * tile_size + 2, self.y * tile_size + 2, tile_size, tile_size)


all_sprites = pygame.sprite.Group()
borders = pygame.sprite.Group()
apple = pygame.sprite.Group()
snake = pygame.sprite.Group()

tile_in_height, tile_in_width = 12, 16
tile_size = 50
size = width, height = tile_in_width * tile_size + 4, tile_in_height * tile_size + 4
screen = pygame.display.set_mode(size)

Border(0, 0, width, 2)
Border(width - 2, 0, 2, height)
Border(0, height - 2, width, 2)
Border(0, 0, 2, height)
head = Snake(9, 9, 'head')
Snake(9, 10, 'body')
Snake(9, 11, 'body')

MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 10)

running = True
is_apple = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MYEVENTTYPE:
            snake.update(10)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                head.update(0)
            elif event.key == pygame.K_a:
                head.update(-1)
            elif event.key == pygame.K_s:
                head.update(2)
            elif event.key == pygame.K_d:
                head.update(1)
    load_background()
    if not is_apple:
        Apple()
        is_apple = True
    apple.draw(screen)
    snake.draw(screen)
    pygame.display.flip()
pygame.quit()
