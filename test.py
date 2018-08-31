import pygame
import math

#det virker
#?
pygame.init()

display_width = 800
display_height = 600

black, white, red, green, blue = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('test')
clock = pygame.time.Clock()

dudeImg = pygame.image.load('dude.png')


def dude(x, y):
	gameDisplay.blit(dudeImg, (x, y))


x = display_width * 0.45
y = display_height * 0.5



done = False

while not done:

	for event in pygame.event.get():

		x_change = 0
		y_change = 0

		#print(event)
		if event.type == pygame.QUIT:
			done = True

		keys = pygame.key.get_pressed()

		if keys[pygame.K_a] or keys[pygame.K_d]:
			if keys[pygame.K_a]:
				x_change = -2
				x_change += -3
			if keys[pygame.K_d]:
				x_change = 5
			if keys[pygame.K_d] and keys[pygame.K_a]:
				x_change = 0
		else:
			x_change = 0
		if keys[pygame.K_w] or keys[pygame.K_s]:
			if keys[pygame.K_w]:
				y_change = -5
			if keys[pygame.K_s]:
				y_change = 5
			if keys[pygame.K_w] and keys[pygame.K_s]:
				y_change = 0

		else:
			y_change = 0

	print(x_change, y_change)
	x += x_change
	y += y_change

	gameDisplay.fill(white)
	dude(x, y)
	#print(math.floor(x), y)
	#x += (1+(1/3))
	#y += 1
	pygame.display.update()
	clock.tick(30)

pygame.quit()
