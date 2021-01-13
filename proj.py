import os
import random
import sys

import pygame

pygame.init()
pygame.font.init()

FPS = 1
tile_size = 50
font = pygame.font.Font('data/font.ttf', 30)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    # fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    fon = load_image('fon.jpg')
    im = fon.get_rect()
    print(im.height, im.width)
    screen.blit(fon, (2, 2))
    font = pygame.font.Font('data/font.ttf', 50)
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


def game_over():
    intro_text = "GAME OVER"

    # fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    # fon = load_image('fon.jpg', tile_size * width, tile_size * height)
    # im = fon.get_rect()
    # screen.blit(fon, (2, 2))
    # color = pygame.color.Color(255, 255, 255).set_a
    # pygame.draw.rect(screen, pygame.color.Color(255, 255, 255, 50), (2, 2, width - 4, height - 4), 0)
    font = pygame.font.Font('data/font.ttf', 100)
    string_rendered = font.render(intro_text, True, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 250
    intro_rect.x = 200
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(200)


def load_background():
    # colors = ['#2bb52b', '#43d143']
    colors = ['#449f35', '#60c44f']
    for i in range(tile_in_height):
        for j in range(tile_in_width):
            pygame.draw.rect(screen, colors[(i + j) % 2],
                             (tile_size * j + 2, tile_size * i + 2, tile_size, tile_size), 0)
    # colors = ['#449f35', '#60c44f']
    # for i in range(12):
    #     for j in range(16):
    #         pygame.draw.rect(screen, colors[(i + j) % 2],
    #                          (tile_size * j + 2, tile_size * i + 2, tile_size, tile_size), 0)
    # colors = ['#fbec5d', '#f7e32a']
    # for i in range(9):
    #     for j in range(12):
    #         pygame.draw.rect(screen, colors[(i + j) % 2],
    #                          (tile_size * j + 2, tile_size * i + 2, tile_size, tile_size), 0)
    # colors = ['#f78fa7', '#f56284']
    # for i in range(6):
    #     for j in range(8):
    #         pygame.draw.rect(screen, colors[(i + j) % 2],
    #                          (tile_size * j + 2, tile_size * i + 2, tile_size, tile_size), 0)


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    # image = pygame.transform.scale(pygame.image.load(fullname), (800, 600))
    image = pygame.image.load(fullname)
    return image


def load_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        menu.load_display()
        pygame.display.flip()
        clock.tick(FPS)


class Menu:
    def __init__(self):
        self.speeds = [0.5, 1, 1.5, 2]
        self.size = {'Small': [6, 8], 'Medium': [9, 12], 'Large': [12, 16]}

    def load_display(self):
        fon = load_image('fon.jpg')
        fon.get_rect()
        screen.blit(fon, (2, 2))

        options_button = load_image('options.png')
        options_button.get_rect()
        screen.blit(options_button, (4, 4))

        # font = pygame.font.Font('data/font.ttf', 30)
        # string_rendered = font.render(line, True, pygame.Color('black'))
        # intro_rect = string_rendered.get_rect()
        # intro_rect.y = 10
        # intro_rect.x = 10
        # screen.blit(string_rendered, intro_rect)

        # while True:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             terminate()
        #         elif event.type == pygame.KEYDOWN or \
        #                 event.type == pygame.MOUSEBUTTONDOWN:
        #             return  # начинаем игру
        #     pygame.display.flip()
        #     clock.tick(FPS)

    def is_options(self):
        pass

    def browsing(self):
        pass

    def select_speed(self):
        pass

    def select_size(self):
        pass


class Snake(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(snake)
        self.len = 3
        self.direction = 0
        self.list = [[x * tile_size + 2, y * tile_size + 2, 'head', self.direction],
                     [x * tile_size + 2, (y + 1) * tile_size + 2, 'body', self.direction],
                     # [x * tile_size + 2, (y + 2) * tile_size + 2, 'body', self.direction],
                     # [x * tile_size + 2, (y + 3) * tile_size + 2, 'body', self.direction],
                     # [x * tile_size + 2, (y + 4) * tile_size + 2, 'body', self.direction],
                     # [x * tile_size + 2, (y + 5) * tile_size + 2, 'body', self.direction],
                     # [x * tile_size + 2, (y + 6) * tile_size + 2, 'body', self.direction],
                     # [x * tile_size + 2, (y + 7) * tile_size + 2, 'body', self.direction],
                     # [x * tile_size + 2, (y + 8) * tile_size + 2, 'body', self.direction],
                     # [x * tile_size + 2, (y + 9) * tile_size + 2, 'body', self.direction],
                     # [x * tile_size + 2, (y + 10) * tile_size + 2, 'body', self.direction],
                     # [x * tile_size + 2, (y + 11) * tile_size + 2, 'body', self.direction],
                     # [x * tile_size + 2, (y + 12) * tile_size + 2, 'body', self.direction],
                     # [x * tile_size + 2, (y + 13) * tile_size + 2, 'body', self.direction],
                     # [x * tile_size + 2, (y + 14) * tile_size + 2, 'body', self.direction],
                     # [x * tile_size + 2, (y + 15) * tile_size + 2, 'body', self.direction],
                     # [x * tile_size + 2, (y + 16) * tile_size + 2, 'body', self.direction],
                     [x * tile_size + 2, (y + 2) * tile_size + 2, 'tail', self.direction]]

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
            self.list[-1][3] = self.list[-2][3]
        if pygame.sprite.spritecollideany(self, borders):
            game_over()

    def draw(self):
        for elem in self.list:
            if self.list[0][0] == elem[0] and self.list[0][1] == elem[1] and elem != self.list[0]:
                game_over()

            image = pygame.transform.scale(load_image(elem[2] + '.png'), (tile_size, tile_size))
            angle = (elem[3] + 1) * 90 if elem[3] % 2 == 1 else (3 - elem[3]) * 90
            if self.list.index(elem) != 0:
                if elem[3] != self.list[self.list.index(elem) - 1][3]:
                    if elem[3] == 0 and self.list[self.list.index(elem) - 1][3] == 1 or \
                            elem[3] == -1 and self.list[self.list.index(elem) - 1][3] == 2:
                        angle = 0
                    elif elem[3] == -1 and self.list[self.list.index(elem) - 1][3] == 0 or \
                            elem[3] == 2 and self.list[self.list.index(elem) - 1][3] == 1:
                        angle = 90
                    elif elem[3] == 2 and self.list[self.list.index(elem) - 1][3] == -1 or \
                            elem[3] == 1 and self.list[self.list.index(elem) - 1][3] == 0:
                        angle = 180
                    elif elem[3] == 1 and self.list[self.list.index(elem) - 1][3] == 2 or \
                            elem[3] == 0 and self.list[self.list.index(elem) - 1][3] == -1:
                        angle = 270
                    else:
                        print('error')
                    image = pygame.transform.scale(load_image('turn.png'), (tile_size, tile_size))
            image = pygame.transform.rotate(image, angle)
            rect = image.get_rect()
            rect.x, rect.y = elem[0] + (tile_size - rect.width) // 2, elem[1] + (tile_size - rect.height) // 2
            screen.blit(image, rect)
        self.image = load_image(self.list[0][2] + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.list[0][0]
        self.rect.y = self.list[0][1]


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

tile_in_height, tile_in_width = 12, 16
# tile_size = 50
size = width, height = tile_in_width * tile_size + 4, tile_in_height * tile_size + 4
screen = pygame.display.set_mode(size)

Border(0, 0, width, 2)
Border(width - 2, 0, 2, height)
Border(0, height - 2, width, 2)
Border(0, 0, 2, height)
snake_object = Snake(random.randrange(2, tile_in_width), random.randrange(2, tile_in_height - 2))
apple_object = Apple()
menu = Menu()

MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 500)

start_screen()
load_menu()
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
