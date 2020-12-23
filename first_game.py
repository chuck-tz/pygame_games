import pygame 
pygame.init()

win = pygame.display.set_mode((500,480))

pygame.display.set_caption("First Game")

bg = pygame.image.load('images/bg.jpg')
char = pygame.image.load('images/standing.png')
walkLeft = [pygame.image.load('images/L{}.png'.format(i)) for i in range(1,10)] 
walkRight = [pygame.image.load('images/R{}.png'.format(i)) for i in range(1,10)] 


clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('sounds/bullet.wav')
hitSound = pygame.mixer.Sound('sounds/hit.wav')

music = pygame.mixer.music.load('sounds/music.mp3')
pygame.mixer.music.play(-1)

score = 0

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = True
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >=27:
            self.walkCount = 0
        
        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0],(self.x, self.y))
            else:
                win.blit(walkLeft[0],(self.x, self.y))

        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10 
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (250 - text.get_width()/2, 200))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 101
                    pygame.quit()

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(object):
    walkLeft = [pygame.image.load('images/L{}E.png'.format(i)) for i in range(1,12)] 
    walkRight = [pygame.image.load('images/R{}E.png'.format(i)) for i in range(1,12)]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visable = True

    def draw(self, win):
        self.move()
        if self.visable:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 5 * self.health, 10))             
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
    
    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.visable = False 
        print('hit') 
    

def redrawGameWindow():

    win.blit(bg, (0,0))
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (370, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


font = pygame.font.SysFont('comicsans', 30, True)
man = player(300, 400, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
shootLoop = 0
bullets = []
run = True
while run:
    clock.tick(27)

    if goblin.visable \
    and man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] \
    and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1] \
    and man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] \
    and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
        man.hit()
        score -= 5

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] \
        and bullet.y + bullet.radius > goblin.hitbox[1] \
        and bullet.x + bullet.radius > goblin.hitbox[0] \
        and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
            hitSound.play()
            goblin.hit()
            score += 1
            bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.width // 2), 6, (0,0,0), facing))
        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not man.isJump:
        if keys[pygame.K_UP]:
            man.isJump = True
            man.left = False
            man.right = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= man.jumpCount**2 * 0.5 * neg
            man.jumpCount -= 1
        else:
           man.isJump = False
           man.jumpCount = 10    

    redrawGameWindow()
    
pygame.quit()