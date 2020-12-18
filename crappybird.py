import pygame
import random
import os

WIDTH = 1920
HEIGHT = 1080
FPS = 60


PIPE_WIDTH = 100
PIPE_HEIGHT = 1080
GAP = 250

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TRANSPARENT = 0


# init
#create window and init pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()



# game loop
running = True
waiting = True
score = 0
high_score = 0

ROOT_FOLDER = os.path.dirname(__file__)
IMG_FOLDER = os.path.join(ROOT_FOLDER, "img")
font_name = pygame.font.match_font('arial')

print(IMG_FOLDER)

def menu_screen():
    global waiting
    global running
    while waiting:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                running = False
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            waiting = False

        # Update
        background_sprites.update()
        # Render
        screen.fill((0,0,0))
        all_sprites.draw(screen)
        draw_text(screen, "Press SPACE to start", 50, WIDTH/2, HEIGHT/2)
        draw_text(screen, str(high_score), 60, 30, 30)
        draw_text(screen, str(int(clock.get_fps())) + "FPS", 30, 60, HEIGHT - 50)
        draw_text(screen, "By Weichen Tie", 20, WIDTH - 100, HEIGHT - 40)
        pygame.display.flip()


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.orig_img = pygame.image.load(os.path.join(IMG_FOLDER,"bird.png")).convert()
        self.image = self.orig_img
        self.image.set_colorkey(RED)
        self.rect = self.image.get_rect()
        self.rect.center = ((WIDTH/6, HEIGHT/2))
        self.velocity = 0
        self.rot = 0
        self.space_pressed = False

    def update(self):
        self.rotate_cw()
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE] and not self.space_pressed:
            self.velocity = -17
            self.space_pressed = True
            self.rot = 60
        elif not keystate[pygame.K_SPACE]:
            self.space_pressed = False
        self.rect.y += self.velocity
        self.velocity += 1

        global waiting
        if pygame.sprite.spritecollide(player, pipes, False):
            waiting = True
        if self.rect.y > HEIGHT:
            waiting = True
    def rotate_cw(self):
        new_image = pygame.transform.rotate(self.orig_img, (self.rot % 360))
        old_center = self.rect.center
        self.image = new_image
        self.image.set_colorkey(RED)
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.rot -= 2.5


class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(IMG_FOLDER,"background.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.center = ((WIDTH/2, HEIGHT/2))
    def update(self):
        self.rect.x -= 1
        if self.rect.right == WIDTH:
            self.rect.left = 0

class UpperPipe(pygame.sprite.Sprite):
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(IMG_FOLDER,"upper_pipe.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = ((WIDTH, y))
    def update(self):
        self.rect.x -= 5
        if self.rect.right == WIDTH/2:
            del self

class LowerPipe(pygame.sprite.Sprite):
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(IMG_FOLDER,"lower_pipe.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = ((WIDTH, y + GAP))
    def update(self):
        self.rect.x -= 5

class ScoreRegion(pygame.sprite.Sprite):
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PIPE_WIDTH/4, GAP))
        self.image.set_alpha(TRANSPARENT)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = ((WIDTH + PIPE_WIDTH * 3/4, y + GAP))

    def update(self):
        self.rect.x -= 5

all_sprites = pygame.sprite.Group()

background = Background()
background_sprites = pygame.sprite.Group()
background_sprites.add(background)
all_sprites.add(background)

player = Player()
all_sprites.add(player)

pipes = pygame.sprite.Group()
scoring_hitbox = pygame.sprite.Group()
cycle = 0

while running:
    clock.tick(FPS)
    # Events
    if waiting is True:
        all_sprites = pygame.sprite.Group()

        background = Background()
        background_sprites = pygame.sprite.Group()
        background_sprites.add(background)
        all_sprites.add(background)

        player = Player()
        all_sprites.add(player)

        pipes = pygame.sprite.Group()
        scoring_hitbox = pygame.sprite.Group()
        cycle = 0

        if score > high_score:
            high_score = score
        score = 0

        menu_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Update
    if not cycle % 100:
        num = random.randrange(200,600)
        
        upper_pipe = UpperPipe(num)
        lower_pipe = LowerPipe(num)
        
        pipes.add(lower_pipe)
        pipes.add(upper_pipe)

        score_region = ScoreRegion(num)
        scoring_hitbox.add(score_region)

        all_sprites.add(upper_pipe)
        all_sprites.add(lower_pipe)
        all_sprites.add(score_region)
    
    if pygame.sprite.spritecollide(player, scoring_hitbox, True):
        score += 1

    all_sprites.update()

    # Render
    screen.fill((0,0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 100, WIDTH/2, HEIGHT/8)
    draw_text(screen, str(high_score), 60, 30, 30)
    draw_text(screen, str(int(clock.get_fps())) + "FPS", 30, 60, HEIGHT - 50)
    draw_text(screen, "By Weichen Tie", 20, WIDTH - 100, HEIGHT - 40)
    pygame.display.flip()
    cycle += 1
pygame.quit()

# end