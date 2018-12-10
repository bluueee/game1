import pygame, math
import main
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from random import randrange


class CharFlap():
	def __init__(self, xpos_start, ypos_start, dims, frameinfo, g_acc, speed, color):

		self.x = xpos_start
		self.y = ypos_start
		self.x_velocity = 0
		self.y_velocity = 0
		self.width = dims[0]
		self.height = dims[1]
		self.y_grav = g_acc
		self.y_accel = 0
		self.on_ground = False
		self.is_colliding_x = False
		self.is_colliding_y = False
		self.color = color
		self.colliding_top = False
		self.x1, self.y1 = self.x, self.y
		self.x2 = self.x + self.width
		self.y2 = self.y + self.height
		self.speed = speed
		self.added_xvel = 0
		self.added_yvel = 0

		self.score = 0

		self.oldprint = ''
		self.dingagain = True

		self.frame = frameinfo['frame']
		self.framewidth = frameinfo['framedims'][0]
		self.frameheight = frameinfo['framedims'][1]

	def updatepos(self):

		is_colliding_top_of_wall = False
		# kører 30 gange i sekundet, hastigheden ændres fra main filen for hvert keypress
		if (self.y + self.height <= self.frameheight or self.y_velocity < 0) and (self.y >= 0 or self.y_velocity > 0):

			if not self.colliding_top:
				self.y_velocity += self.y_grav #tyngdekraft

			if not self.y + self.y_velocity + self.height > self.frameheight and not self.y + self.y_velocity < 0:
				self.y += self.y_velocity
				self.on_ground = False

			elif self.y + self.y_velocity < 0:
				self.y = 0
				self.y_velocity = 0
				self.on_ground = False

			else:
				self.y = self.frameheight - self.height
				self.y_velocity = 0
				self.on_ground = True

		if (self.x + self.width <= self.framewidth or self.x_velocity < 0) and (self.x >= 0 or self.x_velocity > 0) and not self.is_colliding_x:
			if self.x + self.x_velocity + self.width > self.framewidth:
				self.x = self.framewidth - self.width
			elif self.x + self.x_velocity < 0:
				self.x = 0
			else:
				self.x += self.x_velocity
		#fix så man ikke kan blive skubbet ud af mappen men dør i stedet, og clean datastruktur up så hver væg kan have hver sin hastighed list med tuples {wall0:{colliding_x:T/F, colliding_y:T/F}, wall1:{}...].
		#eller gem det i selve væggen (måske lidt wonky)

		if self.y + self.height >= self.frameheight:
			return False
		if self.y <= 0:
			return False
		if self.x - self.width >= self.framewidth:
			return Fasle
		if self.x <= 0:
			return False
		if self.y1 <= 0:
			return False

		return True


	def jump(self):
		self.y_velocity = -10.5   # ELLER NOGET

	def check_collision(self, walls):		

		self.is_colliding_x, self.is_colliding_y = False, False

		self.x1, self.y1 = self.x, self.y
		self.colliding_top = False
		self.x2, self.y2 = self.x + self.width, self.y + self.height

		self.collissionData = []

		for wall in walls:

			wall.is_colliding_x, wall.is_colliding_y, wall.colliding_top = False, False, False

			#left of wall
			if ((self.x2 <= wall.x1 <= self.x2 + self.x_velocity - self.added_xvel or self.x2 <= wall.x1 and wall.x1 + wall.x_velocity <= self.x2 + self.x_velocity - self.added_yvel)
			and self.y1 + self.y_velocity - self.added_yvel < wall.y2  + wall.y_velocity
			and self.y2 + self.y_velocity - self.added_yvel > wall.y1 + wall.y_velocity):

				self.is_colliding_x, wall.is_colliding_x = True, True
				self.color = main.red
				return False

			#right of wall
			if ((self.x1 >= wall.x2 >= self.x1 + self.x_velocity - self.added_xvel or self.x1 >= wall.x2 and wall.x2 + wall.x_velocity >= self.x1 + self.x_velocity - self.added_xvel)
			and self.y1 + self.y_velocity - self.added_yvel < wall.y2  + wall.y_velocity
			and self.y2 + self.y_velocity - self.added_yvel > wall.y1 + wall.y_velocity):

				self.is_colliding_x, wall.is_colliding_x = True, True
				self.color = main.red
				return False

			#top of wall
			if ((self.y2 + self.y_velocity - self.added_yvel >= wall.y1 >= self.y2 or self.y2 + self.y_velocity - self.added_yvel >= wall.y1 + wall.y_velocity and wall.y1 >= self.y2)
			and self.x2 + self.x_velocity - self.added_xvel > wall.x1 + wall.x_velocity
			and self.x1 + self.x_velocity - self.added_xvel < wall.x2 + wall.x_velocity):

				self.color = main.red
				return False

				self.is_colliding_y, wall.is_colliding_y = True, True
				self.colliding_top, wall.colliding_top = True, True
				self.y_velocity = 0

			#bottom of wall
			if ((self.y1 + self.y_velocity - self.added_yvel <= wall.y2 <= self.y1 or self.y1 + self.y_velocity - self.added_yvel <= wall.y2 + wall.y_velocity and wall.y2 <= self.y1)
			and self.x2 + self.x_velocity - self.added_xvel > wall.x1 + wall.x_velocity
			and self.x1 + self.x_velocity - self.added_xvel < wall.x2 + wall.x_velocity):

				self.is_colliding_y, wall.is_colliding_y = True, True
				self.y_velocity = 0
				self.color = main.red
				return False

		return True

	def draw(self):
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glTranslate(self.x, self.y, 0)
		glBegin(GL_QUADS)
		glColor(*self.color)
		glVertex(0, 0, 0)
		glVertex(self.width, 0, 0)
		glVertex(self.width, self.height, 0)
		glVertex(0, self.height, 0)
		glEnd()

class CharPong():
	def __init__(self, xpos_start, ypos_start, dims, frameinfo, g_acc, speed, color, side):

		self.x = xpos_start
		self.y = ypos_start
		self.x_velocity = 0
		self.y_velocity = 0
		self.width = dims[0]
		self.height = dims[1]
		self.y_grav = g_acc
		self.y_accel = 0
		self.on_ground = False
		self.is_colliding_x = False
		self.is_colliding_y = False
		self.color = color
		self.colliding_top = False
		self.x1, self.y1 = self.x, self.y
		self.x2 = self.x + self.width
		self.y2 = self.y + self.height
		self.speed = speed

		self.score = 0

		self.oldprint = ''
		self.dingagain = True

		self.frame = frameinfo['frame']
		self.framewidth = frameinfo['framedims'][0]
		self.frameheight = frameinfo['framedims'][1]

		self.side = side

	def updatepos(self):

		# kører 30 gange i sekundet, hastigheden ændres fra main filen for hvert keypress
		if (self.y + self.height <= self.frameheight or self.y_velocity < 0) and (self.y >= 0 or self.y_velocity > 0):


			if not self.y + self.y_velocity + self.height > self.frameheight and not self.y + self.y_velocity < 0:
				self.y += self.y_velocity
				self.on_ground = False

			elif self.y + self.y_velocity < 0:
				self.y = 0
				self.on_ground = False

			else:
				self.y = self.frameheight - self.height
				self.on_ground = True


		#fix så man ikke kan blive skubbet ud af mappen men dør i stedet, og clean datastruktur up så hver væg kan have hver sin hastighed list med tuples {wall0:{colliding_x:T/F, colliding_y:T/F}, wall1:{}...].
		#eller gem det i selve væggen (måske lidt wonky)

		if self.y + self.height > self.frameheight:
			self.y = self.frameheight - self.height - 1
		if self.y < 0:
			self.y = 0
		if self.x - self.width > self.framewidth:
			self.x = self.framewidth - self.width
		if self.x < 0:
			self.x = 0


	def jump(self):
		self.y_velocity = -15   # ELLER NOGET
	
	def can_jump(self):
		return (self.on_ground or self.colliding_top) and self.y_velocity == 0

	def check_collision(self, walls):
		try:
			if abs(self.y_velocity) > abs(self.height):
				self.y_velocity = self.height * abs(self.y_velocity) / self.y_velocity
		except ZeroDivisionError:
			print('can\'t devide by zero')




		self.is_colliding_x, self.is_colliding_y = False, False

		self.x1, self.y1 = self.x, self.y
		self.colliding_top = False
		self.x2, self.y2 = self.x + self.width, self.y + self.height

		self.collissionData = []


		#if self.oldprint != '(' + str(self.x1) + ', ' + str(self.y1) + ') (' + str(self.x2) + ', ' + str(self.y2) + ')':
		#print('(', self.x1, ',', self.y1, ') (', self.x2, ',', self.y2, ')')
		#print(self.oldprint)
		#self.dingagain = True

		#self.oldprint = '(' + str(self.x1) + ', ' + str(self.y1) + ') (' + str(self.x2) + ', ' + str(self.y2) + ')'


		for wall in walls:

			if wall.ignore_bongs:
				return
			
			wall.is_colliding_x, wall.is_colliding_y, wall.colliding_top = False, False, False

			#right of wall
			if ((self.x2 <= wall.x1 <= self.x2 + self.x_velocity or self.x2 <= wall.x1 and wall.x1 + wall.x_velocity <= self.x2 + self.x_velocity)
			and self.y1 < wall.y2  + wall.y_velocity 
			and self.y2 > wall.y1 + wall.y_velocity):

				self.is_colliding_x, wall.is_colliding_x = True, True
				# print('ping' + str(walls.index(wall)))

			#left of wall
			if ((self.x1 >= wall.x2 >= self.x1 + self.x_velocity or self.x1 >= wall.x2 and wall.x2 + wall.x_velocity >= self.x1 + self.x_velocity)
			and self.y1 + self.y_velocity < wall.y2  + wall.y_velocity 
			and self.y2 + self.y_velocity > wall.y1 + wall.y_velocity):

				self.is_colliding_x, wall.is_colliding_x = True, True
				# print('ding' + str(walls.index(wall)))

			#top of wall
			if ((self.y2 + self.y_velocity >= wall.y1 >= self.y2 or self.y2 + self.y_velocity >= wall.y1 + wall.y_velocity and wall.y1 >= self.y2)
			and self.x2 + self.x_velocity > wall.x1 + wall.x_velocity 
			and self.x1 + self.x_velocity < wall.x2 + wall.x_velocity):

				self.is_colliding_y, wall.is_colliding_y = True, True
				self.colliding_top, wall.colliding_top = True, True
				self.y_velocity = 0

			#bottom of wall
			if ((self.y1 + self.y_velocity <= wall.y2 <= self.y1 or self.y1 + self.y_velocity <= wall.y2 + wall.y_velocity and wall.y2 <= self.y1)
			and self.x2 + self.x_velocity > wall.x1 + wall.x_velocity 
			and self.x1 + self.x_velocity < wall.x2 + wall.x_velocity):

				self.is_colliding_y, wall.is_colliding_y = True, True
				self.y_velocity = 0

			self.collissionData.append({'object': wall, 'wallnum' : walls.index(wall), 'is_colliding_y' : wall.is_colliding_y, 'is_colliding_x': wall.is_colliding_x, 'colliding_top': wall.colliding_top})

		return self.collissionData

	def limitspeed(self):
		if abs(self.y_velocity) > 10:
			if abs(self.y_velocity) > 0 and self.y_velocity > 0:
				self.y_velocity = self.speed
			elif abs(self.y_velocity) > 0 and self.y_velocity < 0:
				self.y_velocity = -self.speed


			#skriv logik for hvis man bliver mast HER:::::

	def draw_score(self, maxscore, score, side):

		self.slicewidth = self.framewidth / (maxscore * 2)

		if side == 'right':
			self.width = self.slicewidth * score

			self.y = 0
			self.x = 0


		if side == 'left':
			self.width = self.slicewidth * score

			self.x = self.framewidth - self.width
			self.y = 0
			
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glTranslate(self.x, self.y, 0)
		glBegin(GL_QUADS)
		glColor(*self.color)
		glVertex(0, 0, 0)
		glVertex(self.width, 0, 0)
		glVertex(self.width, self.height, 0)
		glVertex(0, self.height, 0)
		glEnd()


	def draw(self):
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glTranslate(self.x, self.y, 0)
		glBegin(GL_QUADS)
		glColor(*self.color)
		glVertex(0, 0, 0)
		glVertex(self.width, 0, 0)
		glVertex(self.width, self.height, 0)
		glVertex(0, self.height, 0)
		glEnd()

class CharBoxario(): #Parent
	def __init__(self, pos, dims, frameinfo, g_acc, speed, color):
		self.xpos_start, self.ypos_start = pos[0], pos[1]
		self.x = self.xpos_start
		self.y = self.ypos_start
		self.x_velocity = 0
		self.y_velocity = 0
		self.width = dims[0]
		self.height = dims[1]
		self.y_grav = g_acc
		self.y_accel = 0
		self.on_ground = False
		self.is_colliding_x = False
		self.is_colliding_y = False
		self.frame_colliding_x = False
		self.color = color
		self.colliding_top = False
		self.x1, self.y1 = self.x, self.y
		self.x2 = self.x + self.width
		self.y2 = self.y + self.height
		self.speed = speed
		self.lifespan = 0

		self.oldprint = ''
		self.dingagain = True

		self.frame = frameinfo['frame']
		self.framewidth = frameinfo['framedims'][0]
		self.frameheight = frameinfo['framedims'][1]

	def updatepos(self):
		self.lifespan += 1
		# kører 30 gange i sekundet, hastigheden ændres fra main filen for hvert keypress
		self.frame_colliding_x = False
		if (self.y + self.height <= self.frameheight or self.y_velocity < 0) and (self.y >= 0 or self.y_velocity > 0):

			if not self.colliding_top:
				self.y_velocity += self.y_grav #tyngdekraft

			if not self.y + self.y_velocity + self.height > self.frameheight and not self.y + self.y_velocity < 0:
				self.y += self.y_velocity
				self.on_ground = False

			elif self.y + self.y_velocity < 0:
				self.y = 0
				self.y_velocity = 0
				self.on_ground = False
			else:
				self.y = self.frameheight - self.height
				self.y_velocity = 0
				self.on_ground = True

		if (self.x + self.width <= self.framewidth or self.x_velocity < 0) and (self.x >= 0 or self.x_velocity > 0) and not self.is_colliding_x:
			if self.x + self.x_velocity + self.width > self.framewidth:
				self.x = self.framewidth - self.width
				self.frame_colliding_x = True
			elif self.x + self.x_velocity < 0:
				self.x = 0
				self.frame_colliding_x = True
			else:
				self.x += self.x_velocity

	def jump(self):
		self.y_velocity = -15
		# print(self.y_velocity)

	def smalljump(self):
		self.y_velocity = -5
	
	def can_jump(self):
		return (self.on_ground or self.colliding_top) and self.y_velocity == 0

	def resetenemytracking(self, enemies):
		for enemy in enemies:
			if enemy.movingdir == "AI_FOLLOW":
				enemy.movepath = []
				enemy.moveto = []

	def check_collision(self, walls, enemies):
		self.is_colliding_x = False
		self.is_colliding_y = False
		self.colliding_top = False
		self.x1, self.y1 = self.x, self.y
		self.x2 = self.x + self.width
		self.y2 = self.y + self.height
		self.dingagain = False

		if self.y2 > self.frameheight:
			self.x = self.frameheight-self.height-1

		if self.oldprint != '(' + str(self.x1) + ', ' + str(self.y1) + ') (' + str(self.x2) + ', ' + str(self.y2) + ')':
			#print('(', self.x1, ',', self.y1, ') (', self.x2, ',', self.y2, ')')
			###print(self.oldprint)
			self.dingagain = True

		self.oldprint = '(' + str(self.x1) + ', ' + str(self.y1) + ') (' + str(self.x2) + ', ' + str(self.y2) + ')'


		for wall in walls:
				if (self.x2 <= wall.x1 + wall.x_velocity <= self.x2 + self.x_velocity #Right Collision
				and self.y1 < wall.y2  + wall.y_velocity 
				and self.y2 > wall.y1 + wall.y_velocity
				and wall.rcollision):

					self.is_colliding_x = True
					self.x = wall.x1 - self.width + wall.x_velocity
					# print('ping' + str(walls.index(wall)))

				elif (self.x1 >= wall.x2 + wall.x_velocity >= self.x1 + self.x_velocity #Left Collision
				and self.y1 + self.y_velocity < wall.y2  + wall.y_velocity 
				and self.y2 + self.y_velocity > wall.y1 + wall.y_velocity
				and wall.lcollision):

					self.is_colliding_x = True
					self.x = wall.x2 + wall.x_velocity
					# print('ding' + str(walls.index(wall)))

				elif (self.y2 + self.y_velocity >= wall.y1 + wall.y_velocity >= self.y2 #Top Collision
				and self.x2 + self.x_velocity > wall.x1 + wall.x_velocity 
				and self.x1 + self.x_velocity < wall.x2 + wall.x_velocity
				and wall.tcollision):

					self.is_colliding_y = True
					self.colliding_top = True
					self.y = wall.y1 - self.height + wall.y_velocity
					self.y_velocity = 0

				elif (self.y1 + self.y_velocity <= wall.y2 + wall.y_velocity <= self.y1 #Bottom Collision
				and self.x2 + self.x_velocity > wall.x1 + wall.x_velocity 
				and self.x1 + self.x_velocity < wall.x2 + wall.x_velocity
				and wall.bcollision):

					self.is_colliding_y = True
					self.y = wall.y2 + wall.y_velocity
					self.y_velocity = 0

				elif (wall.x1+1 < self.x1 < wall.x2-1 #If wall Left Top is inside self
				and wall.y1+1 < self.y1 < wall.y2-1
				and wall.collisionkill
				and not wall.dead):
					self.alive = False
					try:
						self.kill(enemies)
					except:
						print('Tried to kill',self,'but failed. (This is supposed to fail if targeting a player)')
				
				elif (wall.x1+1 < self.x1 < wall.x2-1 #If wall Left Bottom is inside self
				and wall.y1+1 < self.y2 < wall.y2-1
				and wall.collisionkill
				and not wall.dead):
					self.alive = False
					try:
						self.kill(enemies)
					except:
						print('Tried to kill',self,'but failed. (This is supposed to fail if targeting a player)')

				elif (wall.x1+1 < self.x2 < wall.x2-1 #If wall Right Top is inside self
				and wall.y1+1 < self.y1 < wall.y2-1
				and wall.collisionkill
				and not wall.dead):
					self.alive = False
					try:
						self.kill(enemies)
					except:
						print('Tried to kill',self,'but failed. (This is supposed to fail if targeting a player)')

				elif (wall.x1+1 < self.x2 < wall.x2-1 #If wall Right Bottom is inside self
				and wall.y1+1 < self.y2 < wall.y2-1
				and wall.collisionkill
				and not wall.dead):
					self.alive = False
					try:
						self.kill(enemies)
					except:
						print('Tried to kill',self,'but failed. (This is supposed to fail if targeting a player)')

			

				#skriv logik for hvis man bliver mast HER:::::

			# print(self.x, self.x+self.width, walls[2].x1, walls[2].x2)
			# print(self.is_colliding_x, self.is_colliding_y)

	def draw(self):
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glTranslate(self.x, self.y, 0)
		glBegin(GL_QUADS)
		glColor(*self.color) #####REPLACE COLOR WITH TEXTURE
		glVertex(0, 0, 0)
		glVertex(self.width, 0, 0)
		glVertex(self.width, self.height, 0)
		glVertex(0, self.height, 0)
		glEnd()


class PlayerBoxario(CharBoxario):
	def __init__(self, pos, dims, frameinfo, g_acc, speed, color):
		self.score = 0
		CharBoxario.__init__(self, pos, dims, frameinfo, g_acc, speed, color)

	def updatepos(self):
		if self.alive:
			CharBoxario.updatepos(self)

	def check_collision(self, walls, enemies):
		if self.alive:
			CharBoxario.check_collision(self, walls, enemies)

			for enemy in enemies:
				if (self.y2 <= enemy.y1
				and self.y2 + self.y_velocity >= enemy.y1 + enemy.y_velocity #Top Collision
				and self.x2 + self.x_velocity >= enemy.x1 + enemy.x_velocity
				and self.x1 + self.x_velocity <= enemy.x2 + enemy.x_velocity
				and not enemy.dead):
					self.score += 1
					if self.y_velocity >= 0:
						self.jump()
					else:
						self.smalljump()
					enemy.kill(enemies)

				if (enemy.x1 <= self.x1 <= enemy.x2 #If  Left Top is inside enemy
				and enemy.y1 <= self.y1 <= enemy.y2
				and enemy.movingdir != "AI_FOLLOW"
				and not enemy.dead):
					self.alive = False

				elif (enemy.x1 <= self.x1 <= enemy.x2 #If  Left Bottom is inside enemy
				and enemy.y1 <= self.y2 <= enemy.y2
				and enemy.movingdir != "AI_FOLLOW"
				and not enemy.dead):
					self.alive = False

				elif (enemy.x1 <= self.x2 <= enemy.x2 #If  Right Top is inside enemy
				and enemy.y1 <= self.y1 <= enemy.y2
				and enemy.movingdir != "AI_FOLLOW"
				and not enemy.dead):
					self.alive = False

				elif (enemy.x1 <= self.x2 <= enemy.x2 #If  Right Bottom is inside enemy
				and enemy.y1 <= self.y2 <= enemy.y2
				and enemy.movingdir != "AI_FOLLOW"
				and not enemy.dead):
					self.alive = False

				elif (self.x1 <= enemy.x1 <= self.x2 #If  Left Top of enemy is inside
				and self.y1 <= enemy.y1 <= self.y2
				and not enemy.dead):
					self.alive = False

				elif (self.x1 <= enemy.x1 <= self.x2 #If  Left Bottom of enemy is inside
				and self.y1 <= enemy.y2 <= self.y2
				and not enemy.dead):
					self.alive = False

				elif (self.x1 <= enemy.x2 <= self.x2 #If  Right Top of enemy is inside
				and self.y1 <= enemy.y1 <= self.y2
				and not enemy.dead):
					self.alive = False

				elif (self.x1 <= enemy.x2 <= self.x2 #If  Right Bottom of enemy is inside
				and self.y1 <= enemy.y2 <= self.y2
				and not enemy.dead):
					self.alive = False


class EnemyBoxario(CharBoxario):
	def __init__(self, pos, dims, frameinfo, g_acc, speed, color, movingdir):
		self.dead = False
		self.aggrotime = 0
		self.g_acc = g_acc
		self.y_grav = self.g_acc
		CharBoxario.__init__(self, pos, dims, frameinfo, g_acc, speed, color)
		self.movingdir = movingdir
		self.moveto = []
		if self.movingdir == "R":
			self.x_velocity = self.speed
		elif self.movingdir == "L":
			self.x_velocity = -self.speed
		elif "AI" in self.movingdir:
			self.x_velocity = self.speed #Forhindrer error message - Ændres kort efter om nødvendigt.
		else:
			self.x_velocity = 0

		if self.movingdir == "AI_FOLLOW":
			self.height, self.width = main.playersize, main.playersize
			self.movepath = []

	def updatepos(self, player_x, player_y, player_x_velocity, player_y_velocity, player_height, enemies):
		self.enemies = enemies
		player_y2 = player_y + player_height
		if not self.dead:
			if randrange(main.fps*(11-main.difficulty)) == 1 and self.x_velocity < 2*self.speed:
				self.x_velocity *= 1 + main.difficulty / 100

			if self.movingdir is not "AI_FOLLOW":
				CharBoxario.updatepos(self)
				#print(self.frame_colliding_x, self.is_colliding_x)
				if self.is_colliding_x and self.lifespan > main.fps*10:
					if self.can_jump():
						self.jump()


			if self.movingdir == "AI_FOLLOW":
				self.movepath.append(player_x_velocity)
				self.movepath.append(player_y_velocity)

				#print(self.moveto)
				#print(self.movepath)

				if len(self.moveto) == 0 or (randrange(main.fps*30) == 0 and len(self.moveto) == 2):
					self.y_grav = self.g_acc
					self.moveto = [player_x, player_y]
					self.movepath = []
					self.aggrotime = 0
					for f in range(math.floor(main.fps*0.5)):
						self.movepath.append(0)
						self.movepath.append(0)
					self.color = (main.enemycolor)

				if len(self.moveto) == 1:
					self.y_grav = 0
					self.aggrotime += 1
					self.x_velocity = self.movepath[0]
					self.y_velocity = self.movepath[1]
					del self.movepath[0],self.movepath[0]
					CharBoxario.updatepos(self)
					#print('Following path...')

				elif (abs(self.moveto[0]-self.x) <= abs(self.x_velocity)
				and abs(self.moveto[1]-self.y) <= abs(self.y_velocity)):
					if self.x_velocity != 0:
						self.x_velocity = self.x_velocity/abs(self.x_velocity)*self.speed
					self.x_velocity = self.moveto[0]-self.x
					self.y_velocity = self.moveto[1]-self.x
					self.moveto = ['Reached']
					self.color = (main.targetlockcolor)
					#print('Destination reached.')

				else:
					if len(self.moveto) == 2:
						if ((self.moveto[0] - 50 < self.x < self.moveto[0] + 50 and self.moveto[1] < self.y)
						or self.is_colliding_x
						or randrange(main.fps*5) == 1):
							if self.can_jump():
								self.jump()

						if self.x > self.moveto[0] + 50 and randrange(main.fps*1) == 1:
							self.x_velocity = -abs(self.x_velocity)
						elif self.x < self.moveto[0] - 50 and randrange(main.fps*1) == 1:
							self.x_velocity = abs(self.x_velocity)
						CharBoxario.updatepos(self)

			if self.movingdir == "AI_CHASE":
				if player_x - 50 < self.x < player_x + 50 and randrange(main.fps*1) == 1:
					if self.can_jump():
						self.jump()

				if self.x > player_x + 50 and randrange(main.fps*1) == 1:
					self.x_velocity = -abs(self.x_velocity)
				elif self.x < player_x - 50 and randrange(main.fps*1) == 1:
					self.x_velocity = abs(self.x_velocity)
			
			elif self.movingdir == "AI_FLEE":
				if self.x < 25:
					self.x_velocity = abs(self.x_velocity)
				elif self.x > self.framewidth - 25 - self.width:
					self.x_velocity = -abs(self.x_velocity)
				elif 50 < self.x < player_x:
					self.x_velocity = -abs(self.x_velocity)
				elif player_x < self.x < self.framewidth - 50 - self.width:
					self.x_velocity = abs(self.x_velocity)
			
			elif self.frame_colliding_x or self.is_colliding_x or randrange(main.fps*15) == 1:
				self.x_velocity *= -1
			
			if self.can_jump() and not (self.y1 > player_y2 and self.y1 - 15 <= player_y2):
				if randrange(main.fps*5) == 1:
					self.jump()

	def kill(self, enemies):
		self.dead = True
		CharBoxario.resetenemytracking(self, self.enemies)



