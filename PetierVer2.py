#from _typeshed import Self
from Tkinter import * #in python3 tkinter; python2 Tkinter
import tkFont # also a fix for python3
import serial
from PeltierBoard import PeltierBoard
import time
import datetime
import keyboard
import threading

class Peltier_Control(Frame):			 
	def __init__(self, master=None):
		self.peltier = PeltierBoard(1)

		self.peltier.disable_roc_limit()
		self.roc_limited = False
		#print 
		self.peltier.read_line()
		
		self.started=False
		self.red_on=False
		self.green_on=False
		self.streaming=False
		Frame.__init__(self, master)  
		self.grid()
				
		self.createWidgets()

	def createWidgets(self):
		uni_image = PhotoImage(file="C:/Users/Administrator/Downloads/project/PeltierControlDemoOriginal/PeltierControlDemoOriginal/res/Uni.png")		
	#	uni_image = PhotoImage(file="res/Uni.png")
		self.image_label = Label(image=uni_image)
		self.image_label.uni_image = uni_image
		self.image_label.grid(sticky=N)

		self.temp_label = Label(self, text="***  Enter temperatures in tenths of 1C  ***\n e.g. 35C = 350\n", font=tkFont.Font(family="Helvetica", weight="bold", size=15))
		self.temp_label.grid(column=1, row=1, columnspan=4)
		#self.temp_label.focus_set()       ####
		#self.temp_label.pack()
		self.temp_label.bind("<Key>",self.func)
	
		self.p1_label = Label(self, text='Channel 1')
		self.p1_label.grid(column=1, row=2)
		self.p1_temp = Entry(self, width=4)
		self.p1_temp.grid(column=2, row=2)
		self.p1_button = Button(self, text='Set', command=self.do_temp1_button)
		self.p1_button.grid(column=3, row=2, padx=10)
		self.p1_disable = Button(self, text='Disable', command=self.do_disable_1)
		self.p1_disable.grid(column=4, row=2)
		
		self.p2_label = Label(self, text='Channel 2')
		self.p2_label.grid(column=1, row=3)
		self.p2_temp = Entry(self, width=4)
		self.p2_temp.grid(column=2, row=3)
		self.p2_button = Button(self, text='Set', command=self.do_temp2_button)
		self.p2_button.grid(column=3, row=3, padx=10)
		self.p2_disable = Button(self, text='Disable', command=self.do_disable_2)
		self.p2_disable.grid(column=4, row=3)
		
		self.quitButton = Button (self, text='Quit', command=self.quit_control)	   
		self.quitButton.grid(column=1, row=12, sticky=W)   
		
		self.timebutton = Button (self, text="printTime",command=self.printtime)   
		self.timebutton.grid(column=2, row=6, sticky=W) 
		#self.timebutton.bind("<Key>",self.printtime)     a failed function for binding the key event
		
		
		self.heatbutton = Button (self, text="heat",command=self.do_heat)   #try to heat the pump automatically
		self.heatbutton.grid(column=2, row=18, sticky=W) 


	def func(self):   #######it's a test function for .bind()
		print("event.char =", self.char)
		print("event.keycode =", self.keycode)	
    
	def do_heat(self):  #cycle begin
		print("start heating")
		
		self.temp_change(320) #neutral temp 3s
		time.sleep(3)

		print("3 degree up")
		self.temp_change(350) #3 degree up 5s
		time.sleep(5)

		print("back to neutral")
		self.temp_change(320) #neutral temp 3s
		time.sleep(3)

		print("3 degree down")
		self.temp_change(290) #3 degree dowm 3s
		time.sleep(3)

		print("back to neutral")
		self.temp_change(320) #neutral temp 3s
		time.sleep(3)

		self.do_disable_1()

	def temp_change(self,num):   #a convenient way to control the temp in 1 line
		temp = self.peltier.convert(num) 
		self.peltier.set_temp(1, temp)
		self.peltier.read_line()

	def do_temp1_button(self):
		temp = self.peltier.convert(self.p1_temp.get())
		self.peltier.set_temp(1, temp)
		#print 
		print(self.peltier.read_line())  #"Copyright 2017 SAMH Engineering Services "
		print(self.peltier.get_channel_temp(1))
		#self.peltier.set_temp(3, temp)
	
	def do_temp2_button(self):
		temp = self.convert(self.p2_temp.get())
		self.peltier.set_temp(2, temp) 						# NEED TO CHANGE THIS BACK TO 2
		#print 
		self.peltier.read_line()
#		self.peltier.set_temp(2, temp)
		print(self.peltier.read_line())
		
	
		
	def get_temp1_button(self):
		self.comething = ""
		
	def do_disable_1(self):
		self.peltier.disable_channel(1)
		#print 
		self.peltier.read_line()
		#print "Disable 1"
		
	def do_disable_2(self):
		self.peltier.disable_channel(2)
		#print 
		self.peltier.read_line()
		#print "Disable 2"
		
	
				
	def stream_data(self):
#		if self.streaming==False:
#			self.streaming=True
#		self.peltier.stream_num_readings(10)
		if not self.roc_limited:
			self.roc_limited = True
			self.peltier.enable_roc_limit()
		elif self.roc_limited:
			self.roc_limited = False
			self.peltier.disable_roc_limit()
		#print 
		self.peltier.read_line()
				
			
	def quit_control(self):
		self.peltier.close()
		self.quit() 

	def printtime(self):
		stamp=datetime.datetime.now()
		print (stamp)



app = Peltier_Control()					
app.master.title("test code version2")

app.mainloop() 

""" keyboard.hook(app.printtime)
keyboard.wait() """