import sys
import pygame
import random
import math
import time
from pygame.locals import *

WIDTH = 1080
HEIGHT = 840


INVADER_HEIGHT = 25
INVADER_LENGTH = 75

INVADER_GAP = 25


BULLET_LENGTH = 5
BULLET_HEIGHT = 5
DEFENDER_HEIGHT = 25
DEFENDER_LENGTH = 75

LEFT = -0.3
RIGHT = 0.3

variables = [RIGHT]
bullets = []
invaders = []

def createBullet(x, y, screen, team):
	if team == 1:
		target = invaders
	if team == 2:
		target = player
	bullets.append(Bullet(x, y, screen, target))

def resetInvaders():
	for i in range(10):
		for j in range(6):
			invaders.append(Invader(30 + i * (INVADER_GAP + INVADER_LENGTH), 0 + j * (INVADER_GAP + INVADER_HEIGHT), screen, variables))


class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, screen, target):
		super(Bullet, self).__init__()
		self.x = x
		self.y = y
		self.screen = screen
		self.target = target
		self.speed = 2
		self.surf = pygame.Surface((BULLET_LENGTH, BULLET_HEIGHT))
		self.surf.fill((255, 0, 0))
		if type(self.target) == list:
			self.speed = -2
    
	def update(self):
		if self.y < 0 or self.y > HEIGHT:
			return 1
		else:
			self.y += self.speed
			if type(self.target) == list:
				for i in self.target:
					if self.x > i.x - BULLET_LENGTH and self.x < i.x + DEFENDER_LENGTH and self.y + BULLET_HEIGHT > i.y and self.y < i.y + DEFENDER_HEIGHT:
						return i
			else:
				if self.x > self.target.x - BULLET_LENGTH and self.x < self.target.x + DEFENDER_LENGTH and self.y + BULLET_HEIGHT > self.target.y and self.y < self.target.y + DEFENDER_HEIGHT:
					self.target.lives -= 1
					return 1
			self.screen.blit(self.surf, (self.x, self.y))

class Character(pygame.sprite.Sprite):
	def __init__(self, x, y, screen, lives):
		super(Character, self).__init__()
		self.x = x
		self.y = y
		self.screen = screen
		self.lives = lives

class Invader(Character):
	def __init__(self, x, y, screen, variables):
		super().__init__(x, y, screen, 1)
		self.team = 2
		self.surf = pygame.Surface((INVADER_LENGTH, INVADER_HEIGHT))
		self.surf.fill((255, 255, 255))
		self.variables = variables
		self.prev = 1
    
	def update(self):
		if self.prev != variables[0]:
			self.y = self.y + INVADER_HEIGHT + INVADER_GAP
		self.x = self.x + variables[0]
		if self.x <= 0 or self.x >= WIDTH - INVADER_LENGTH:
			variables[0] *= -1
			self.y = self.y + INVADER_HEIGHT + INVADER_GAP
		self.prev = variables[0]
		self.screen.blit(self.surf, (self.x, self.y))

		if random.randint(1, 1000) == 1:
			createBullet(self.x + INVADER_LENGTH / 2, self.y + INVADER_HEIGHT, self.screen, self.team)

	def shoot(self):
		pass

class Defender(Character):
	def __init__(self, x, y, screen):
		super().__init__(x, y, screen, 3)
		self.team = 1
		self.surf = pygame.Surface((DEFENDER_LENGTH, DEFENDER_HEIGHT))
		self.surf.fill((255, 255, 255))
		self.time = -1
	def update(self, pressed_keys):
		if pressed_keys[K_LEFT]:
			self.x = self.x - 5
			if self.x < 0:
				self.x = 0
		if pressed_keys[K_RIGHT]:
			self.x = self.x + 5
			if self.x > WIDTH - DEFENDER_LENGTH:
				self.x = WIDTH - DEFENDER_LENGTH
		if pressed_keys[K_SPACE] and time.time() - self.time > 0.5:
			createBullet(self.x + DEFENDER_LENGTH / 2, self.y + DEFENDER_HEIGHT - BULLET_HEIGHT, self.screen, self.team)
			self.time = time.time()
		self.screen.blit(self.surf, (self.x, self.y))

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
running = True
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
player = Defender(30, 800, screen)
gameOver = False
f = open("highScore.txt", "r")
highScore = f.readline()
f.close()
newHighScore = False
while running:
	screen.fill((0, 0, 0))
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == K_ESCAPE:
				running = False
			# if event.key == K_TAB:
			# 	fps = 240
			# else:
			# 	fps = 60
			if event.key == K_r and gameOver:
				gameOver = False
				score = 0
				newHighScore = False
				invaders = []
				bullets = []
				player = Defender(30, 800, screen)
		if event.type == pygame.QUIT:
			running = False
	if gameOver:
		if score > int(highScore):
			f = open("highScore.txt", "w")
			newHighScore = True
			f.write(str(score))
			highScore = score
			f.close()
		gameOverText = font.render(f'Game Over', True, (255, 0, 0))
		gameOverTextRect = gameOverText.get_rect()
		gameOverTextRect.center = (WIDTH / 2, HEIGHT / 2 - 80)
		screen.blit(gameOverText, gameOverTextRect)

		playAgainText = font.render(f'Press R to restart', True, (255, 0, 0))
		playAgainTextRect = playAgainText.get_rect()
		playAgainTextRect.center = (WIDTH / 2, HEIGHT / 2 - 40)
		screen.blit(playAgainText, playAgainTextRect)

		scoreText = font.render(f'Score: {score}', True, (0, 0, 255))
		scoreTextRect = scoreText.get_rect()
		scoreTextRect.center = (WIDTH / 2, HEIGHT / 2)
		screen.blit(scoreText, scoreTextRect)

		highScoreText = font.render(f'High Score: {highScore}', True, (0, 0, 255))
		highScoreTextRect = highScoreText.get_rect()
		highScoreTextRect.center = (WIDTH / 2, HEIGHT / 2 + 40)
		screen.blit(highScoreText, highScoreTextRect)

		closeText = font.render(f'Press Escape to Quit', True, (0, 0, 255))
		closeTextRect = closeText.get_rect()
		closeTextRect.center = (WIDTH / 2, HEIGHT / 2 + 80)
		screen.blit(closeText, closeTextRect)

		pygame.display.flip()
		fpsClock.tick(fps)
		continue


	if len(invaders) == 0:
		resetInvaders()
	pressed_keys = pygame.key.get_pressed()
	for i in invaders:
		i.update()
	for i in bullets:
		x = i.update()
		if x:
			bullets.remove(i)
		if type(x) == Invader:
			invaders.remove(x)
			score += 10
	scoreText = font.render(f'Score: {score}', True, (0, 0, 255))
	livesText = font.render(f'Lives: {player.lives}', True, (0, 0, 255))
	scoreTextRect = scoreText.get_rect()
	livesTextRect = livesText.get_rect()
	scoreTextRect.midleft = (20, 25)
	livesTextRect.midright = (1060, 25)
	screen.blit(scoreText, scoreTextRect)
	screen.blit(livesText, livesTextRect)
	if score > int(highScore):
		highScoreText = font.render(f'High Score: {score}', True, (0, 0, 255))
	else:
		highScoreText = font.render(f'High Score: {highScore}', True, (0, 0, 255))
	highScoreTextRect = highScoreText.get_rect()
	highScoreTextRect.center = (WIDTH / 2, 25)
	screen.blit(highScoreText, highScoreTextRect)

	if player.lives == 0:
		gameOver = True
	player.update(pressed_keys)

	pygame.display.flip()
	fpsClock.tick(fps)

pygame.quit()
sys.exit()