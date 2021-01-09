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


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Snake(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(snake)
        self.len = 3
        self.direction = 0
        self.list = [[x, y, 'head', self.direction, [-1, -1]], [x, y + tile_size, 'body', self.direction],
                     [x, y + tile_size * 2, 'body', self.direction]]
        for elem in self.list:
            Part_of_snake(elem[0], elem[1], elem[2], elem[3])

    def moving(self):
        parts.update()
        # for i in range(self.len):

            # if self.list[i][3] % 2 == 1:
            #     self.list[i][0] += self.list[i][3]
            # else:
            #     self.list[i][1] += self.list[i][3]

        # if pygame.sprite.spritecollideany(self, borders):
        #     pass
        # if pygame.sprite.spritecollideany(self, apple):
        #     pass

    def change_direction(self, dirctn=None):
        if dirctn:
            self.list[0][3] = dirctn
            if dirctn in [0, 2]:
                if self.list[0][0] - self.list[0][0] // tile_size * tile_size < 25:
                    self.list[0][0] = self.list[0][0] // tile_size * tile_size
                    for i in range(1, self.len):
                        self.list[i][0] += self.list[0][0] - self.list[0][0] // tile_size * tile_size
                else:
                    self.list[0][0] = (self.list[0][0] // tile_size + 1) * tile_size
                    for i in range(1, self.len):
                        self.list[i][0] -= self.list[0][0] - self.list[0][0] // tile_size * tile_size
            else:
                if self.list[0][1] - self.list[0][1] // tile_size * tile_size < 25:
                    self.list[0][1] = self.list[0][1] // tile_size * tile_size
                    for i in range(1, self.len):
                        self.list[i][1] += self.list[0][1] - self.list[0][1] // tile_size * tile_size
                else:
                    self.list[0][1] = (self.list[0][1] // tile_size + 1) * tile_size
                    for i in range(1, self.len):
                        self.list[i][1] -= self.list[0][1] - self.list[0][1] // tile_size * tile_size
            self.list[0][4] = [self.list[0][0], self.list[0][1]]
        dir = self.list[0][3] % 2
        x_chng_dir = self.list[0][4][0]
        y_chng_dir = self.list[0][4][0]
        for i in range(1, self.len):
            if self.list[i][3] != dir and self.list[i][0] == x_chng_dir and self.list[i][1] == y_chng_dir:
                self.list[i][3] = dir


    # def update(self, num):
    #     # if num == 10:
    #     #     self.moving()
    #     # else:
    #     #     self.change_direction(num)
    #     for elem in self.list:
    #         elem.image = load_image(elem[2] + str(elem[3]) + '.png')
    #         elem.rect = pygame.Rect(elem[0], elem[1], tile_size, tile_size)
    #         elem.draw(screen)
    def eat_apple(self):
        # Part_of_snake()
        # self.len += 1
        pass

    def draw(self):
        pass


class Part_of_snake(pygame.sprite.Sprite):
    def __init__(self, x, y, name, direct):
        super().__init__(all_sprites)
        self.add(parts)
        self.name = name
        self.direction = direct
        self.image = load_image(self.name + str(self.direction) + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, n):
        if n == 1:
            self.move()
        else:
            self.chng_dir(n)

    def move(self):
        if self.direction % 2 == 1:
            self.rect.x += self.direction
        else:
            self.rect.y += self.direction - 1

    def chng_dir(self, dir):
        self.direction = dir
        self.image = load_image(self.name + str(self.direction) + '.png')


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
parts = pygame.sprite.Group()

tile_in_height, tile_in_width = 12, 16
tile_size = 50
size = width, height = tile_in_width * tile_size + 4, tile_in_height * tile_size + 4
screen = pygame.display.set_mode(size)

Border(0, 0, width, 2)
Border(width - 2, 0, 2, height)
Border(0, height - 2, width, 2)
Border(0, 0, 2, height)
snake_object = Snake(450, 450)
MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 10)

running = True
is_apple = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MYEVENTTYPE:
            # snake_object.moving()
            parts.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                snake.update(0)
            elif event.key == pygame.K_a:
                snake.update(-1)
            elif event.key == pygame.K_s:
                snake.update(2)
            elif event.key == pygame.K_d:
                snake.update(1)
    load_background()
    if not is_apple:
        Apple()
        is_apple = True
    apple.draw(screen)
    # snake.draw(screen)
    parts.draw(screen)
    pygame.display.flip()
pygame.quit()
