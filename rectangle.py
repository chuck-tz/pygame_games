import pygame 
pygame.init()

win = pygame.display.set_mode((500,480))

pygame.display.set_caption("First Game")

bg = pygame.image.load('images/bg.jpg')
char = pygame.image.load('images/standing.png')
walkLeft = [pygame.image.load('images/L{}.png'.format(i)) for i in range(1,10)] 
walkRight = [pygame.image.load('images/R{}.png'.format(i)) for i in range(1,10)] 


clock = pygame.time.Clock()

x =50
y = 400
width = 64
height = 64
vel = 5

isJump = False
jumpCount = 10
left = False
right = False
walkCount = 0


run = True

def redrawGameWindow():
    global walkCount
    win.blit(bg, (0,0))
    
    if walkCount + 1 >=27:
        walkCount = 0

    if left:
        win.blit(walkLeft[walkCount//3], (x,y))
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount//3], (x,y))
        walkCount += 1
    else:
        win.blit(char, (x,y))

    pygame.display.update()

while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < 500 - width - vel:
        x += vel
        left = False
        right = True
    else:
        left = False
        right = False
        walkCount = 0

    if not isJump:
        if keys[pygame.K_SPACE]:
            isJump = True
            left = False
            right = False
            walkCount = 0
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= jumpCount**2 * 0.5 * neg
            jumpCount -= 1
        else:
           isJump = False
           jumpCount = 10    

    redrawGameWindow()
    
pygame.quit()
