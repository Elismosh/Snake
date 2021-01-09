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
    image = pygame.transform.scale(pygame.image.load(fullname), (tile_size, tile_size))
    return image


class Snake(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(snake)
        self.len = 3
        self.direction = 0
        self.list = [[x * tile_size, y * tile_size, 'head', self.direction], [x * tile_size, (y + 1) * tile_size, 'body', self.direction],
                     [x * tile_size, (y + 2) * tile_size, 'tail', self.direction]]

    def change_direction(self, dirctn=None):
        if (self.direction + dirctn) % 2 == 1:
            self.direction = dirctn

    def update(self):
        if self.direction in [0, 2]:
            self.list.insert(0, [self.list[0][0], self.list[0][1] + (self.direction - 1) * tile_size, 'head', self.direction])
        else:
            self.list.insert(0, [self.list[0][0] + self.direction * tile_size, self.list[0][1], 'head', self.direction])
        self.list[1][2] = 'body'
        if self.list[0][0] == apple_object.rect.x and self.list[0][1] == apple_object.rect.y:
            is_apple = False
        else:
            self.list.pop()
            self.list[-1][2] = 'tail'

    # def eat_apple(self):
    #     # Part_of_snake()
    #     # self.len += 1
    #     pass

    def draw(self):
        for elem in self.list:
            image = load_image(elem[2] + str(elem[3]) + '.png')
            rect = image.get_rect()
            rect.x, rect.y = elem[0] + (tile_size - rect.width) // 2, elem[1] + (tile_size - rect.height) // 2
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
MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 500)

running = True
is_apple = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MYEVENTTYPE:
            pass
            snake_object.update()
            # parts.update(3)
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