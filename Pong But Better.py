import pygame
from pygame import *
import random
import time

pygame.init()
clock = pygame.time.Clock()

screenWidth = 600
screenHeight = 710

font = pygame.font.SysFont('Bauhaus', 30)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

fps = 60
movingLeft = False
movingRight = False
gameOver = False
score = 0
highScore = 0
timer = False
delay = 0.5

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Pong')

resetBtnImg = pygame.image.load('reset.png')
resetBtnImg = pygame.transform.scale(resetBtnImg, (100, 50))

class Button():

    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):

        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.reset(x, y)

    def update(self):
        global timer
        global score
        dx = 0
        if movingLeft:
            dx -= 5
        if movingRight:
            dx += 5

        if self.rect.right > screenWidth:
            self.rect.right = screenWidth
            dx = 0
        if self.rect.left < 0:
            self.rect.left = 0
            dx = 0

        self.rect.x += dx

        for ball in ballGroup:
            if pygame.sprite.spritecollide(ball, playerGroup, False):
                global velx
                global vely
                self.time = time.time()
                timer = True
                ball.velx = int(ball.speed * ball.velx)
                ball.vely = int(ball.speed * -1)
                if self.noAction == False:
                    score += 1
                    ball.speed += 0.1
                    ball.newBall = True
                self.noAction = True
                return ball.speed

        screen.blit(self.image, self.rect)

    def reset(self, x, y):
        img = pygame.image.load('white.jpg')
        self.image = pygame.transform.scale(img, (100, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.noAction = False

class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('ball.png')
        self.image = pygame.transform.scale(img, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1.0
        self.velx = random.randint(-1, 1)
        self.vely = random.randint(-1, 1)
        self.newBall = False

    def update(self):
        global gameOver
        global highScore
        if self.vely == 0:
            self.vely = random.randint(-1, 1)
        if self.velx == 0:
            self.velx = random.randint(-1, 1)

        if self.rect.right > screenWidth:
            self.velx = int(self.velx * -1)
            self.vely = self.vely
            if self.vely == 0:
                self.vely = random.randint(-1, 1)
        if self.rect.left < 0:
            self.velx = int(self.velx * -1)
            self.vely = self.vely
            if self.vely == 0:
                self.vely = random.randint(-1, 1)
        if self.rect.top < 0:
            self.velx = self.velx
            self.vely = int(self.vely * -1)
            if self.velx == 0:
                self.velx = random.randint(-1, 1)
        if self.rect.top > player.rect.bottom:
            for ball in ballGroup:
                ball.kill()
            if score > highScore:
                highScore  = score
            gameOver = True

        self.rect.x += self.velx
        self.rect.y += self.vely
        screen.blit(self.image, self.rect)

        if self.newBall:
            ball = Ball(random.randint(50, 550), random.randint(50, 400))
            ballGroup.add(ball)
        self.newBall = False

def drawText(text, font, textColor, x, y):
    img = font.render(text, True, textColor)
    screen.blit(img, (x, y))

playerGroup = pygame.sprite.Group()
ballGroup = pygame.sprite.Group()

ball = Ball(screenWidth / 2, screenHeight / 2)
ballGroup.add(ball)
player = Player(int(screenWidth / 2), 700)
playerGroup.add(player)

resetBtn = Button((screenWidth / 2 - 100), (screenHeight / 2 + 150), resetBtnImg)

run = True
while run:

    if gameOver == True:
        drawText('Game Over!', font, WHITE, (screenWidth / 2 - 100), (screenHeight / 2))
        drawText('Your Score: ' + str(score), font, WHITE, (screenWidth / 2 - 100), (screenHeight / 2 + 50))
        drawText('High Score: ' + str(highScore), font, WHITE, (screenWidth / 2 - 100), (screenHeight / 2 + 100))
        if resetBtn.draw():
            ball = Ball(screenWidth / 2, screenHeight / 2)
            ballGroup.add(ball)
            score = 0
            gameOver = False

    if gameOver == False:
        screen.fill(BLACK)
        player.update()
        for ball in ballGroup:
            ball.update()
        
        drawText('Score: ' + str(score), font, WHITE, 0, 0)

        clock.tick(fps)
        if timer:

            if time.time() - player.time >= delay:
                player.noAction = False
                player.time = 0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                movingLeft = True
            if event.key == pygame.K_d:
                movingRight = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                movingLeft = False
            if event.key == pygame.K_d:
                movingRight = False

    pygame.display.update()

pygame.quit()