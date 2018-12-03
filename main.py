from charclass import *
from wallclass import *
import time, random, math, pygame, os
import numpy as np

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (250,50)

#########################
# TO DO:                #
# Dive bomb             #
# Enemies go into walls #
#########################

display_width = 800
display_height = 600
fps = 60
clock = pygame.time.Clock()
frameNum = 0

difficulty = 5 #5
winscore = 25 #25
randomenemysize = True
enemiesfollow = False

win = False

enemies = []

enemysize = 50
enemyspeed = 2

playersize = 50
playerspeed = 5

enemyspawner1 = (25, display_height-enemysize-25)
enemyspawner2 = (display_width-enemysize-25, display_height-enemysize-25)
playerspawner1 = (150, display_height-playersize)

gravity = 0.5

aDown = False
dDown = False
spaceDown = False

wallxvel = 0
wallyvel = 0

randomcolorvar = np.arange(0.5, 1, 0.5/winscore)
black, white, red, green, blue = (0.1, 0.1, 0.1, 1), (1, 1, 1, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)
enemycolor = (0, 0, randomcolorvar[randrange(len(randomcolorvar))], 1)
targetlockcolor = (0.25, 0, randomcolorvar[randrange(len(randomcolorvar))], 1)
enemyspawnercolor = (0.15, 0.1, 0.1, 1)

black, white, red, blue, green = (0.1, 0.1, 0.1, 1), (1, 1, 1, 1), (1, 0, 0, 1), (0, 0, 1, 1), (0, 1, 0, 1)
display_width = 800
display_height = 600
spaceDown = False

framenum = 0
framenum2 = 0

gamemode = 3

aaa = 1

player_width = 25
player_height = 100
ball_width = 25
ball_height = 25

max_score = 5


fps = 60
buff = 15

frameNum = 0

print('initialized')

def loadimg(filename):
	img = Image.open(filename)
	img_data = np.array(list(img.getdata()), np.int8)

	imgid = glGenTextures(1)
	glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
	glBindTexture(GL_TEXTURE_2D, imgid)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_FLOAT, img_data)
	print(imgid)
	return imgid
	#imgvar = pygame.image.load('/'+img)
	#textureData = pygame.image.tostring(imgvar, "RGB", 1)
	#imgwidth = imgvar.get_width()
	#imgheight = imgvar.get_height()
	#glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
	#glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	#glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, imgwidth, imgheight, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)
	#glEnable(GL_TEXTURE_2D)
				

def randomspawner():
	return [enemyspawner1,enemyspawner2][randrange(2)]

def randomAI():
	if enemiesfollow:
		return "AI_FOLLOW"
	else:
		#return ["AI_FOLLOW","AI_FLEE","AI_CHASE","L"][randrange(4)]
		return ["AI_FOLLOW","AI_FLEE","AI_CHASE"][randrange(3)]

def spawnenemy():
	if randomenemysize:
		enemies.append(EnemyBoxario(randomspawner(), (math.floor(randrange(enemysize/2, enemysize)), math.floor(randrange(enemysize/2, enemysize))), frameInfo, gravity, enemyspeed, enemycolor, randomAI()))
	else:
		enemies.append(EnemyBoxario(randomspawner(), (enemysize, enemysize), frameInfo, gravity, enemyspeed, enemycolor, randomAI()))

def allenemiesdead(enemies):
	for enemy in enemies:
		if enemy.dead == False:
			return False
	return True

def allenemiesfollowing(enemies):
	for enemy in enemies:
		if len(enemy.moveto) != 1 or enemy.aggrotime < fps*0.5:
			return False
	return True

def defspawners():
	return [
	WallBoxario(enemyspawner1, (enemyspawner1[0] + enemysize, enemyspawner1[1] + enemysize), enemyspawnercolor, wallxvel, wallyvel, False, False, False, False),
	WallBoxario(enemyspawner2, (enemyspawner2[0] + enemysize, enemyspawner2[1] + enemysize), enemyspawnercolor, wallxvel, wallyvel, False, False, False, False)
	]

def defwalls():
	return defspawners() + [
	WallBoxario((300, 525), (400, 600), white, wallxvel, wallyvel),
	WallBoxario((500, 400), (600, 524), white, wallxvel, wallyvel),
	#Wall((690, 370), (740, 420), white, wallxvel, wallyvel),
	#Wall((450, 250), (550, 300), white, wallxvel, wallyvel),
	#Wall((200, 175), (210, 260), white, wallxvel, wallyvel),
	#Wall((260, 175), (270, 260), white, wallxvel, wallyvel),
	#Wall((200, 250), (260, 260), white, wallxvel, wallyvel),
	#Wall((280, 175), (290, 260), white, wallxvel, wallyvel),
	#Wall((340, 175), (350, 260), white, wallxvel, wallyvel),
	#Wall((280, 250), (340, 260), white, wallxvel, wallyvel),
	#Wall((180, 175), (190, 260), white, wallxvel, wallyvel)
	]

def defenemies():
	for i in range(difficulty):
		spawnenemy()

def defplayer():
	return PlayerBoxario(playerspawner1, (playersize, playersize), frameInfo, gravity, playerspeed, red)

def drawscreen():
	glClear(GL_COLOR_BUFFER_BIT)
	glClear(GL_DEPTH_BUFFER_BIT)

	for wall in walls:
		wall.updatepos()
		wall.draw()
	
	for enemy in enemies:
		if not enemy.dead:
			enemy.check_collision(walls, enemies)
			enemy.updatepos(char.x, char.y, char.x_velocity, char.y_velocity, char.height, enemies)
			enemy.draw()

	if allenemiesdead(enemies) or allenemiesfollowing(enemies):
		win = True
		char.alive = False #Restarts the game
		char.color = green

	char.check_collision(walls, enemies)
	char.updatepos()
	char.draw()


if __name__ == '__main__':

	pygame.init()

	gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.DOUBLEBUF | pygame.OPENGL)
	pygame.display.set_caption('g a m e s')

	frameInfo = {'frame':gameDisplay, 'framedims':(display_width, display_height)}

	if gamemode == 1:

		while True:
			char = CharFlap(100, 50, (35, 35), frameInfo, 0.45, 5, green)

			previous = time.time() * 1000

			glClearColor(*black)
			glMatrixMode(GL_PROJECTION)
			glLoadIdentity()
			glOrtho(0, display_width, display_height, 0, -1, 3)

			alive = True
			clock = pygame.time.Clock()

			wallyvel = -1
			wallxvel = 0

			walls = [WallFlap((-10, -10), (-20, -20), black, -10, 0, frameInfo)]
			index = 0


			framenum = 0
			char.y_velocity = 0
			shouldjump = False
			space_pressed_once = False

			while alive:

				for event in pygame.event.get():

					if event.type == pygame.QUIT:
						exit()

					if event.type == pygame.KEYDOWN:

						if event.key == pygame.K_SPACE or event.key == pygame.K_w:

							if not spaceDown:
								shouldjump = True
							else:
								shouldjump = False
							spaceDown = True

							if spaceDown and shouldjump:
								char.jump()

					if event.type == pygame.KEYUP:

						if event.key == pygame.K_SPACE or event.key == pygame.K_w:
							spaceDown = False
							shouldjump = False

				alive = char.check_collision(walls)

				if not alive:
					char.updatepos()
				else:
					alive = char.updatepos()

				framenum += 1

				glClear(GL_COLOR_BUFFER_BIT)
				glClear(GL_DEPTH_BUFFER_BIT)

				for wall in walls:
					wall.updatepos()
					wall.draw()

				if framenum % fps == 0:
					#print(clock.get_fps())
					framenum = 0

				framenum2 += 1
				if framenum2 % (fps * 2)  == 0:
					for wall in walls[0].spawn_boxes(40, 180, (-3, 0), white):
						walls.append(wall)
					for wall in walls[1:]:
						if wall.x2 < 0:
							walls[walls.index(wall)] = walls[-1]
							del(walls[-1])
					walls[0].check_point_trigger(walls, char)



					framenum2 = 0

				char.draw()
				pygame.display.flip()

			time.sleep(1)


	elif gamemode == 2:
		while True:

			gameover = False

			startvar = [-1, 1]

			pygame.init()

			gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.DOUBLEBUF | pygame.OPENGL)
			pygame.display.set_caption('g a m e s')

			frameInfo = {'frame':gameDisplay, 'framedims':(display_width, display_height)}
			# char = Char(display_width * 0.45, display_height * 0.5, 50, 50, frameinfo, 3)
			char = CharPong(buff, 0, (player_width, player_height), frameInfo, 0.5, 6, blue, 'left')
			char2 = CharPong(display_width - player_width - buff, display_height - player_height, (player_width, player_height), frameInfo, 0.5, 6, blue, 'right')

			leftbar = CharPong(0, display_height - 5, (display_width, 5), frameInfo, 0.5, 6, white, 'bottom')
			rightbar = CharPong(0, display_height - 5, (display_width, 5), frameInfo, 0.5, 6, white, 'bottom')

			while not gameover:

				previous = time.time() * 1000

				glClearColor(*black)
				glMatrixMode(GL_PROJECTION)
				glLoadIdentity()
				glOrtho(0, display_width, display_height, 0, -1, 3)

				clock = pygame.time.Clock()

				frameNum = 0

				ball = BallPong((400, 300), (400 + ball_width, 300 + ball_height), red, -3 * startvar[random.randrange(2)], startvar[random.randrange(2)] * 2, frameInfo)

				alive = True

				w_down, s_down, UP_down, DOWN_down = False, False, False, False


				while alive:

					current = time.time() * 1000
					elapsed = current - previous
					previous = current
					delay = 1000.0 / fps - elapsed
					delay = max(int(delay), 0)


					for event in pygame.event.get():

						if event.type == pygame.QUIT:
							exit()

						if event.type == pygame.KEYDOWN:
							if event.key == pygame.K_w:
								w_down = True

							if event.key == pygame.K_s:
								s_down = True

							if event.key == pygame.K_UP:
								UP_down = True

							if event.key == pygame.K_DOWN:
								DOWN_down = True

							if event.key == pygame.K_r:
								alive = False


						if event.type == pygame.KEYUP:
							if event.key == pygame.K_w:
								w_down = False

							if event.key == pygame.K_s:
								s_down = False

							if event.key == pygame.K_UP:
								UP_down = False

							if event.key == pygame.K_DOWN:
								DOWN_down = False

						if w_down and not s_down:
							char.y_velocity = -char.speed
						if s_down and not w_down:
							char.y_velocity = char.speed
						if w_down == s_down:
							char.y_velocity = 0

						if UP_down and not DOWN_down:
							char2.y_velocity = -char2.speed
						if DOWN_down and not UP_down:
							char2.y_velocity = char2.speed
						if UP_down == DOWN_down:
							char2.y_velocity = 0

						char.limitspeed()
						char2.limitspeed()

					ball.check_collission([char, char2])
					#alive, gameover = ball.update_score([char, char2], [leftbar, rightbar])
					#alive, gameover = ball2.update_score([char, char2], [leftbar, rightbar])
					#print(char.is_colliding_x, char.is_colliding_y)

					char.updatepos()
					char2.updatepos()

					glClear(GL_COLOR_BUFFER_BIT)
					glClear(GL_DEPTH_BUFFER_BIT)

					alive, gameover = ball.update_score([char, char2], [leftbar, rightbar])

					char.draw()
					char2.draw()

					leftbar.draw_score(max_score, char.score, char.side)
					rightbar.draw_score(max_score, char2.score, char2.side)

					ball.updatepos()
					ball.draw()

					pygame.display.flip()
					clock.tick(fps)

					ball.limitvelocity(15, 5)

				time.sleep(1)

			time.sleep(2)

	elif gamemode == 3:
		while True:
			char = defplayer()
			walls = defwalls()

			enemies = []
			defenemies()

			previous = time.time() * 1000

			glClearColor(*black)
			glMatrixMode(GL_PROJECTION)
			glLoadIdentity()
			glOrtho(0, display_width, display_height, 0, -1, 3)

			# wall1 = Wall((display_width*0.6-100, 500-75), (display_width*0.5, display_height-75), white, frameinfo)

			char.alive = True
			char.score = 0
			spacedown, aDown, sDown, dDown = False, False, False, False

			while char.alive: #Runs each frame

				current = time.time() * 1000
				elapsed = current - previous
				previous = current
				delay = 1000.0/fps - elapsed
				delay = max(int(delay), 0)

				if randrange(fps*(11-difficulty)) == 1 and len(enemies) < winscore:
					spawnenemy()

				for event in pygame.event.get():

					if event.type == pygame.QUIT:
						exit()

					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_p:
							print('"P" pressed. Shutting down...')
							time.sleep(0.1)
							exit()

						elif event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
							spaceDown = True
						
						elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
							aDown = True

						elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
							sDown = True

						elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
							dDown = True

						elif event.key == pygame.K_r:
							char.alive = False

						### Single-press Keys
						elif event.key == pygame.K_t:
							if randomenemysize:
								randomenemysize = False
							else:
								randomenemysize = True

						elif event.key == pygame.K_y:
							if enemiesfollow:
								enemiesfollow = False
							else:
								enemiesfollow = True

						elif event.key == pygame.K_1:
							difficulty = 1
						elif event.key == pygame.K_2:
							difficulty = 2
						elif event.key == pygame.K_3:
							difficulty = 3
						elif event.key == pygame.K_4:
							difficulty = 4
						elif event.key == pygame.K_5:
							difficulty = 5
						elif event.key == pygame.K_6:
							difficulty = 6
						elif event.key == pygame.K_7:
							difficulty = 7
						elif event.key == pygame.K_8:
							difficulty = 8
						elif event.key == pygame.K_9:
							difficulty = 9
						elif event.key == pygame.K_0:
							difficulty = 10


					if event.type == pygame.KEYUP:

						if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
							spaceDown = False

						elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
							aDown = False

						elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
							sDown = False

						elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
							dDown = False

						
					if aDown and not dDown:
						char.x_velocity = -char.speed

					elif dDown and not aDown:
						char.x_velocity = char.speed

					elif dDown == aDown:
						char.x_velocity = 0
				# (char.can_jump(), char.y_velocity)

				if char.can_jump() and spaceDown:
					char.jump()
				# print(char.x_velocity, char.y_velocity)

				drawscreen()
				pygame.display.flip()

				'''
				if frameNum % fps == 0:
					print(frameNum)
				'''
				frameNum += 1

				clock.tick(fps)
				#print('fps:',clock.get_fps())

			time.sleep(0.5)
			drawscreen()
			time.sleep(0.5)
			#Reaching here restarts game

