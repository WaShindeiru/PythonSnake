import pygame
import sys
from random import randint

RES = W_SIZE, H_SIZE = 64, 64
MATRIX = WIDTH, HEIGHT = 16, 16
INTERVAL = 200


class SnakeGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def erase(self):
        if self.sprites():
            self.sprites()[0].kill()

    def collide(self, sprite):
        return pygame.sprite.spritecollide(sprite, self, dokill=False)


class Block(pygame.sprite.Sprite):
    def __init__(self, col, x, y):
        super().__init__()
        self.image = pygame.Surface((W_SIZE, H_SIZE))
        self.image.fill(col)
        self.rect = self.image.get_rect(topleft=(x*W_SIZE, y*H_SIZE))


class Fruit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((W_SIZE, H_SIZE))
        self.image.fill((200, 10, 20))
        self.rect = self.image.get_rect(topleft=(x*W_SIZE, y*H_SIZE))


class Snake:
    def __init__(self, x, y, app):
        self.body = SnakeGroup()
        self.head = pygame.sprite.GroupSingle()
        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.x = x
        self.y = y
        self.food = 0

        self.delay = INTERVAL
        self.key = [pygame.K_RIGHT]

        self.head.add(Block(self.colour, self.x, self.y))

    def draw(self, screen):
        self.body.draw(screen)
        self.head.draw(screen)

    def move(self, key):
        if key == pygame.K_RIGHT:
            self.x += 1
        elif key == pygame.K_LEFT:
            self.x -= 1
        elif key == pygame.K_UP:
            self.y -= 1
        elif key == pygame.K_DOWN:
            self.y += 1

        if self.x < 0:
            self.x = WIDTH - 1
        elif self.x >= WIDTH:
            self.x = 0
        elif self.y < 0:
            self.y = HEIGHT - 1
        elif self.y >= HEIGHT:
            self.y = 0

        self.body.add(self.head.sprite)
        self.head.add(Block(self.colour, self.x, self.y))

    def update(self):
        if pygame.time.get_ticks() > self.delay:
            self.delay += INTERVAL
            if self.key:
                self.key2 = self.key.pop(0)
            self.move(self.key2)

        if self.body.collide(self.head.sprite):
            return False
        return True

    def check(self, fruit):
        if pygame.sprite.groupcollide(self.body, fruit, dokilla=False, dokillb=False) or pygame.sprite.groupcollide(self.head, fruit, dokilla=False, dokillb=False):
            fruit.sprite.kill()
            fruit.add(Fruit(randint(0, 15), randint(0, 15)))
            self.eat()

        if len(self.body.sprites()) > self.food:
            self.body.erase()

        return self.food + 1

    def eat(self):
        self.food += 1

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((W_SIZE*WIDTH, H_SIZE*HEIGHT))
        self.clock = pygame.time.Clock()
        self.game = True
        self.alive = True
        self.score = 0

        self.snake = Snake(1, 1, self)
        self.fruit = pygame.sprite.GroupSingle(Fruit(randint(0, 15), randint(0, 15)))

    def Event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game = False

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    self.snake.key.append(event.key)

    def update(self):
        self.alive = self.snake.update()
        self.score = self.snake.check(self.fruit)

    def draw(self):
        self.screen.fill((10, 205, 60))
        for x in range(WIDTH):
            for y in range(HEIGHT):
                pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(x*W_SIZE, y*H_SIZE, W_SIZE, H_SIZE), 1)

        self.snake.draw(self.screen)
        self.fruit.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while(self.game and self.alive):
            self.Event()
            self.update()
            self.draw()

            self.clock.tick(60)

        delay = pygame.time.get_ticks()
        if not self.alive:
            print("You lost")
            while(pygame.time.get_ticks() < delay + 2000):
                pass

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.run()
