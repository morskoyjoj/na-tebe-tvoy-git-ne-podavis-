from pygame import *
from random import randint

font.init()




window = display.set_mode((1920,1080))
display.set_caption("aphex twin versus metaL")

pic = image.load("back.jpg")
picture = transform.scale(image.load("back.jpg"),(1920,1080))


RED = (201,32,32)
GREEN = (0,233,50)
YELLOW = (255,255,0)
DARK_BLUE = (0,0,100)
BLUE = (80,70,255)
back = (DARK_BLUE)
window.fill(back)


class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = Rect(x, y, width, height)
        self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        draw.rect(window, self.fill_color, self.rect)

    def outline(self, frame_color, thickness):
        draw.rect(window, frame_color, self.rect, thickness)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)


class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = font.SysFont('Comic Sans MS', 50).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    def update(self):
        chekoty = aphex.rect.y <= win_width - 80 and aphex.y_speed > 0 or aphex.rect.y >= 0 > aphex.y_speed
        chekotx = aphex.rect.x <= win_width - 80 and aphex.x_speed > 0 or aphex.rect.x >= 0 > aphex.x_speed

        if chekotx and chekoty:

            platforms_touchd = sprite.spritecollide(self, barriers, False)
            self.rect.x += self.x_speed
            if self.x_speed > 0:
                for p in platforms_touchd:
                    self.rect.right = min(self.rect.right, p.rect.left)
            elif self.x_speed < 0:
                for p in platforms_touchd:
                    self.rect.left = max(self.rect.left, p.rect.right)

            self.rect.y += self.y_speed
            if self.y_speed > 0:
                for p in platforms_touchd:
                    self.rect.bottom = min(self.rect.bottom, p.rect.top)
            elif self.y_speed < 0:
                for p in platforms_touchd:
                    self.rect.top = max(self.rect.top, p.rect.bottom)
#razmer player


class Enemy(GameSprite):
    def __init__(self, enemy_image, enemy_x, enemy_y, size_x, size_y, speed):
        GameSprite.__init__(self, enemy_image, enemy_x, enemy_y, size_x, size_y)
        self.speed = speed
        self.direction = 'left'
    def update(self):
        if self.rect.x > 400:
            self.direction = 'right'
        elif self.rect.x < 300:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
class Bullet(GameSprite):
    def __init__(self, bullet_image, bullet_x, bullet_y, size_x, size_y, speed):
        GameSprite.__init__(self, bullet_image, bullet_x, bullet_y, size_x, size_y)
        self.speed = speed
    def update(self):
        self.speed = self.speed
        self.rect.x += self.speed
        if self.rect.x > win_width+10:
            self.kill()

a = Enemy('enemy.jpg', 5, 100, 80, 80, 5)
monster = sprite.Group()

pew = Bullet('pew.jpg', 115, 115, 115, 115, 115)
pewsprite = sprite.Group()

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
back = (119, 210, 223)

complete = 0



aphex = Player("aphex.jpg", 5, win_height - 180, 180, 180, 0, 0)


final = GameSprite('final.jpg', 600, 400, 80, 80)
run = True



complete += 1


def komnata():
    global w1, w2
    num = randint(1, 2)
    if num == 1:
        w1 = GameSprite("platform2.png", win_width / 2 - win_width / 3, win_height / 4, 300, 50)
        w2 = GameSprite("platform2_v.png", 370, 100, 50, 400)


    elif num == 2:
        w1 = GameSprite("platform2.png", 200, 66, 300, 50)
        w2 = GameSprite("platform2_v.png", 100, 100, 50, 400)


komnata()

barriers = sprite.Group()
barriers.add(w1)
barriers.add(w2)
font = font.SysFont('Comic Sans MS', 40)
win = font.render('YOU WIN', True, GREEN)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False





        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                aphex.x_speed = -5
            elif e.key == K_RIGHT:
                aphex.x_speed = 5
            elif e.key == K_UP:
                aphex.y_speed = -5
            elif e.key == K_DOWN:
                aphex.y_speed = 5

        elif e.type == KEYUP:
            if e.key == K_LEFT:
                aphex.x_speed = 0
            elif e.key == K_RIGHT:
                aphex.x_speed = 0
            elif e.key == K_UP:
                aphex.y_speed = 0
            elif e.key == K_DOWN:
                aphex.y_speed = 0
    window.blit(picture, (0, 0))

    final.reset()
    barriers.draw(window)
    aphex.reset()
    a.reset()

    a.update()
    aphex.update()
    time.delay(50)

    if sprite.collide_rect(aphex, final):
        window.blit(win, (300, 300))
        if complete <= 3:
            komnata()
            complete += 1
        else:
            run = False

    display.update()