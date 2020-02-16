__version__ = 1.0

 
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, Ellipse
import kivy.graphics.vertex_instructions
import random
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import time
from kivy.core.audio import SoundLoader,Sound
from kivy.storage.jsonstore import JsonStore
from os.path import join 
from kivy.uix.scatter import ScatterPlane 
import math

from jnius import autoclass
from kivy.utils import platform


from kivy.config import Config
if platform == 'android':
	PythonActivity=autoclass("org.renpy.android.PythonActivity")
	AdBuddiz = autoclass("com.purplebrain.adbuddiz.sdk.AdBuddiz")

Config.set('graphics','width','800')
Config.set('graphics','height','600')
Config.write()
Window.clearcolor = (0.2,0.5,0.5,1.) 

colours_list = []
colours_list.append((0,0,0,1))
colours_list.append((0,0,1,1))
colours_list.append((0,1,1,1))
colours_list.append((1,1,1,1))
colours_list.append((0,1,0,1))
colours_list.append((1,0,0,1))
colours_list.append((1,0,1,1))
colours_list.append((1,1,0,1))
counter = 0

#music = SoundLoader.load('Faster_Does_It.mp3')
#musicPos = music.get_pos()
#music.play()

done  = False
#Interface for the circle
class EllipseMake(Widget):
	def __init__(self, **kwargs):
		super(EllipseMake, self).__init__(**kwargs)
		
		self.r_col = random.choice(colours_list)
		self.r = self.r_col[0]
		self.g = self.r_col[1]
		self.b = self.r_col[2]
		self.a = self.r_col[3]
		
		with self.canvas.before:
			Color(self.r,self.g,self.b,self.a)
			self.rect = Ellipse(pos=self.pos,size=self.size)
			self.bind(pos=self.update_graphics_pos)
			self.x = self.center_x
			self.y = self.center_y
			self.pos = (self.x,self.y)
			self.rect.pos = self.pos
			self.bind(size= self.setSize)

	def update_graphics_pos(self, instance, value):
		self.rect.pos = value
	def setSize(self, width, height):
		self.size = (self.width, self.height)
		self.rect.size = self.size
	def get_rgb(self):
		return self.r,self.g,self.b

#Interface for the colour options
class ColourChoose(Widget):
	def __init__(self, i, **kwargs):
		super(ColourChoose, self).__init__(**kwargs)
		self.colour = colours_list[i]
		self.r = self.colour[0]
		self.g = self.colour[1]
		self.b = self.colour[2]
		self.a = self.colour[3]
		with self.canvas.after:
			Color(self.r,self.g,self.b,self.a)
			self.rect = Rectangle(pos=self.pos,size=self.size)
			self.bind(pos=self.update_graphics_pos)
			self.x = self.center_x
			self.y = self.center_y
			self.pos = (self.x,self.y)
			self.rect.pos = self.pos
			self.bind(size= self.setSize)

	def update_graphics_pos(self, instance, value):
		self.rect.pos = value
	def setSize(self, width, height):
		self.size = (self.width, self.height)
		self.ratio_x = Window.width/self.width
		self.ratio_y = Window.height/self.height
		self.width = Window.width/self.ratio_x
		self.height = Window.height/self.ratio_y
		self.size = (self.width,self.height)
		self.rect.size = self.size
		
	def get_rgb(self):
		return self.r,self.g,self.b

class Music():
	def __init__(self):
		self.mu = SoundLoader.load('Faster_Does_It.mp3')
		self.musicPos = 0

music = Music()
music.mu.play()


class TitleGui(Widget):
	
	def __init__(self, **kwargs):
		super(TitleGui, self).__init__(**kwargs)
		self.startTime = time.time()
		self.moveDist = Window.width/2 +50
		#self.moveDist = 50
		self.shape_list = []
		for i in range(10):
			self.circle = EllipseMake()
			if Window.width + Window.height >=2500:
				self.circle.width = self.circle.width *2
				self.circle.height = self.circle.height *2
				self.circle.x = (Window.width/2 - self.circle.width/2) + i* self.moveDist
			else:
				self.circle.x = (Window.width/2 - self.circle.width/2) + i* self.moveDist
			self.circle.y = Window.height/2
			self.add_widget(self.circle)
			self.shape_list.append(self.circle)

		self.curr = 0
		self.end  = len(self.shape_list)-1
		Clock.schedule_interval(self.ani_timer, 1)
		self.temp = self.end/2


	def ani_timer(self,dt):

		if self.shape_list[self.end].x < 0:
			for i in range(0,len(self.shape_list)):
					self.shape_list[i].x = Window.width + i * self.moveDist

		for i in self.shape_list:

			anima=Animation(x=i.x - self.moveDist, duration=1)
			anima.start(i)
	
	def playMusic(self, state):
		music.mu.MusicPos = music.mu.get_pos()
		if state == 'down':
			music.mu.stop()
		else:
			music.mu.seek(music.mu.MusicPos)
			music.mu.play()
		print(music.mu.MusicPos)
	
class GUI(Widget):
	def __init__(self, **kwargs):
		super(GUI, self).__init__(**kwargs)
		self.LoadStuff()
		
	def on_touch_down(self, touch):

		if self.touch == True:
			for c in self.color_choice:
				if c.collide_point(touch.x, touch.y):
					if c.get_rgb() == self.shape_list[self.objective].get_rgb():
						self.playSound(self.blop)
						
						self.start = True
						self.correct = True
						self.addScore()

						#self.newBalls();
						
						ran = random.randint(0,10)
						length = len(self.shape_list)

						#More likely to move to middle if current is less than half
						if self.currentColour <= length / 2:
							if self.currentColour == 0:
								self.moveLeft()
								
							elif self.currentColour == length -1:
								self.moveRight()
								
							elif ran >=4:
								self.moveLeft()
								
							elif ran <4:
								self.moveRight()
								
						#More likely to move to the middle if the current is more than half
						elif self.currentColour > length / 2:
							if self.currentColour == length-1:
								self.moveRight()
								
							elif self.currentColour == 0:
								self.moveLeft()
								
							elif ran >=4:
								self.moveRight()
								
							elif ran <4:
								self.moveLeft()

						
						self.new_ran = random.randint(0,1)
						
						#Determine what the current objective is
						if self.new_ran ==0:
							self.objective = self.currentColour
							self.parent.ids['arrow'].source = self.arrow_down
						else:
							self.objective = self.prevColour
							if self.currentColour> self.prevColour:
								self.parent.ids['arrow'].source = self.arrow_left
							else:
								
								self.parent.ids['arrow'].source = self.arrow_right
						
					else:
						self.over = True
						self.LoseAnim()
						Clock.unschedule(self.timerfunc)
						
		if self.parent.ids['restart'].collide_point(touch.x, touch.y):

			self.LoseAnim()
			self.newGame()

		if self.parent.ids['home'].collide_point(touch.x, touch.y):
			
			self.parent.parent.current = 'title'
			self.parent.parent.transition.direction = 'up'
			self.newGame()
			
	#moves the circles left
	def moveLeft(self):
		self.currentColour +=1
		self.prevColour = self.currentColour-1
		self.touch = False
		for i in self.shape_list:
			anim=Animation(x=i.x - self.moveDist, duration=self.animDur)
			anim.bind(on_complete=self.ani_complete)
			anim.start(i)

	#moves the circles right
	def moveRight(self):
		self.currentColour -=1
		self.prevColour = self.currentColour +1
		self.touch = False
		for i in self.shape_list:
			anim=Animation(x=i.x + self.moveDist, duration=self.animDur)
			anim.bind(on_complete=self.ani_complete)
			anim.start(i)

	def timerfunc(self, dt):
		finish = time.time()
		#allows countdown
		if self.correct:
			self.startTime = finish
		elif self.start == True:
			seconds = (self.countdownLimit-(finish-self.startTime))
			if (seconds > 2.9 and seconds <=3.1) or (seconds > 1.9 and seconds <2.1) or (seconds > 0.9 and seconds <1.1):
				self.parent.ids['countdown'].font_size = '60sp'
			else:
				self.parent.ids['countdown'].font_size = '30sp'

			#Lose if time reaches zero
			if seconds <=0:
				self.noTime = True
				Clock.unschedule(self.timerfunc)
				seconds =0
				self.over = True
				self.LoseAnim()
				
			timer= "%.1f" % (round(seconds,2))
			self.parent.ids['countdown'].text = str(timer)

		#Decreases timer, the higher the score
		
		if self.score % 5 == 0 and self.score !=0:	
			if not self.score in self.scorelist:
				if self.countdownLimit >= self.limit:
					self.countdownLimit = self.countdownLimit - 0.2
				self.scorelist.append(self.score)

		self.correct = False

	#Doesn't allow touch until animation is complete
	def ani_complete(self,animation, widget):
		self.touch = True

	#Adding score and updating label
	def addScore(self):
		self.score +=1
		self.parent.ids['a'].text = 'Score: ' + str(self.score)

	#Makes a new game
	def newGame(self):
		self.clearScreen()
		self.resetLabels()
		self.LoadStuff()
		self.over = False

	#Puts labels to their default
	def resetLabels(self):
		self.parent.ids['a'].text = 'Score: ' +str(0)
		self.parent.ids['arrow'].source = self.arrow_down
		self.high.text = ''
		self.parent.ids['countdown'].text = str(self.countdownLimit)
		if self.gameOverWidget:
			self.gameOverWidget[0].text = ''
			self.gameOverWidget[1].text = ''

	#Removes the widgets
	def clearScreen(self):
		for i in self.shape_list:
			self.remove_widget(i)
		for i in self.color_choice:
			self.remove_widget(i)

	def newBalls(self):
		self.circle = EllipseMake()
		if Window.width + Window.height >=2500:
			self.circle.width  = self.circle.width *2
			self.circle.height = self.circle.height *2
		self.circle.x = self.shape_list[len(self.shape_list)-1].x + self.moveDist
		self.circle.y = Window.height/2
						
		self.add_widget(self.circle)
		self.shape_list.append(self.circle)

	def LoadStuff(self):
		self.scorelist  = []
		self.limit = 0.5
		self.blop = SoundLoader.load('blop.wav')
		#Loading images
		self.arrow_right = 'arrow_right.png'
		self.arrow_down = 'arrow_down.png'
		self.arrow_left = 'arrow_left.png'


		#store high score
		self.store = JsonStore('highScore.json')

		self.font_size = 50

		#storing widgets and objects
		self.shape_list = []
		self.color_choice = []
		self.gameOverWidget = []
	
		#Holds the spacing and positions for widgets
		self.pos_x = Window.width/2 
		self.pos_y = Window.height/2
		self.starting_height = random.randint(0,200)
		self.moveDist = self.pos_x + 50

		self.width_ratio = float(Window.width)/800.
		self.height_ratio = float(Window.height)/600.

		self.b = math.floor(float(Window.width + Window.height)/ float(800 + 600))
		print(self.b)
	
		self.menuWidth = 100 *self.b 
		self.menuHeight = 75 *self.b

		#For higher resolution
		if Window.width + Window.height >=2500:
			self.moveDist *=2
			self.font_size *=2

		#Make circles with equal spacing and different starting height
		for i in range(10):
			self.circle = EllipseMake()
			if Window.width + Window.height >=2500:
				self.circle.width = self.circle.width *2
				self.circle.height = self.circle.height *2
				self.circle.x = (self.pos_x - self.circle.width/2) + i* self.moveDist
			else:
				#self.circle.x = (self.pos_x - self.circle.width/2) + i* self.moveDist
				self.circle.x = (self.pos_x - self.circle.width/2) + i* self.moveDist
			self.circle.y = Window.height + self.starting_height
			self.add_widget(self.circle)
			self.shape_list.append(self.circle)
			self.starting_height = random.randint(0,200)

		#falling to start animation
		for i in self.shape_list:
			anim=Animation(y=self.pos_y, t='out_bounce',duration=2)
			anim.start(i)


		#Draw the colour options
		self.counter = 0
		for i in range(len(colours_list)):
			self.rect = ColourChoose(i=i)
			if i >= len(colours_list) / 2:
				self.rect.x = ((Window.width/14)*2)  + self.counter * Window.width/5 
				self.rect.y = Window.height/9
				self.counter +=1
			else:
				self.rect.x = ((Window.width/14)*2)  + i * Window.width/5 
				self.rect.y = Window.height/4

			self.rect.size = (self.menuWidth,self.menuHeight)
			self.add_widget(self.rect)
			self.color_choice.append(self.rect)

		#Determine what circle is the objective
		self.currentColour = 0
		self.prevColour = 0
		self.objective =0
		self.score = 0

		self.animDur = 0.2
				
		self.correct = False
		self.over = False
		self.start = False
		self.touch = True
		self.noTime = False
		
		
		self.l=Label(text='',center=(Window.width/2, Window.height/2), 
					font_size=70, font_name ='AldotheApache')

		self.high=Label(text='',center=(Window.width/2, Window.height/4), 
					font_size=70, font_name ='AldotheApache')

		self.add_widget(self.l)
		self.gameOverWidget.append(self.l)				
		self.add_widget(self.high)
		self.gameOverWidget.append(self.high)

		self.countdownLimit = 3.00
		self.startTime = time.time()
		Clock.schedule_interval(self.timerfunc, 1/60)

	def LoseAnim(self):
		#Falling down animation
		for i in self.shape_list:
			ran_s =random.randint(0,1000)
			anim=Animation(y=0-i.height - ran_s, t='in_out_back',duration=1)
			anim.start(i)
			if i.y <0:
				self.remove_widget(i)

		for i in self.color_choice:
			ran_s =random.randint(100,1000)
			anim=Animation(y=0-i.height - ran_s, t='in_out_back', duration=1)
			anim.start(i)
			if i.y <0:
				self.remove_widget(i)

		#Update high score
		if self.over:
			if self.noTime:
				self.l.text = 'Ran out of time...'
			else:
				self.l.text = 'Wrong colour...'
			if self.store.exists('score') == False:
				self.store.put('score', best=self.score)
				self.high.text = 'Best: ' +str(self.store.get('score')['best'])
			elif self.store.get('score')['best'] < self.score:
				self.store.put('score', best=self.score)
				self.high.text = 'New best: ' +str(self.store.get('score')['best'])
			else:
				self.high.text = 'Best: ' +str(self.store.get('score')['best'])
			
	def playSound(self, sound):
		if sound:
			sound.volume = 1
			sound.pitch = .5
			sound.play()

class ShapeGame(Widget):
	def __init__(self, **kwargs):
		super(ShapeGame, self).__init__(**kwargs)
		self.LoadStuff()
		
	def on_touch_down(self, touch):

		if self.touch == True:
			for c in self.color_choice:
				if c.collide_point(touch.x, touch.y):
					print('hello')
					print(c.source)
					if c.source == self.shape_list[self.objective].source:
						self.playSound(self.blop)
						
						self.start = True
						self.correct = True
						self.addScore()
						
						ran = random.randint(0,10)
						length = len(self.shape_list)

						#More likely to move to middle if current is less than half
						if self.currentColour <= length / 2:
							if self.currentColour == 0:
								self.moveLeft()
								
							elif self.currentColour == length -1:
								self.moveRight()
								
							elif ran >=4:
								self.moveLeft()
								
							elif ran <4:
								self.moveRight()
								
						#More likely to move to the middle if the current is more than half
						elif self.currentColour > length / 2:
							if self.currentColour == length-1:
								self.moveRight()
								
							elif self.currentColour == 0:
								self.moveLeft()
								
							elif ran >=4:
								self.moveRight()
								
							elif ran <4:
								self.moveLeft()

						
						self.new_ran = random.randint(0,1)
						
						#Determine what the current objective is
						if self.new_ran ==0:
							self.objective = self.currentColour
							self.parent.ids['arrow'].source = self.arrow_down
						else:
							self.objective = self.prevColour
							if self.currentColour> self.prevColour:
								self.parent.ids['arrow'].source = self.arrow_left
							else:
								
								self.parent.ids['arrow'].source = self.arrow_right
						
					else:
						self.over = True
						self.LoseAnim()
						Clock.unschedule(self.timerfunc)
						
		if self.parent.ids['restart'].collide_point(touch.x, touch.y):

			self.LoseAnim()
			self.newGame()

		if self.parent.ids['home'].collide_point(touch.x, touch.y):
			
			self.parent.parent.current = 'title'
			self.parent.parent.transition.direction = 'up'
			self.newGame()
			
	#moves the circles left
	def moveLeft(self):
		self.currentColour +=1
		self.prevColour = self.currentColour-1
		self.touch = False
		for i in self.shape_list:
			anim=Animation(x=i.x - self.moveDist, duration=self.animDur)
			anim.bind(on_complete=self.ani_complete)
			anim.start(i)

	#moves the circles right
	def moveRight(self):
		self.currentColour -=1
		self.prevColour = self.currentColour +1
		self.touch = False
		for i in self.shape_list:
			anim=Animation(x=i.x + self.moveDist, duration=self.animDur)
			anim.bind(on_complete=self.ani_complete)
			anim.start(i)

	def timerfunc(self, dt):
		finish = time.time()
		#allows countdown
		if self.correct:
			self.startTime = finish
		elif self.start == True:
			seconds = (self.countdownLimit-(finish-self.startTime))
			if (seconds > 2.9 and seconds <=3.1) or (seconds > 1.9 and seconds <2.1) or (seconds > 0.9 and seconds <1.1):
				self.parent.ids['countdown'].font_size = '60sp'
			else:
				self.parent.ids['countdown'].font_size = '30sp'

			#Lose if time reaches zero
			if seconds <=0:
				self.noTime = True
				Clock.unschedule(self.timerfunc)
				seconds =0
				self.over = True
				self.LoseAnim()
				
			timer= "%.1f" % (round(seconds,2))
			self.parent.ids['countdown'].text = str(timer)

		#Decreases timer, the higher the score
		
		if self.score % 5 == 0 and self.score !=0:	
			if not self.score in self.scorelist:
				if self.countdownLimit >= self.limit:
					self.countdownLimit = self.countdownLimit - 0.2
				self.scorelist.append(self.score)

		self.correct = False

	#Doesn't allow touch until animation is complete
	def ani_complete(self,animation, widget):
		self.touch = True

	#Adding score and updating label
	def addScore(self):
		self.score +=1
		self.parent.ids['a'].text = 'Score: ' + str(self.score)

	#Makes a new game
	def newGame(self):
		self.clearScreen()
		self.resetLabels()
		self.LoadStuff()
		self.over = False

	#Puts labels to their default
	def resetLabels(self):
		self.parent.ids['a'].text = 'Score: ' +str(0)
		self.parent.ids['arrow'].source = self.arrow_down
		self.high.text = ''
		self.parent.ids['countdown'].text = str(self.countdownLimit)
		if self.gameOverWidget:
			self.gameOverWidget[0].text = ''
			self.gameOverWidget[1].text = ''

	#Removes the widgets
	def clearScreen(self):
		for i in self.shape_list:
			self.remove_widget(i)
		for i in self.color_choice:
			self.remove_widget(i)

	def LoadStuff(self):
		self.scorelist  = []
		self.limit = 0.5
		self.blop = SoundLoader.load('blop.wav')
		#Loading images
		self.arrow_right = 'arrow_right.png'
		self.arrow_down = 'arrow_down.png'
		self.arrow_left = 'arrow_left.png'
		
		
		self.circle = Image(source='circle.png')
		self.triangle = Image(source='triangle.png')
		self.square = Image(source='square.png')
		self.rhombus = Image(source='rhombus.png')
		self.trapezium = Image(source='trapezium.png')
		self.pentagon = Image(source='pentagon.png')
		self.hexagon = Image(source='hexagon.png')
		self.octagon = Image(source='octagon.png')
		
		self.circle1 = Image(source='circle.png')
		self.triangle1 = Image(source='triangle.png')
		self.square1 = Image(source='square.png')
		self.rhombus1 = Image(source='rhombus.png')
		self.trapezium1 = Image(source='trapezium.png')
		self.pentagon1 = Image(source='pentagon.png')
		self.hexagon1 = Image(source='hexagon.png')
		self.octagon1 = Image(source='octagon.png')
		
		
		#store high score
		self.store = JsonStore('highScore.json')

		self.font_size = 50

		#storing widgets and objects
		self.shape_list = []
		self.color_choice = []
		self.gameOverWidget = []
		
		self.shape_list.append(self.triangle)
		self.shape_list.append(self.circle)
		self.shape_list.append(self.square)
		self.shape_list.append(self.rhombus)
		self.shape_list.append(self.trapezium)
		self.shape_list.append(self.pentagon)
		self.shape_list.append(self.hexagon)
		self.shape_list.append(self.octagon)
		
		self.color_choice.append(self.triangle1)
		self.color_choice.append(self.circle1)
		self.color_choice.append(self.square1)
		self.color_choice.append(self.rhombus1)
		self.color_choice.append(self.trapezium1)
		self.color_choice.append(self.pentagon1)
		self.color_choice.append(self.hexagon1)
		self.color_choice.append(self.octagon1)
	
		#Holds the spacing and positions for widgets
		self.pos_x = Window.width/2 
		self.pos_y = Window.height/2
		self.starting_height = random.randint(0,200)
		self.moveDist = self.pos_x + 50

		self.width_ratio = float(Window.width)/800.
		self.height_ratio = float(Window.height)/600.

		self.b = math.floor(float(Window.width + Window.height)/ float(800 + 600))
		print(self.b)
	
		self.menuWidth = 100 *self.b 
		self.menuHeight = 75 *self.b

		#For higher resolution
		if Window.width + Window.height >=2500:
			self.moveDist *=2
			self.font_size *=2

		#Make circles with equal spacing and different starting height
		for i in range(len(self.shape_list)):
			if Window.width + Window.height >=2500:
				self.shape_list[i].width = self.shape_list[i].width *2
				self.shape.list[i].height = self.shape_list[i].height *2
				self.shape_list[i].x = (self.pos_x - self.shape_list[i].width/2) + i* self.moveDist
			else:
				self.shape_list[i].x = (self.pos_x - self.shape_list[i].width/2) + i* self.moveDist
			
			self.shape_list[i].y = Window.height + self.starting_height
			self.add_widget(self.shape_list[i])
			self.starting_height = random.randint(0,200)

		#falling to start animation
		for i in self.shape_list:
			anim=Animation(y=self.pos_y, t='out_bounce',duration=2)
			anim.start(i)
				
		#Draw the colour options
		self.counter = 0
		for i in range(len(self.color_choice)):
			if i >= len(self.color_choice) / 2:
				self.color_choice[i].x = ((Window.width/14)*2)  + self.counter * Window.width/5
				self.color_choice[i].y = Window.height/9
				self.counter +=1
			else:
				self.color_choice[i].x = ((Window.width/14)*2)  + i * Window.width/5 
				self.color_choice[i].y = Window.height/4
			
			self.color_choice[i].size = (self.menuWidth,self.menuHeight)
			self.add_widget(self.color_choice[i])
	

		#Determine what circle is the objective
		self.currentColour = 0
		self.prevColour = 0
		self.objective =0
		self.score = 0

		self.animDur = 0.2
				
		self.correct = False
		self.over = False
		self.start = False
		self.touch = True
		self.noTime = False
		
		
		self.l=Label(text='',center=(Window.width/2, Window.height/2), 
					font_size=70, font_name ='AldotheApache')

		self.high=Label(text='',center=(Window.width/2, Window.height/4), 
					font_size=70, font_name ='AldotheApache')

		self.add_widget(self.l)
		self.gameOverWidget.append(self.l)				
		self.add_widget(self.high)
		self.gameOverWidget.append(self.high)

		self.countdownLimit = 3.00
		self.startTime = time.time()
		Clock.schedule_interval(self.timerfunc, 1/60)

	def LoseAnim(self):
		#Falling down animation
		for i in self.shape_list:
			ran_s =random.randint(0,1000)
			anim=Animation(y=0-i.height - ran_s, t='in_out_back',duration=1)
			anim.start(i)
			if i.y <0:
				self.remove_widget(i)

		for i in self.color_choice:
			ran_s =random.randint(100,1000)
			anim=Animation(y=0-i.height - ran_s, t='in_out_back', duration=1)
			anim.start(i)
			if i.y <0:
				self.remove_widget(i)

		#Update high score
		if self.over:
			if self.noTime:
				self.l.text = 'Ran out of time...'
			else:
				self.l.text = 'Wrong colour...'
			if self.store.exists('score') == False:
				self.store.put('score', best=self.score)
				self.high.text = 'Best: ' +str(self.store.get('score')['best'])
			elif self.store.get('score')['best'] < self.score:
				self.store.put('score', best=self.score)
				self.high.text = 'New best: ' +str(self.store.get('score')['best'])
			else:
				self.high.text = 'Best: ' +str(self.store.get('score')['best'])
			
	def playSound(self, sound):
		if sound:
			sound.volume = 1
			sound.pitch = .5
			sound.play()



			
				
class ScreenManage(ScreenManager):
	pass


class Viewport(ScatterPlane):
    def __init__(self, **kwargs):
        kwargs.setdefault('size', (1920, 1080))
        kwargs.setdefault('size_hint', (None, None))
        kwargs.setdefault('do_scale', False)
        kwargs.setdefault('do_translation', False)
        kwargs.setdefault('do_rotation', False)
        super(Viewport, self).__init__( **kwargs)
        Window.bind(system_size=self.on_window_resize)
        Clock.schedule_once(self.fit_to_window, -1)

    def on_window_resize(self, window, size):
        self.fit_to_window()

    def fit_to_window(self, *args):
        if self.width < self.height: #portrait
            if Window.width < Window.height: #so is window   
                self.scale = Window.width/float(self.width)
            else: #window is landscape..so rotate vieport
                self.scale = Window.height/float(self.width)
                self.rotation = -90
        else: #landscape
            if Window.width > Window.height: #so is window   
                self.scale = Window.width/float(self.width)
            else: #window is portrait..so rotate vieport
                self.scale = Window.height/float(self.width)
                self.rotation = -90

        self.center = Window.center
        for c in self.children:
            c.size = self.size

    def add_widget(self, w, *args, **kwargs):
        super(Viewport, self).add_widget(w, *args, **kwargs)
        w.size = self.size

yo = Builder.load_file("blah.kv")

class blahApp(App):
	#def on_pause(self):
      # Here you can save data if needed
    	#AdBuddiz.showAd(PythonActivity.mActivity)
	#	AdBuddiz.showAd(PythonActivity.mActivity)
	#	return True

	def on_resume(self):
      # Here you can check if any data needs replacing (usually nothing)
		
		pass

	#def on_start(self):
	#	AdBuddiz.setPublisherKey("TEST_PUBLISHER_KEY")
	#	AdBuddiz.setTestModeActive()
	#	AdBuddiz.cacheAds(PythonActivity.mActivity)

	#def show_ads(*args):
	#	AdBuddiz.showAd(PythonActivity.mActivity)

	def build(self):
		
		self.root = Viewport(size=(1080,1920))
		#gui = GUI()
		#ame = secondGame()
		#self.root.add_widget(gui)
		#self.root.add_widget(ame)
        #self.root.add_widget(Factory.Button(text="ViewportApp"))
		#gui = GUI()
		return yo

	#def show_ads(*args):
     #   AdBuddiz.showAd(PythonActivity.mActivity)

if __name__ == '__main__':
	blahApp().run()
