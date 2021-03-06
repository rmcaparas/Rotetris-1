import pygame
from pygame.locals import *

from time import time
from os import path

from random import *
from sprites import Button
from game import *

def load_image(file, colorkey = None):
	surf = pygame.image.load(path.join('resource', file)).convert_alpha()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = surf.get_at((0,0))
		surf.set_colorkey(colorkey, RLEACCEL)
	return surf

pygame.init()
pygame.display.set_caption("Rotetris")
SCR = pygame.display.set_mode((800, 600))
icon = load_image("icon.png")
pygame.display.set_icon(icon)
pygame.font.init()
pygame.key.set_repeat(100, 70)

BG =  load_image("title.png")
#main animation
arrow = load_image("arrow.png")
arrowd = arrow.copy()
arrow_rect = arrow.get_rect()
arrow_rect.center = 209, 150
arrow_timer = time()
arrow_ang = 0
#animation
BGM = pygame.mixer.Sound(path.join('resource', 'music', 'track1.ogg'))
BGM.set_volume(settings["volume"])
BGM.play(-1)

def load_level(diff):
	g = Game(diff, SCR)
	BGM.stop()
	t = Thread(target = g.start)
	g.start()
	BGM.play()
	pygame.event.get()

def change_vol(command):
	command()
	BGM.set_volume(settings["volume"])
class MainObjects():

	def __init__(self, default):
		self.group = default
		self.running = True

	def set(self, group):
		self.group = group

	def get(self):
		return self.group

	def stop(self):
		self.running = False

baseoptions = pygame.sprite.Group()
startoptions = pygame.sprite.Group()
creditsoptions = pygame.sprite.OrderedUpdates()
optionoptions = pygame.sprite.OrderedUpdates()
instructionoptions = pygame.sprite.OrderedUpdates()
mainobject = MainObjects(baseoptions)

clock = pygame.time.Clock()

def start_game(difficulty):
	pass

#Main Menu
start = load_image('Start.png')
startb = Button(start, (400, 250), lambda: mainobject.set(startoptions))

option = load_image("Options.png")
optionb = Button(option, (400, 325), lambda: mainobject.set(optionoptions))

credit = load_image("Credits.png")
creditb = Button(credit, (400, 400), lambda: mainobject.set(creditsoptions))

instruction = load_image("Instructions.png")
instructionb = Button(instruction, (400, 475), lambda: mainobject.set(instructionoptions))

exit = load_image("Exit.png")
exitb = Button(exit, (400, 550), lambda: mainobject.stop())

baseoptions.add(startb, optionb, creditb, instructionb, exitb)
#-------------------------------------
#start menu
easy = load_image("Easy.png")
easyb = Button(easy, (400, 275), lambda: load_level(EASY))

normal = load_image("Normal.png")
normalb = Button(normal, (400, 350), lambda: load_level(NORMAL))

hard = load_image("Hard.png")
hardb = Button(hard, (400, 425), lambda: load_level(HARD))

insane = load_image("Insane.png")
insaneb = Button(insane, (400, 500), lambda: load_level(EXTREME))

back = load_image("Back.png")
backb = Button(back, (100, 565), lambda: mainobject.set(baseoptions))

startoptions.add(easyb, normalb, hardb, insaneb, backb)
#-------------------------------------
#credits
class _CreditsPg(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image("Creditspg.png")
		self.rect = self.image.get_rect()
creditspg = _CreditsPg()

creditsoptions.add(creditspg, backb)
#---------------------------------------
#options
class _OptionsPG(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image("Optionpg.png")
		self.rect = self.image.get_rect()
optionspg = _OptionsPG()

low = load_image("Low.png")
lowb = Button(low, (200, 375), lambda: change_vol(low_vol))

med = load_image("Med.png")
medb = Button(med, (400, 375), lambda: change_vol(med_vol))

high = load_image("High.png")
highb = Button(high, (600, 375), lambda: change_vol(high_vol))

relative = load_image("Relative.png")
relativeb = Button(relative, (200, 175), relative_control)

absolute = load_image("Absolute.png")
absoluteb = Button(absolute, (575, 230), absolute_control)

save = load_image("Save.png")
saveb = Button(save, (700, 565), save_settings)
optionoptions.add(optionspg, lowb, medb, highb, relativeb, absoluteb, backb, saveb)

#---------------------------------------
#instructions
class _InstructionsPG(pygame.sprite.Sprite):
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image("Instructionpage.png")
		self.rect = self.image.get_rect()
instructionspg = _InstructionsPG()

i_start = load_image("Start.png")
i_startb = Button(i_start, (700, 565), lambda: mainobject.set(startoptions))
instructionoptions.add(instructionspg,backb, i_startb)

allsprites = pygame.sprite.Group()

while(mainobject.running):
	clock.tick(60)

	for event in pygame.event.get():
		if event.type == QUIT:
			mainobject.stop()
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				mainobject.set(baseoptions)
		elif event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				clicked = False
				for sp in mainobject.get():
					if isinstance(sp, Button):
						if sp.click():
							clicked = True
							break
				if clicked: break

	if(time() - arrow_timer >= .75):
		arrow_ang += choice([90, 180, 270])
		arrow_ang %= 360
		arrowd = pygame.transform.rotate(arrow, arrow_ang)	
		arrow_rect = arrowd.get_rect()
		arrow_rect.center = 209, 150
		arrow_timer = time()

	SCR.blit(BG, (0, 0))
	SCR.blit(arrowd, arrow_rect)

	allsprites.update()
	mainobject.get().update()

	allsprites.draw(SCR)
	mainobject.get().draw(SCR)
	pygame.display.update()
	
BGM.stop()
pygame.quit()