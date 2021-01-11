import os
import random
import sys

import pygame

pygame.init()
pygame.font.init()

FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


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
    image = pygame.transform.scale(pygame.image.load(fullname), (tile_size, tile_size))
    return image


class Snake(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(snake)
        self.len = 3
        self.direction = 0
        self.list = [[x * tile_size + 2, y * tile_size + 2, 'head', self.direction],
                     [x * tile_size + 2, (y + 1) * tile_size + 2, 'body', self.direction],
                     [x * tile_size + 2, (y + 2) * tile_size + 2, 'tail', self.direction]]
        self.copy = self.list.copy()

    def change_direction(self, dirctn=None):
        if (self.direction + dirctn) % 2 == 1:
            self.direction = dirctn

    def update(self):
        if self.direction in [0, 2]:
            self.list.insert(0, [self.list[0][0], self.list[0][1] + (self.direction - 1) * tile_size, 'head',
                                 self.direction])
        else:
            self.list.insert(0, [self.list[0][0] + self.direction * tile_size, self.list[0][1], 'head', self.direction])
        self.list[1][2] = 'body'
        if self.list[0][0] == apple_object.rect.x and self.list[0][1] == apple_object.rect.y:
            apple_object.update()
        else:
            self.list.pop()
            self.list[-1][2] = 'tail'
        self.copy = self.list.copy()

    def move(self):
        for elem in self.list:
            pass

    # def eat_apple(self):
    #     # Part_of_snake()
    #     # self.len += 1
    #     pass

    def draw(self):
        for elem in self.list:
            image = pygame.transform.scale(load_image(elem[2] + str(elem[3]) + '.png'), (tile_size, tile_size))
            rect = image.get_rect()
            rect.x, rect.y = elem[0] + (tile_size - rect.width) // 2, elem[1] + (tile_size - rect.height) // 2
            screen.blit(image, rect)
        self.image = load_image(self.list[0][2] + str(self.list[0][3]) + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.list[0][0]
        self.rect.y = self.list[0][1]
        # self.mask = pygame.mask.from_surface(self.image)
        # if pygame.sprite.collide_mask(self, upper_wall) or pygame.sprite.collide_mask(self, right_wall) or\
        #    pygame.sprite.collide_mask(self, left_wall) or pygame.sprite.collide_mask(self, bottom_wall):
        #     pass
        if pygame.sprite.spritecollideany(self, borders):
            pass


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
        self.image = load_image('apple.png')
        self.update()

    def update(self):
        flag = False
        while not flag:
            self.x = random.randrange(tile_in_width)
            self.y = random.randrange(tile_in_height)
            flag = True
            for el in snake_object.list:
                if el[0] == self.x * tile_size + 2 and el[1] == self.y * tile_size + 2:
                    flag = False
                if not flag:
                    break
        self.rect = pygame.Rect(self.x * tile_size + 2, self.y * tile_size + 2, tile_size, tile_size)


all_sprites = pygame.sprite.Group()
borders = pygame.sprite.Group()
apple = pygame.sprite.Group()
snake = pygame.sprite.Group()
parts = pygame.sprite.Group()
clock = pygame.time.Clock()

tile_in_height, tile_in_width = 6, 6
tile_size = 50
size = width, height = tile_in_width * tile_size + 4, tile_in_height * tile_size + 4
screen = pygame.display.set_mode(size)

upper_wall = Border(0, 0, width, 2)
right_wall = Border(width - 2, 0, 2, height)
bottom_wall = Border(0, height - 2, width, 2)
left_wall = Border(0, 0, 2, height)
snake_object = Snake(random.randrange(2, tile_in_width), random.randrange(2, tile_in_height - 2))
apple_object = Apple()

MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 500)

start_screen()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MYEVENTTYPE:
            snake_object.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                snake_object.change_direction(0)
            elif event.key == pygame.K_a:
                snake_object.change_direction(-1)
            elif event.key == pygame.K_s:
                snake_object.change_direction(2)
            elif event.key == pygame.K_d:
                snake_object.change_direction(1)
    screen.fill('black')
    load_background()
    apple.draw(screen)
    snake_object.draw()
    pygame.display.flip()
pygame.quit()
