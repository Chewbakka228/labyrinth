from pygame import *


class GameSprite(sprite.Sprite):
    def __init__(self, x, y, width, height, playerimage):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(playerimage), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, speedx, speedy, x, y, width, height, playerimage):
        GameSprite.__init__(self, x, y, width, height, playerimage)
        self.speedx = speedx
        self.speedy = speedy

    def update(self):
        if player.rect.x <= winw - 80 and player.speedx > 0 or player.rect.x >= 0 and player.speedx < 0:
            self.rect.x += self.speedx
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.speedx > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.speedx < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)

        if player.rect.y <= winw - 80 and player.speedy > 0 or player.rect.y >= 0 and player.speedy < 0:
            self.rect.y += self.speedy
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.speedy > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.speedy < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)


class Bullet(GameSprite):
    def __init__(self, bulletimage, x, y, width, height, speed):
        GameSprite.__init__(self, x, y, width, height, bulletimage)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > winw + 10:
            self.kill()


class Enemy(GameSprite):
    direction = 'left'

    def __init__(self, speed, x, y, width, height, enemyimage):
        GameSprite.__init__(self, x, y, width, height, enemyimage)
        self.speed = speed

    def update(self):
        if self.rect.x <= 420:
            self.direction = 'right'
        if self.rect.x >= winw - 85:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


winw = 700
winh = 500
window = display.set_mode((winw, winh))
back = (80, 80, 255)
display.set_caption('Лабиринт')

player = Player(0, 0, 5, winh - 80, 50, 50, 'playerimage.png')
enemy = Enemy(5, winw - 80, 180, 40, 50, 'enemy.png')
wall = GameSprite(winw / 2 - winw / 3, winh / 2, 300, 50, 'wall.png')
wall2 = GameSprite(370, 110, 50, 400, 'wall.png')
final = GameSprite(winw - 85, winh - 100, 100, 80, 'flag.png')
barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()
monsters.add(enemy)
barriers.add(wall)
barriers.add(wall2)
run = True
finish = False

while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                player.speedy = -5
            elif e.key == K_s:
                player.speedy = 5
            elif e.key == K_a:
                player.speedx = -5
            elif e.key == K_d:
                player.speedx = 5
            elif e.key == K_SPACE:
                player.fire()
        elif e.type == KEYUP:
            if e.key == K_w:
                player.speedy = 0
            elif e.key == K_s:
                player.speedy = 0
            elif e.key == K_a:
                player.speedx = 0
            elif e.key == K_d:
                player.speedx = 0

    if not finish:
        window.fill(back)
        player.reset()
        player.update()
        final.reset()
        barriers.draw(window)
        bullets.draw(window)
        bullets.update()
        monsters.draw(window)
        monsters.update()
        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets, monsters, True, True)
        if sprite.collide_rect(player, final):
            finish = True
            img = image.load('win.png')
            winner = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (winh * winner, winh)), (90, 0))
        if sprite.spritecollide(player, monsters, False):
            finish = True
            img = image.load('go.jpg')
            winner = img.get_width() // img.get_height()
            window.fill((0, 0, 0))
            window.blit(transform.scale(img, (winh * winner, winh)), (90, 0))
    else:
        finish = False
        for b in bullets:
            b.kill()
        for barrier in barriers:
            barrier.kill()
        for monster in monsters:
            monster.kill()
        time.delay(3000)
        enemy = Enemy(5, winw - 80, 180, 40, 50, 'enemy.png')
        monsters.add(enemy)
        wall = GameSprite(winw / 2 - winw / 3, winh / 2, 300, 50, 'wall.png')
        wall2 = GameSprite(370, 110, 50, 400, 'wall.png')
        barriers.add(wall)
        barriers.add(wall2)
    display.update()
    time.delay(50)
