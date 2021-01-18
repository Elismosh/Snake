import os
import random
import sys

import pygame

pygame.init()
pygame.display.set_caption('Snake')
pygame.font.init()

FPS = 80


def terminate():
    pygame.quit()
    sys.exit()


# Игровой цикл
def play():
    global pl, lv

    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, int(500 / menu.speed))
    background = load_image('fon_for_play.png')

    while pl:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
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
        if pl:
            screen.blit(background, (2, 2))
            if tile_in_width == 8:
                screen.blit(load_image('grad_8_6.jpg'), (x_shift - 25, y_shift - 25))
            elif tile_in_width == 12:
                screen.blit(load_image('grad_12_9.jpg'), (x_shift - 25, y_shift - 25))

            lv.draw_level()
            apple.draw(screen)
            snake_object.draw()

            font = pygame.font.Font('data/font.ttf', 40)
            string_rendered = font.render('Score:' + str(snake_object.len - 3), True, pygame.Color('#465945'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 0
            intro_rect.x = 2
            screen.blit(string_rendered, intro_rect)

            pygame.display.flip()


# Загрузки изображения
def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# Загрузка меню
def load_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(5, 55) and event.pos[1] in range(2, 52):
                    menu.sound()
                elif event.pos[0] in range(122, 682) and event.pos[1] in range(152, 392):
                    menu.select_level(event.pos[0], event.pos[1])
                elif event.pos[0] in range(125, 281) and event.pos[1] in range(460, 560):
                    menu.select_speed(event.pos[0], event.pos[1])
                elif event.pos[0] in range(380, 486) and event.pos[1] in range(411, 561):
                    menu.select_size(event.pos[0], event.pos[1])
                elif event.pos[0] in range(522, 682) and event.pos[1] in range(444, 531):
                    return
        menu.load_display()
        pygame.display.flip()
        clock.tick(FPS)


# Загрузка начального экрана
def start_screen():
    fon = load_image('start_fon.png')
    fon.get_rect()
    screen.blit(fon, (2, 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


# Загрузка экрана, когда игра проиграна
def game_over():
    global pl
    intro_text = "GAME OVER"
    screen.blit(load_image('fon_for_play.png'), (2, 2))
    font = pygame.font.Font('data/font.ttf', 100)
    string_rendered = font.render(intro_text, True, pygame.Color('#465945'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 200
    intro_rect.x = 195
    screen.blit(string_rendered, intro_rect)

    font = pygame.font.Font('data/font.ttf', 50)
    string_rendered = font.render('Score:' + str(snake_object.len), True, pygame.Color('#465945'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 300
    intro_rect.x = 323
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                pl = False
                return
        pygame.display.flip()
        clock.tick(FPS)


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.add(snake)
        self.len = 3
        # Направление каждой чсати змейки
        self.direction = 2
        # Список для хранения каждой части змейки
        self.list = [[x_shift, y_shift + tile_size * 2, 'head', self.direction],
                     [x_shift, y_shift + tile_size, 'body', self.direction],
                     [x_shift, y_shift, 'tail', self.direction]]

    # Изменение направления головы змейки
    def change_direction(self, dirctn=None):
        if (self.direction + dirctn) % 2 == 1:
            self.direction = dirctn

    # Обновение координат каждой части змейки
    def update(self):
        if self.direction in [0, 2]:
            self.list.insert(0, [self.list[0][0], self.list[0][1] + (self.direction - 1) * tile_size, 'head',
                                 self.direction])
        else:
            self.list.insert(0, [self.list[0][0] + self.direction * tile_size, self.list[0][1], 'head', self.direction])
        self.list[1][2] = 'body'
        if self.list[0][0] == apple_object.rect.x and self.list[0][1] == apple_object.rect.y:
            self.len += 1
            apple_object.update()
        else:
            self.list.pop()
            self.list[-1][2] = 'tail'
            self.list[-1][3] = self.list[-2][3]

        self.image = load_image(self.list[0][2] + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.list[0][0]
        self.rect.y = self.list[0][1]
        if pygame.sprite.spritecollideany(self, borders):
            game_over()

        for elem in self.list:
            if self.list[0][0] == elem[0] and self.list[0][1] == elem[1] and elem != self.list[0]:
                game_over()
            if lv.level_map[(elem[1] - y_shift) // tile_size][(elem[0] - x_shift) // tile_size] == '#':
                game_over()

    # Отрисовка змейки
    def draw(self):
        image = pygame.transform.scale(load_image(self.list[0][2] + '.png'), (tile_size, tile_size))
        angle = (self.list[0][3] + 1) * 90 if self.list[0][3] % 2 == 1 else (3 - self.list[0][3]) * 90
        image = pygame.transform.rotate(image, angle)
        self.rect = image.get_rect()
        self.rect.x, self.rect.y = self.list[0][0] + (tile_size - self.rect.width) // 2, self.list[0][1] + (
                tile_size - self.rect.height) // 2

        for elem in self.list:
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
                    image = pygame.transform.scale(load_image('turn.png'), (tile_size, tile_size))
            image = pygame.transform.rotate(image, angle)
            rect = image.get_rect()
            rect.x, rect.y = elem[0] + (tile_size - rect.width) // 2, elem[1] + (tile_size - rect.height) // 2
            screen.blit(image, rect)

        self.image = load_image(self.list[0][2] + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.list[0][0]

    # Обновляем змейку для нового игрового цикла
    def new_snake(self):
        self.len = 3
        self.direction = 2
        self.list = [[x_shift, y_shift + tile_size * 2, 'head', self.direction],
                     [x_shift, y_shift + tile_size, 'body', self.direction],
                     [x_shift, y_shift, 'tail', self.direction]]


class Border(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(all_sprites)
        self.add(borders)
        self.rect = pygame.Rect(x, y, w, h)

    # Изменение координат, высоты и ширины стенок для нового игрового цикла
    def update(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.add(apple)
        self.image = load_image('apple.png')
        self.update()

    # Изменение положения яблока при съедении его змейкой или для нового игрового цикла
    # Яблоко не должно находиться на одной клетке со змейкой или препятствиями
    def update(self):
        flag = False
        while not flag:
            self.x = random.randrange(tile_in_width)
            self.y = random.randrange(tile_in_height)
            flag = True
            for el in snake_object.list:
                if el[0] == self.x * tile_size + x_shift and el[1] == self.y * tile_size + y_shift \
                        or lv.level_map[self.y][self.x] == '#':
                    flag = False
                if not flag:
                    break
        self.rect = pygame.Rect(self.x * tile_size + x_shift, self.y * tile_size + y_shift, tile_size, tile_size)


class Menu:
    def __init__(self):
        self.list_of_speeds = [0.5, 1, 1.5, 2]
        self.list_of_size = ['Small', 'Medium', 'Large']
        self.speed = 1
        self.size = [16, 12]
        self.level = 0

        # Загружаем звук
        self.music = True
        pygame.mixer.music.load("data/music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

    # Отрисовка всех элементов меню (внутри подробно)
    def load_display(self):
        # Отрисовка фона
        fon = load_image('fon.jpg')
        fon.get_rect()
        screen.blit(fon, (2, 2))

        # Отрисовка уровней
        image = load_image('frame_for_levels.png')
        t_w = 7
        t_h = 3
        font = pygame.font.Font('data/font.ttf', 60)
        num = 1
        for i in range(t_h):
            for j in range(t_w):
                if not (j == 0 and i == 0):
                    frame = image.get_rect()
                    screen.blit(image, ((width - t_w * frame.width) // 2 + frame.width * j,
                                        (height - t_h * frame.height) // 2 - 30 + frame.height * i))
                    num_rendered = font.render(str(num), True, pygame.Color('#465945'))
                    num_rect = num_rendered.get_rect()
                    num_rect.y = (height - t_h * frame.height) // 2 - 21 + frame.height * i
                    num_rect.x = (width - t_w * frame.width) // 2 + (12 if num >= 10 else 26) + frame.width * j
                    screen.blit(num_rendered, num_rect)
                    num += 1
        image = load_image('frame_for_classic_level.png')
        frame = image.get_rect()
        screen.blit(image, ((width - t_w * frame.width) // 2,
                            (height - t_h * frame.height) // 2 - 30))

        # Отрисовка скоростей
        font = pygame.font.Font('data/font.ttf', 60)
        speed_word_rendered = font.render('Speed', True, pygame.Color('#465945'))
        speed_word_rect = speed_word_rendered.get_rect()
        speed_word_rect.y = 400
        speed_word_rect.x = 131
        screen.blit(speed_word_rendered, speed_word_rect)

        image = load_image('frame_for_speed.png')
        font = pygame.font.Font('data/font.ttf', 40)
        n = 0
        for i in range(2):
            for j in range(2):
                frame = image.get_rect()
                screen.blit(image, (125 + j * frame.width, 460 + i * frame.height))
                speed_rendered = font.render(str(self.list_of_speeds[n]), True, pygame.Color('#465945'))
                speed_rect = speed_rendered.get_rect()
                speed_rect.y = 465 + i * 50
                speed_rect.x = (136 if self.list_of_speeds[n] in [0.5, 1.5] else 154) + j * 80
                screen.blit(speed_rendered, speed_rect)
                n += 1

        # Отрисовка размеров
        size_word = ['S', 'i', 'z', 'e']
        font = pygame.font.Font('data/font.ttf', 60)
        for i in range(len(size_word)):
            size_word_rendered = font.render(size_word[i], True, pygame.Color('#465945'))
            size_word_rect = size_word_rendered.get_rect()
            size_word_rect.y = 397 + i * 40
            size_word_rect.x = 340
            screen.blit(size_word_rendered, size_word_rect)
        n = 0
        image = load_image('frame_for_size.png')
        font = pygame.font.Font('data/font.ttf', 30)
        for i in range(3):
            frame = image.get_rect()
            screen.blit(image, (380, 411 + i * frame.height))
            size_rendered = font.render(str(self.list_of_size[n]), True, pygame.Color('#465945'))
            size_rect = size_rendered.get_rect()
            size_rect.y = 420 + i * frame.height
            size_rect.x = 391
            screen.blit(size_rendered, size_rect)
            n += 1

        # Отрисовка кнопки старта
        image = load_image('start_frame.png')
        screen.blit(image, (522, 444))
        font = pygame.font.Font('data/font.ttf', 55)
        start_rendered = font.render('Start', True, pygame.Color('#465945'))
        start_rect = start_rendered.get_rect()
        start_rect.y = 459
        start_rect.x = 538
        screen.blit(start_rendered, start_rect)

        # Отрисовка выбранных элементов
        screen.blit(load_image('selected_frame_for_levels.png'), ((self.level - self.level // 7 * 7) * 80 + 122,
                                                       self.level // 7 * 80 + 152))
        x = 203 if self.speed in [1, 2] else 125
        y = 510 if self.speed in [1.5, 2] else 460
        screen.blit(load_image('selected_frame_for_speed.png'), (x, y))

        if self.size == [8, 6]:
            y = 411
        elif self.size == [12, 9]:
            y = 461
        else:
            y = 511
        screen.blit(load_image('selected_frame_for_size.png'), (380, y))

        # Отрисовка кнопки включения\выключения звука
        screen.blit(load_image('music_on.png') if self.music else load_image('music_off.png'), (5, 2))
        # Отрисовка названия игры
        screen.blit(load_image('title.png'), ((804 - 342) // 2, 10))

    # Изменение звука
    def sound(self):
        self.music = not self.music
        if self.music:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    # Выбор уровня
    def select_level(self, x, y):
        x_tile = (x - 122) // 80
        y_tile = (y - 152) // 80
        self.level = y_tile * 7 + x_tile

    # Выбор скорости
    def select_speed(self, x, y):
        if y in range(460, 510) and x in range(125, 203):
            self.speed = 0.5
        elif y in range(510, 560) and x in range(125, 203):
            self.speed = 1.5
        elif y in range(460, 510) and x in range(203, 281):
            self.speed = 1
        elif y in range(510, 560) and x in range(203, 281):
            self.speed = 2

    # Выбор скорости
    def select_size(self, x, y):
        if y in range(415, 460):
            self.size = [8, 6]
        elif y in range(460, 510):
            self.size = [12, 9]
        elif y in range(510, 560):
            self.size = [16, 12]


class Level:
    def __init__(self, filename):
        filename = "data/levels/" + filename
        # Загруска матрицы уровня
        with open(filename, 'r') as mapFile:
            self.level_map = [line.strip() for line in mapFile]

    # Обновление уровня для нового игрового цикла
    def update(self, filename):
        filename = "data/levels/" + filename
        with open(filename, 'r') as mapFile:
            self.level_map = [line.strip() for line in mapFile]

    # Отрисовка уровня
    def draw_level(self):
        colors = ['#449f35', '#60c44f']
        for i in range(tile_in_height):
            for j in range(tile_in_width):
                if self.level_map[i][j] == '.':
                    pygame.draw.rect(screen, colors[(i + j) % 2],
                                     (x_shift + tile_size * j, y_shift + tile_size * i, tile_size, tile_size), 0)
                elif self.level_map[i][j] == '#':
                    image = load_image('box.png')
                    screen.blit(image, (j * tile_size + x_shift, i * tile_size + y_shift))


tile_size = 50
size = width, height = 16 * tile_size + 4, 12 * tile_size + 4
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
borders = pygame.sprite.Group()
apple = pygame.sprite.Group()
snake = pygame.sprite.Group()
clock = pygame.time.Clock()

start_screen()

# Загрузка меню
menu = Menu()
load_menu()

# Установка размеров поля, отступов. Загрузка уровня
tile_in_width, tile_in_height = menu.size[0], menu.size[1]
x_shift, y_shift = (width - tile_in_width * tile_size) // 2, (height - tile_in_height * tile_size) // 2
lv = Level(str(menu.level) + '.txt')

# Установка стенок, змейки, яоблока
brd1 = Border(x_shift, y_shift - 2, tile_in_width * tile_size, 2)
brd2 = Border(x_shift + tile_in_width * tile_size + 2, y_shift, 2, tile_in_height * tile_size)
brd3 = Border(x_shift, y_shift + tile_in_height * tile_size + 2, tile_in_width * tile_size, 2)
brd4 = Border(x_shift - 2, y_shift, 2, tile_in_height * tile_size)
snake_object = Snake()
apple_object = Apple()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Игровой цикл
    pl = True
    play()
    pygame.draw.rect(screen, pygame.color.Color(0, 0, 0), (0, 0, width, height), 0)
    # Загрузка меню
    load_menu()

    # Установка размеров поля, отступов. Обновление уровня
    tile_in_width, tile_in_height = menu.size[0], menu.size[1]
    x_shift, y_shift = (width - tile_in_width * tile_size) // 2, (height - tile_in_height * tile_size) // 2
    lv.update(str(menu.level) + '.txt')

    # Обновление стенок, змейки, яблока
    brd1.update(x_shift, y_shift - 2, tile_in_width * tile_size, 2)
    brd2.update(x_shift + tile_in_width * tile_size + 2, y_shift, 2, tile_in_height * tile_size)
    brd3.update(x_shift, y_shift + tile_in_height * tile_size + 2, tile_in_width * tile_size, 2)
    brd4.update(x_shift - 2, y_shift, 2, tile_in_height * tile_size)
    snake_object.new_snake()
    apple_object.update()

    pygame.display.flip()
pygame.quit()
