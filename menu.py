import pygame
import math
from entityclass import *
from wallclass import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
import os
from random import *
import numpy as np
from PIL import Image
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (250,50)

display_width = 800
display_height = 600

red, green, blue, black = (1,0,0,1), (0,1,0,1), (0,0,1,1), (0,0,0,1)

button_height, button_width, button_spacing = 100, 500, 50

class Button():
	def __init__(self,p1,p2,color,txt):
		self.x1 = p1[0]
		self.y1 = p1[1]
		self.x2 = p2[0]
		self.y2 = p2[1]

		self.color = color
		self.txt = txt

		self.width = self.x2 - self.x1
		self.height = self.y2 - self.y1
		
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

def defbuttons():
	return [
	Button((display_width/2 - button_width/2, display_height/2 - 1.5*button_height - button_spacing), (display_width/2 + button_width/2, display_height/2 - 0.5*button_height - button_spacing), red, 'boxario'),
	Button((display_width/2 - button_width/2, display_height/2 - 0.5*button_height), (display_width/2 + button_width/2, display_height/2 + 0.5*button_height), green, 'flappybox'),
	Button((display_width/2 - button_width/2, display_height/2 + 0.5*button_height + button_spacing), (display_width/2 + button_width/2, display_height/2 + 1.5*button_height + button_spacing), blue, 'pingpong')
	]

def drawmenu():
	glClear(GL_COLOR_BUFFER_BIT)
	glClear(GL_DEPTH_BUFFER_BIT)

	for button in buttons:
		button.draw()
	
	pygame.display.flip()


if __name__ == '__main__':
	pygame.init()

	gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.DOUBLEBUF | pygame.OPENGL)
	pygame.display.set_caption('test')

	frameInfo = {'frame':gameDisplay, 'framedims':(display_width, display_height)}

	buttons = defbuttons()

	glClearColor(*black)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0, display_width, display_height, 0, -1, 3)

	drawmenu()

	while True:
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					for button in buttons:
						if (button.x1 < event.pos[0] < button.x2
						and button.y1 < event.pos[1] < button.y2):
							print(button.txt)