import random
import time
import pygame, sys
from pygame.locals import *

height = 480
width = 640
size = 8

black = (0, 0, 0)
white = (255, 255, 255)
red = (244, 0, 0)
vel = 10

populationsize = 200
length = 200
mut = 0.1

targetx = width/2
targety = 20
radius = 20

obstacles = [(width/4,height/2,300,10)]

def createPopulation():
	a = []
	for i in range(populationsize):
		b = []
		for j in range(length):
			move = random.randint(0,3)
			b.append(move)
		a.append((citizen(),b))
	return a

def fitness(citizen):
	return (targetx - citizen.x)**2 + (targety - citizen.y)**2 +citizen.x + citizen.y

class citizen(object):
	def __init__(self):
		self.x = width/2
		self.y = height
		self.fit = fitness(self)

	def up(self):
		self.y -= vel

	def down(self):
		self.y += vel

	def left(self):
		self.x -= vel

	def right(self):
		self.x += vel		

def crossover(a,b):
	c = []
	for i in range(length):
		if random.random() <= 0.5:
			c.append(b[i])
		else:
			c.append(a[i])				
	return c

def mutation(c):
	for i in range(length):
		if random.random() <= mut:
			c[i] = random.randint(0,3)

def selction(population):
	prob = random.random()
	pc = 0.2
	total = 1- pc
	for i in range(populationsize-1):
		if prob<=total:
			return population[i][1]
		total = prob*(1-pc)
	
	return population[populationsize-1][1]	

def solve():
	global screen
	pygame.init()
	screen =  pygame.display.set_mode((width,height)) 
	population = createPopulation()
	generations = 0

	while True:
		generations+=1
		for i in range(length):
			screen.fill(black)
			showGenerations(generations)
			drawTarget()
			drawDrawobstacles(obstacles)
			pygame.display.update()
			for j in range(populationsize):
				if isStuck(population[j][0],obstacles):
					draw(population[j][0],j)
					continue
				key = population[j][1][i]
				if key == 0:
					population[j][0].up()
				if key == 1:
					population[j][0].down()
				if key ==  2:
					population[j][0].right()
				if key ==  3:
					population[j][0].left()
				draw(population[j][0],j)				
			pygame.display.update()
			time.sleep(0.01)
				
		for i in range(populationsize):
			if isStuck(population[i][0], obstacles):
				population[i][0].fit = 10000000000
				continue
			population[i][0].fit = fitness(population[i][0])
		population.sort(key = lambda x: x[0].fit)
		print population[0][0].fit

		new_population = []	

		for i in range(populationsize):
			child = crossover(selction(population),selction(population))
			mutation(child)
			new_population.append((citizen(),child))
		population = new_population	

def isStuck(citizen, obstacles):
	for i in obstacles:
		if citizen.x>=i[0] and citizen.x<=i[0]+i[2] and citizen.y<=i[1] and citizen.y>=i[1]-i[3]:
			return True
	return False		

def drawTarget():
	pygame.draw.circle(screen,red,(targetx,targety),radius)

def draw(citizen,j):
	color = (212, 91, 8)
	pygame.draw.rect(screen,color,(citizen.x,citizen.y,10,10))		

def showGenerations(gen):
	text= 'Total Generations : ' + str(gen)
	fontObj = pygame.font.Font('freesansbold.ttf', 20)
	textSurfaceObj = fontObj.render(text, True, white, black)
	textRectObj = textSurfaceObj.get_rect()
	textRectObj.center = (50,20)
	screen.blit(textSurfaceObj, textRectObj)
def drawDrawobstacles(obstacles):
	for i in obstacles:
		pygame.draw.rect(screen,(0,0,200), (i[0],i[1],i[2],i[3]))

solve()