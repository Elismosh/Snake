import os
import random
import sys

import pygame


def load_background():
    color = '#60c44f'
    # for i in range(tile_in_height):
    #     for j in range(tile_in_width):
    #         pygame.draw.rect(screen, colors[(i + j) % 2],
    #                          (tile_size * j + 2, tile_size * i + 2, tile_size, tile_size), 0)
    pygame.draw.rect(screen, color,
                     (0, 0, width, height), 0)


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
        self.list = [[x * tile_size, y * tile_size, 'head', self.direction],
                     [x * tile_size, (y + 1) * tile_size, 'body', self.direction],
                     [x * tile_size, (y + 2) * tile_size, 'tail', self.direction]]
        self.copy = self.list.copy()

    def change_direction(self, dirctn=None):
        if (self.direction + dirctn) % 2 == 1:
            self.direction = dirctn
            self.list[0][3] = self.direction
            # if self.direction in [0, 2]:
            #     shift_x = self.list[0][0] - self.list[0][0] // tile_size * tile_size
            #     shift_y = 0
            #     if shift_x > 25:
            #         shift_x = shift_x - 50
            # else:
            #     shift_y = self.list[0][1] - self.list[0][1] // tile_size * tile_size
            #     shift_x = 0
            #     if shift_y > 25:
            #         shift_y = shift_y - 50
            # for elem in self.list:
            #     elem[0] -= shift_x
            #     elem[1] -= shift_y

    def update(self):
        for i in range(1, len(self.list)):
            self.list[i][3] = self.copy[i - 1][3]
        self.copy = self.list.copy()
        # self.list.insert(0, [self.list[0][0], self.list[0][1], self.list[0][2], self.list[0][3]])
        # self.list[1][2] = 'body'
        # del self.list[-1]
        # self.list[-1][2] = 'tail'
        # for i in range(1, len(self.list)):
        #     self.list[i][0], self.list[i][1] = self.list[i - 1][0], self.list[i - 1][1]
        #
        # for i in range(1, len(self.list)):
        #     self.list[i][3] = self.list[i - 1][3]

        # for i in range(len(self.list)):
        #     if self.direction in [0, 2]:
        #          self.list.insert(i, [self.list[i][0], self.list[i][1] + (self.direction - 1), self.list[i][2],
        #                              self.list[i][3]])
        #     else:
        #         self.list.insert(i, [self.list[i][0] + self.direction, self.list[i][1], self.list[i][2],
        #                              self.list[i][3]])
        #     del self.list[i + 1]

        # if self.direction in [0, 2]:
        #     for i in range(len(self.list)):
        #         self.list.insert(i, [self.list[i][0], self.list[i][1] + (self.direction - 1), self.list[i][2],
        #                              self.list[i][3]])
        #         del self.list[i + 1]
        # else:
        #     for i in range(len(self.list)):
        #         self.list.insert(i,
        #                          [self.list[i][0] + self.direction, self.list[i][1], self.list[i][2], self.list[i][3]])
        #         del self.list[i + 1]
        # self.list[1][2] = 'body'
        # if self.list[0][0] == apple_object.rect.x and self.list[0][1] == apple_object.rect.y:
        #     is_apple = False
        # else:
        #     self.list.pop()
        #     self.list[-1][2] = 'head'

        # print(self.list)
        # if self.direction in [0, 2]:
        #     for elem in self.list:
        #         elem[1] += self.direction - 1
        # else:
        #     for elem in self.list:
        #         elem[0] += self.direction
    def move(self):
        for elem in self.list:
            if elem[3] in [0, 2]:
                elem[1] += elem[3] - 1
            else:
                elem[0] += elem[3]

    # def eat_apple(self):
    #     # Part_of_snake()
    #     # self.len += 1
    #     pass

    def draw(self):
        for elem in self.list:
            image = load_image(elem[2] + str(elem[3]) + '.png')
            rect = image.get_rect()
            rect.x, rect.y = elem[0], elem[1]
            screen.blit(image, rect)


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
snake_object = Snake(9, 9)
apple_object = Apple()
MOVESNAKE = pygame.USEREVENT + 1
UPDATESNAKE = pygame.USEREVENT + 2
time = 10
pygame.time.set_timer(MOVESNAKE, time)
pygame.time.set_timer(UPDATESNAKE, time * tile_size * 2)

running = True
is_apple = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MOVESNAKE:
            snake_object.move()
        if event.type == UPDATESNAKE:
            snake_object.update()
            print('jfks')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                snake_object.change_direction(0)
            elif event.key == pygame.K_a:
                snake_object.change_direction(-1)
            elif event.key == pygame.K_s:
                snake_object.change_direction(2)
            elif event.key == pygame.K_d:
                snake_object.change_direction(1)
    load_background()
    if not is_apple:
        apple_object = Apple()
        is_apple = True
    apple.draw(screen)
    # snake.draw(screen)
    snake_object.draw()
    pygame.display.flip()
pygame.quit()
