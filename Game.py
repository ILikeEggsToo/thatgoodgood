import pygame
from pygame.locals import *
from os.path import sys

#initialize Pygame and set up the screen
pygame.init()
vec = pygame.math.Vector2

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

displaySurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 100))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.jumping = False

    def move(self):
        self.acc = vec(0, 0.5)
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_d]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos


    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False
        else:
            if hits:
                self.vel.y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center = (x, y))

class Text():
    def __init__(self, font, text, x, y):
        self.surf = font.render(text, 1, (255,255,255))
        self.rect = self.surf.get_rect(center=(x,y))


PT1 = Platform(100, 400, 200, 40)
P1 = Player()

PT2 = Platform(200, 200, 200, 40)

platforms = pygame.sprite.Group()
platforms.add(PT1)
platforms.add(PT2)

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(PT2)
all_sprites.add(P1)

# info text
font = pygame.font.Font(None, 24)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()

    displaySurface.fill((0, 0, 0))

    # draw text
    infoText = f"""
    Pos: {P1.pos.x:.3f}, {P1.pos.y:.3f}
    Vel: {P1.vel.x:.3f}, {P1.vel.y:.3f}
    Acc: {P1.acc.x:.3f}, {P1.acc.y:.3f}"""
    for index, line in enumerate(infoText.splitlines()):
        info = Text(font, line, 300, 32 * index)
        displaySurface.blit(info.surf, info.rect)

    P1.move()
    P1.update()

    for entity in all_sprites:
        displaySurface.blit(entity.surf, entity.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)