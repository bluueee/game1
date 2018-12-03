import pygame
import main
import charclass
from OpenGL.GL import *
from random import randrange


class WallFlap():

	def __init__(self, p1, p2, color, x_velocity, y_velocity, frameinfo):
		self.p1 = p1
		self.p2 = p2

		self.x1 = p1[0]
		self.y1 = p1[1]
		self.x2 = p2[0]
		self.y2 = p2[1]

		self.frameinfo = frameinfo

		self.color = color
		self.is_collidng_x = False
		self.is_collidng_y = False

		self.width = self.x2 - self.x1
		self.height = self.y2 - self.y1

		self.x_velocity = x_velocity
		self.y_velocity = y_velocity
		self.colliding_top = False

		self.hasAddedx1, self.hasAddedx2, self.hasAddedy = False, False, False

		self.frame = frameinfo['frame']
		self.framewidth = frameinfo['framedims'][0]
		self.frameheight = frameinfo['framedims'][1]

		self.triggeredpoint = False

		self.pointdata = []

		self.templist = []



	def updatepos(self):
		self.x1 += self.x_velocity
		self.x2 += self.x_velocity
		self.y1 += self.y_velocity
		self.y2 += self.y_velocity

	def spawn_boxes(self, width, space, velocities, color):

		upper_box_p1 = [self.framewidth, 0]
		upper_box_p2 = [self.framewidth + width, randrange(0, self.frameheight - space - 25)]

		lower_box_p1 = [self.framewidth, upper_box_p2[1] + space]
		lower_box_p2 = [self.framewidth + width, self.frameheight]

		return (WallFlap(upper_box_p1, upper_box_p2, color, velocities[0], velocities[1], self.frameinfo), WallFlap(lower_box_p1, lower_box_p2, color, velocities[0], velocities[1], self.frameinfo))


	def check_point_trigger(self, walls, char):
		pass
		
		#skriv her

	def draw(self):
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glTranslate(self.x1, self.y1, 0)
		glBegin(GL_QUADS)
		glColor(*self.color)
		glVertex(0, 0, 0)
		glVertex(self.width, 0, 0)
		glVertex(self.width, self.height, 0)
		glVertex(0, self.height, 0)
		glEnd()

class BallPong():
	def __init__(self, p1, p2, color, x_velocity, y_velocity, frameinfo):
		self.x1 = p1[0]
		self.y1 = p1[1]
		self.x2 = p2[0]
		self.y2 = p2[1]

		self.hitcount = 0

		self.color = color
		self.is_collidng_x = False
		self.is_collidng_y = False

		self.width = self.x2 - self.x1
		self.height = self.y2 - self.y1

		self.x_velocity = x_velocity
		self.y_velocity = y_velocity
		self.colliding_top = False

		self.frame = frameinfo['frame']
		self.framewidth = frameinfo['framedims'][0]
		self.frameheight = frameinfo['framedims'][1]
		self.ignore_bongs = False

	def updatepos(self):
		self.x1 += self.x_velocity
		self.x2 += self.x_velocity
		self.y1 += self.y_velocity
		self.y2 += self.y_velocity

	def check_collission(self, chars):


		try:
			if abs(self.x_velocity) > abs(chars[0].width):
				self.x_velocity = abs(chars[0].width) * abs(self.x_velocity) / self.x_velocity
			if abs(self.y_velocity) > abs(chars[0].height):
				self.y_velocity = chars[0].height * abs(self.y_velocity) / self.y_velocity
		except ZeroDivisionError:
			print('can\'t devide by zero')

		# frame collsssion:

		if self.y1 <= 0:
			self.y_velocity *= -1.05
		elif self.y2 >= self.frameheight:
			self.y_velocity *= -1.05

		# player collission:

		for char in chars:

			char.is_colliding_x, char.is_colliding_y = False, False

			char.x1, char.y1 = char.x, char.y
			char.colliding_top = False
			char.x2, char.y2 = char.x + char.width, char.y + char.height

			char.collissionData = []
				
			self.is_colliding_x, self.is_colliding_y, self.colliding_top = False, False, False


			#right of self
			if ((char.x2 <= self.x1 <= char.x2 + char.x_velocity or char.x2 <= self.x1 and self.x1 + self.x_velocity <= char.x2 + char.x_velocity)
			and char.y1 < self.y2  + self.y_velocity 
			and char.y2 > self.y1 + self.y_velocity):

				char.is_colliding_x, self.is_colliding_x = True, True

				self.x_velocity *= -1.05
				self.y_velocity += 0.1 * char.y_velocity

				self.hitcount += 1
				print(self.hitcount, 'hits')
				# print('ping' + str(selfs.index(self)))

			#left of self
			if ((char.x1 >= self.x2 >= char.x1 + char.x_velocity or char.x1 >= self.x2 and self.x2 + self.x_velocity >= char.x1 + char.x_velocity)
			and char.y1 + char.y_velocity < self.y2  + self.y_velocity 
			and char.y2 + char.y_velocity > self.y1 + self.y_velocity):

				# print('ding' + str(selfs.index(self)))
				self.x_velocity *= -1.05
				self.y_velocity += 0.1 * char.y_velocity


				self.hitcount += 1
				#print(self.hitcount, 'hits')

			#top of self
			if ((char.y2 + char.y_velocity >= self.y1 >= char.y2 or char.y2 + char.y_velocity >= self.y1 + self.y_velocity and self.y1 >= char.y2)
			and char.x2 + char.x_velocity > self.x1 + self.x_velocity 
			and char.x1 + char.x_velocity < self.x2 + self.x_velocity):

				try:
					self.y_velocity *= -2 * abs(char.y_velocity)/char.y_velocity * -1
				except ZeroDivisionError:
					self.y_velocity *= -2
				self.hitcount += 1

				#print(self.hitcount, 'hits')

				self.ignore_bongs = True
				

			#bottom of self
			if ((char.y1 + char.y_velocity <= self.y2 <= char.y1 or char.y1 + char.y_velocity <= self.y2 + self.y_velocity and self.y2 <= char.y1)
			and char.x2 + char.x_velocity > self.x1 + self.x_velocity 
			and char.x1 + char.x_velocity < self.x2 + self.x_velocity):

				char.is_colliding_y, self.is_colliding_y = True, True
				try:
					self.y_velocity *= -2 * abs(char.y_velocity)/char.y_velocity * -1
				except ZeroDivisionError:
				 	self.y_velocity *= -2
				self.ignore_bongs = True

	def limitvelocity(self, max_xvel, max_yvel):

		if abs(self.x_velocity) > max_xvel:
			self.x_velocity = max_xvel * (abs(self.x_velocity) / self.x_velocity)

		if abs(self.y_velocity) > max_yvel:
			self.y_velocity = max_yvel * (abs(self.y_velocity) / self.y_velocity)


	def update_score(self, chars, bars):

		if self.x1 < 0:
			chars[0].score += 1
			print('score:', chars[0].score, ':', chars[1].score)
			if chars[0].score >=  5:
				chars[1].color = main.green
				bars[0].color = main.green
				print('Left player wins!')
				return False, True
			return False, False


		elif self.x2 > self.framewidth:
			chars[1].score += 1
			print('score:', chars[0].score, ':', chars[1].score)
			if chars[1].score >=  main.max_score:
				chars[0].color = main.green
				bars[1].color = main.green
				print('Right player wins!')
				return False, True
			return False, False
		return True, False


	def draw(self):
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glTranslate(self.x1, self.y1, 0)
		glBegin(GL_QUADS)
		glColor(*self.color)
		glVertex(0, 0, 0)
		glVertex(self.width, 0, 0)
		glVertex(self.width, self.height, 0)
		glVertex(0, self.height, 0)
		glEnd()

class WallBoxario():

	def __init__(self, p1, p2, color, x_velocity, y_velocity, lcollision = True, rcollision = True, tcollision = True, bcollision = True):
		self.lcollision = lcollision
		self.rcollision = rcollision
		self.tcollision = tcollision
		self.bcollision = bcollision

		if self.lcollision and self.rcollision and self.tcollision and self.bcollision:
			self.collisionkill = True
		else:
			self.collisionkill = False

		self.x1 = p1[0]
		self.y1 = p1[1]
		self.x2 = p2[0]
		self.y2 = p2[1]
		self.dead = False

		#print('wall = (', self.x1, ',', self.y1, ') (', self.x2, ',', self.y2, ')')
		self.color = color
		self.is_collidng_x = False
		self.is_collidng_y = False

		self.width = self.x2 - self.x1
		self.height = self.y2 - self.y1

		self.x_velocity = x_velocity
		self.y_velocity = y_velocity

	def updatepos(self):
		self.x1 += self.x_velocity
		self.x2 += self.x_velocity
		self.y1 += self.y_velocity
		self.y2 += self.y_velocity
	


	def draw(self):
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glTranslate(self.x1, self.y1, 0)
		glBegin(GL_QUADS)
		glColor(*self.color)
		glVertex(0, 0, 0)
		glVertex(self.width, 0, 0)
		glVertex(self.width, self.height, 0)
		glVertex(0, self.height, 0)
		glEnd()




