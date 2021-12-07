#from _typeshed import Self
from Tkinter import * #in python3 tkinter; python2 Tkinter
import tkFont # also a fix for python3
import serial
from PeltierBoard import PeltierBoard
import time
import datetime
import keyboard
import threading
import re

ser = serial.Serial('COM3',9600)
real_time_temp = ser.readline() # a global
toolvariable1 = re.findall(r"\d+\.?\d*",real_time_temp) #filt the number out
toolvariable2 = toolvariable1[-1]
toolvariable3 = float(toolvariable2)*10
real_time_numTemp = int(toolvariable3)    #used in temp change round 2&4


neutral = 320 #32 Degree C just make it as a global
flag = 0   #another global helps the measuring thread

timefile = open('hit-time.txt', 'w+')    #recourd the printtime button in the whole process

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
		#uni_image = PhotoImage(file="./res/Uni.png")
		self.image_label = Label(image=uni_image)
		self.image_label.uni_image = uni_image
		self.image_label.grid(sticky=N)

		self.temp_label = Label(self, text="Thermo feedback experiment version1 \n     \n", font=tkFont.Font(family="Helvetica", weight="bold", size=15))
		self.temp_label.grid(column=1, row=1, columnspan=4)
		#self.temp_label.focus_set()       ####this is something to do with the keyboard event
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
		self.p2_label.grid(column=1, row=4)
		self.p2_temp = Entry(self, width=4)
		self.p2_temp.grid(column=2, row=4)
		self.p2_button = Button(self, text='Set', command=self.do_temp2_button)
		self.p2_button.grid(column=3, row=4, padx=10)
		self.p2_disable = Button(self, text='Disable', command=self.do_disable_2)
		self.p2_disable.grid(column=4, row=4)
		
		self.quitButton = Button (self, text='Quit', command=self.quit_control)	   
		self.quitButton.grid(column=1, row=8, sticky=W)   
		
		self.timebutton = Button (self, text="printTime",command=self.printtime)   
		self.timebutton.grid(column=2, row=8, sticky=W) 
		#self.timebutton.bind("<Key>",self.printtime)     a failed function for binding the key event
		
		self.tempbutton = Button (self, text="start measuring",command=self.start_measure)    
		self.tempbutton.grid(column=3, row=8, sticky=W) 

		self.tempbutton = Button (self, text="stop measuring",command=self.stop_measure)   
		self.tempbutton.grid(column=4, row=8, sticky=W) 
		
		self.heatbutton = Button (self, text="  round1  ",command=self.round1)   #pre-set round 1
		self.heatbutton.grid(column=1, row=6, sticky=W) 

		self.heatbutton = Button (self, text="  round2  ",command=self.round2)   #real-time temp round 1
		self.heatbutton.grid(column=2, row=6, sticky=W) 

		self.heatbutton = Button (self, text="  round3  ",command=self.round3)   #pre-set round 2
		self.heatbutton.grid(column=3, row=6, sticky=W) 

		self.heatbutton = Button (self, text="  round4  ",command=self.round4)   #real-time temp round 2
		self.heatbutton.grid(column=4, row=6, sticky=W) 


	def func(self):   #######it's a test function for .bind()
		print("event.char =", self.char)
		print("event.keycode =", self.keycode)	

#--------------------------------------------------------------------------------------------------------------------------------------  
	def do_heat1(self):  #cycle begin  round1 pre-set normal pace
		f = open('heat1.txt', 'w+')  #round 1 open the file #####
		stamp=time.time()
		timehint=datetime.datetime.now()
		print(timehint,"start round1")
		print >> f, timehint,"start round1"                   #signal

		
		self.temp_change(320)                              #1 neutral temp
		print >> f, stamp,"neutral"  #in file
		print(stamp,"neutral")
		time.sleep(10)
		
		stamp=time.time()
		self.temp_change(350)  
		print >> f, stamp,"3 degree up"  #in file           #01 degree up 5s
		print(stamp,"3 degree up") 
		time.sleep(5)

		stamp=time.time()
		self.temp_change(320)                              #2 neutral temp 
		print >> f, stamp,"back to neutral"  #in file
		print(stamp,"back to neutral")
		time.sleep(10)

		stamp=time.time()
		self.temp_change(290)  
		print >> f, stamp,"3 degree down"  #in file        #02 degree downp 5s
		print(stamp,"3 degree down") 
		time.sleep(5)

		stamp=time.time()
		self.temp_change(320)                              #3 neutral temp 5s
		print >> f, stamp,"back to neutral"  #in file
		print(stamp,"back to neutral")
		time.sleep(10)

		stamp=time.time()
		self.temp_change(350)  
		print >> f, stamp,"3 up"  #in file        #03 degree up
		print(stamp,"3 degree up") 
		time.sleep(5)

		stamp=time.time()
		self.temp_change(320)                              #4 neutral temp 5s
		print >> f, stamp,"back to neutral"  #in file
		print(stamp,"back to neutral")
		time.sleep(10)

		stamp=time.time()
		self.temp_change(350)  
		print >> f, stamp,"3 up"  #in file        #04 degree up 5s
		print(stamp,"3 degree up") 
		time.sleep(5)

		stamp=time.time()
		self.temp_change(320)                              #5 neutral temp 5s
		print >> f, stamp,"back to neutral"  #in file
		print(stamp,"back to neutral")
		time.sleep(10)

		stamp=time.time()
		self.temp_change(290)  
		print >> f, stamp,"3 degree down"  #in file        #05 degree down 5s
		print(stamp,"3 degree down") 
		time.sleep(5)

		stamp=time.time()
		self.temp_change(320)                              #6 neutral temp 5s
		print >> f, stamp,"back to neutral"  #in file
		print(stamp,"back to neutral")
		time.sleep(10)

		stamp=time.time()
		self.temp_change(350)  
		print >> f, stamp,"3 up"  #in file        #06 degree up 5s
		print(stamp,"3 degree up") 
		time.sleep(5)

		stamp=time.time()
		self.temp_change(320)                              #7 neutral temp 5s
		print >> f, stamp,"back to neutral"  #in file
		print(stamp,"back to neutral")
		time.sleep(10)

		stamp=time.time()
		self.temp_change(290)  
		print >> f, stamp,"3 degree down"  #in file        #07 degree down 5s
		print(stamp,"3 degree down") 
		time.sleep(5)

		stamp=time.time()
		self.temp_change(320)                              #8 neutral temp 5s
		print >> f, stamp,"back to neutral"  #in file
		print(stamp,"back to neutral")
		time.sleep(10)

		stamp=time.time()
		self.temp_change(290)  
		print >> f, stamp,"3 degree down"  #in file        #08 degree down 5s
		print(stamp,"3 degree down") 
		time.sleep(5)

		stamp=time.time()
		self.temp_change(320)                              #9 neutral temp 5s
		print >> f, stamp,"back to neutral"  #in file
		print(stamp,"back to neutral")
		time.sleep(10)

		stamp=time.time()
		self.temp_change(350)  
		print >> f, stamp,"3 up"  #in file        #09 degree up 5s
		print(stamp,"3 degree up") 
		time.sleep(5)

		stamp=time.time()
		self.temp_change(320)                              #10 neutral temp 5s
		print >> f, stamp,"back to neutral"  #in file
		print(stamp,"back to neutral")
		time.sleep(10)

		stamp=time.time()
		self.temp_change(290)  
		print >> f, stamp,"3 degree down"  #in file        #10 degree down 5s
		print(stamp,"3 degree down") 
		time.sleep(5)

		timehint=datetime.datetime.now()
		print >> f, timehint,"round 1 end"  
		print(timehint,"round 1 end") 

		self.do_disable_1()
		self.do_disable_2()
		f.close()

#--------------------------------------------------------------------------------------------------------------------------------------
	def do_heat2(self):  #cycle begin  round2 real-time normal pace
		f2 = open('heat2.txt', 'w+')
		stamp=time.time()
		timehint=datetime.datetime.now()
		print(timehint,"start round2")
		print >> f2, timehint,"start round2"
		
		self.real_change_up(0)             #1 skin temp 
		print >> f2, stamp,"skin temp"
		time.sleep(10)

		stamp=time.time()
		print(stamp,"3 degree down")
		self.real_change_up(-30)               #01 degree dowm 3s
		print >> f2, stamp,"3 degree down 5s"
		time.sleep(5)

		stamp=time.time()
		print(stamp,"back to skin temp")
		self.real_change_up(0)                 #2 skin temp 
		print >> f2, stamp,"skin temp"
		time.sleep(10)

		stamp=time.time()
		print(stamp,"3 degree up")
		self.real_change_up(30)               #02 degree up 5s
		print >> f2, stamp,"3 degree up 5s"
		time.sleep(5)

		stamp=time.time()
		print(stamp,"back to skin temp")
		self.real_change_up(0)                 #3 skin temp 
		print >> f2, stamp,"skin temp"
		time.sleep(10)

		stamp=time.time()
		print(stamp,"3 degree down")
		self.real_change_up(-30)                #03 degree dowm 
		print >> f2, stamp,"3 degree down 5s"
		time.sleep(5)

		stamp=time.time()
		print(stamp,"back to skin temp")
		self.real_change_up(0)                  #4 skin temp 
		print >> f2, stamp,"skin temp"
		time.sleep(10)

		stamp=time.time()
		print(stamp,"3 degree down")
		self.real_change_up(-30)                #04 degree dowm 
		print >> f2, stamp,"3 degree down 5s"
		time.sleep(5)

		stamp=time.time()
		print(stamp,"back to skin temp")
		self.real_change_up(0)                   #5 skin temp
		print >> f2, stamp,"skin temp"
		time.sleep(10)

		stamp=time.time()
		print(stamp,"3 degree up")
		self.real_change_up(30)                  #05 degree up 5s
		print >> f2, stamp,"3 degree up 5s"
		time.sleep(5)

		stamp=time.time()
		print(stamp,"back to skin temp")
		self.real_change_up(0)                   #6 skin temp
		print >> f2, stamp,"skin temp"
		time.sleep(10)

		stamp=time.time()
		print(stamp,"3 degree up")
		self.real_change_up(30)                  #06 degree up 5s
		print >> f2, stamp,"3 degree up 5s"
		time.sleep(5)

		stamp=time.time()
		print(stamp,"back to skin temp")
		self.real_change_up(0)                   #7 skin temp
		print >> f2, stamp,"skin temp"
		time.sleep(10)

		stamp=time.time()
		print(stamp,"3 degree down")
		self.real_change_up(-30)                #07 degree dowm 
		print >> f2, stamp,"3 degree down 5s"
		time.sleep(5)

		stamp=time.time()
		print(stamp,"back to skin temp")
		self.real_change_up(0)                   #8 skin temp
		print >> f2, stamp,"skin temp"
		time.sleep(10)

		stamp=time.time()
		print(stamp,"3 degree up")
		self.real_change_up(30)                  #08 degree up 5s
		print >> f2, stamp,"3 degree up 5s"
		time.sleep(5)

		stamp=time.time()
		print(stamp,"back to skin temp")
		self.real_change_up(0)                   #9 skin temp
		print >> f2, stamp,"skin temp"
		time.sleep(10)

		stamp=time.time()
		print(stamp,"3 degree up")
		self.real_change_up(30)                  #09 degree up 5s
		print >> f2, stamp,"3 degree up 5s"
		time.sleep(5)

		stamp=time.time()
		print(stamp,"back to skin temp")
		self.real_change_up(0)                   #10 skin temp
		print >> f2, stamp,"skin temp"
		time.sleep(10)

		stamp=time.time()
		print(stamp,"3 degree down")
		self.real_change_up(-30)                #10 degree dowm 
		print >> f2, stamp,"3 degree down 5s"
		time.sleep(5)
		
		stamp=time.time()
		print(stamp,"back to skin temp and close")
		self.real_change_up(0)                     #6 skin temp 3s
		print >> f2, stamp,"skin temp and close"
		time.sleep(3)

		timehint=datetime.datetime.now()
		print >> f2, timehint,"round 2 end"  
		print(timehint,"round 2 end") 

		self.do_disable_1()
		self.do_disable_2()
		f2.close()

#--------------------------------------------------------------------------------------------------------------------------------------
	def do_heat3(self):  #cycle begin  round1 pre-set normal pace
		f = open('heat3.txt', 'w+')  #round 1 open the file #####
		stamp=time.time()
		timehint=datetime.datetime.now()
		print(timehint,"start round3")
		print >> f, timehint,"start round3"
		

		
		self.temp_change(320)                              #1 neutral temp
		print >> f, stamp,"neutral 8s"  #in file
		print(stamp,"neutral 8s")
		time.sleep(8)
		
		stamp=time.time()
		self.temp_change(260)  
		print >> f, stamp,"6 degree down 3s"  #in file           #01 degree up 5s
		print(stamp,"6 degree down 3s") 
		time.sleep(3)

		stamp=time.time()
		self.temp_change(320)                              #2 neutral temp 
		print >> f, stamp,"back to neutral 8s"  #in file
		print(stamp,"back to neutral 8s")
		time.sleep(8)

		stamp=time.time()
		self.temp_change(360)  
		print >> f, stamp,"4 degree up 4s"  #in file        #02 degree up 4s
		print(stamp,"4 degree up 4s") 
		time.sleep(4)

		stamp=time.time()
		self.temp_change(320)                              #3 neutral temp 6s
		print >> f, stamp,"back to neutral 6s"  #in file
		print(stamp,"back to neutral 6s")
		time.sleep(6)

		stamp=time.time()
		self.temp_change(380)  
		print >> f, stamp,"6 degree up 5s"  #in file        #03 degree up
		print(stamp,"6 degree up 5s") 
		time.sleep(5)

		stamp=time.time()
		self.temp_change(320)                              #4 neutral temp 5s
		print >> f, stamp,"back to neutral 2s"  #in file
		print(stamp,"back to neutral 2s")
		time.sleep(2)

		stamp=time.time()
		self.temp_change(300)  
		print >> f, stamp,"2 down 5s"  #in file        #04 degree up 5s
		print(stamp,"2 down 5s") 
		time.sleep(5)

		stamp=time.time()
		self.temp_change(320)                              #5 neutral temp 5s
		print >> f, stamp,"back to neutral 4s"  #in file
		print(stamp,"back to neutral 4s")
		time.sleep(4)

		stamp=time.time()
		self.temp_change(390)  
		print >> f, stamp,"7 degree up 4s"  #in file        #05 degree down 5s
		print(stamp,"7 degree up 4s") 
		time.sleep(4)

		stamp=time.time()
		self.temp_change(320)                              #6 neutral temp 5s
		print >> f, stamp,"back to neutral 3s"  #in file
		print(stamp,"back to neutral 3s")
		time.sleep(3)

		stamp=time.time()
		self.temp_change(250)  
		print >> f, stamp,"7 degree down 4s"  #in file        #06 degree down
		print(stamp,"7 degree down 4s") 
		time.sleep(4)

		stamp=time.time()
		self.temp_change(320)                              #7 neutral temp 4s
		print >> f, stamp,"back to neutral 4s"  #in file
		print(stamp,"back to neutral 4s")
		time.sleep(4)

		stamp=time.time()
		self.temp_change(340)  
		print >> f, stamp,"2 degree up 5s"  #in file        #07 degree up 5s
		print(stamp,"2 degree up 5s") 
		time.sleep(5)

		stamp=time.time()
		self.temp_change(320)                              #8 neutral temp 5s
		print >> f, stamp,"back to neutral 2s"  #in file
		print(stamp,"back to neutral 2s")
		time.sleep(2)

		stamp=time.time()
		self.temp_change(280)  
		print >> f, stamp,"4 degree down 4"  #in file        #08 degree down 4s
		print(stamp,"4 degree down 4") 
		time.sleep(4)

		stamp=time.time()
		self.temp_change(320)                              #9 neutral temp 3s
		print >> f, stamp,"back to neutral 3"  #in file
		print(stamp,"back to neutral 3")
		time.sleep(3)

		stamp=time.time()
		self.temp_change(370)  
		print >> f, stamp,"5 degree up 5"  #in file        #09 degree up 5s
		print(stamp,"5 degree up 5") 
		time.sleep(5)

		stamp=time.time()
		self.temp_change(320)                              #10 neutral temp 3s
		print >> f, stamp,"back to neutral 3"  #in file
		print(stamp,"back to neutral 3")
		time.sleep(3)

		stamp=time.time()
		self.temp_change(270)  
		print >> f, stamp,"5 degree down 5"  #in file        #10 degree down 5s
		print(stamp,"5 degree down 5") 
		time.sleep(5)

		stamp=datetime.datetime.now()
		self.temp_change(320)                              #10 neutral temp 3s
		print >> f, stamp,"round3 end"  #in file
		print(stamp,"round 3 end")
		time.sleep(3)

		self.do_disable_1()
		self.do_disable_2()
		f.close()
#--------------------------------------------------------------------------------------------------------------------------------------
	def do_heat4(self):  #cycle begin  round4 skin-measured normal pace
			
		f = open('heat4.txt', 'w+')  #round 1 open the file #####
		stamp=time.time()
		timehint=datetime.datetime.now()
		print(timehint,"start round4")
		print >> f, timehint,"start round4"

		
		self.real_change_up(0)                            #1 skin temp
		print >> f, stamp,"skin 8s"  #in file
		print(stamp,"skin 8s")
		time.sleep(8)
		
		stamp=time.time()
		self.real_change_up(-60)  
		print >> f, stamp,"6 degree down 3s"  #in file           #01 6 degree down 3s
		print(stamp,"6 degree down 3s") 
		time.sleep(3)

		stamp=time.time()
		self.real_change_up(0)                              #2 neutral temp 
		print >> f, stamp,"back to neutral 8s"  #in file
		print(stamp,"back to neutral 8s")
		time.sleep(8)

		stamp=time.time()
		self.real_change_up(40)  
		print >> f, stamp,"4 degree up 4s"  #in file        #02 degree up 4s
		print(stamp,"4 degree up 4s") 
		time.sleep(4)

		stamp=time.time()
		self.real_change_up(0)                             #3 neutral temp 6s
		print >> f, stamp,"back to neutral 6s"  #in file
		print(stamp,"back to neutral 6s")
		time.sleep(6)

		stamp=time.time()
		self.real_change_up(60)
		print >> f, stamp,"6 degree up 5s"  #in file        #03 degree up
		print(stamp,"6 degree up 5s") 
		time.sleep(5)

		stamp=time.time()
		self.real_change_up(0)                            #4 neutral temp 5s
		print >> f, stamp,"back to neutral 2s"  #in file
		print(stamp,"back to neutral 2s")
		time.sleep(2)

		stamp=time.time()
		self.real_change_up(-20)
		print >> f, stamp,"2 down 5s"  #in file        #04 degree down 5s
		print(stamp,"2 down 5s") 
		time.sleep(5)

		stamp=time.time()
		self.real_change_up(0)                             #5 neutral temp 5s
		print >> f, stamp,"back to neutral 4s"  #in file
		print(stamp,"back to neutral 4s")
		time.sleep(4)

		stamp=time.time()
		self.real_change_up(70)  
		print >> f, stamp,"7 degree up 4s"  #in file        #05 degree up 5s
		print(stamp,"7 degree up 4s") 
		time.sleep(4)

		stamp=time.time()
		self.real_change_up(0)                            #6 neutral temp 5s
		print >> f, stamp,"back to neutral 3s"  #in file
		print(stamp,"back to neutral 3s")
		time.sleep(3)

		stamp=time.time()
		self.real_change_up(-70)  
		print >> f, stamp,"7 degree down 4s"  #in file        #06 degree down
		print(stamp,"7 degree down 4s") 
		time.sleep(4)

		stamp=time.time()
		self.real_change_up(0)                             #7 neutral temp 4s
		print >> f, stamp,"back to neutral 4s"  #in file
		print(stamp,"back to neutral 4s")
		time.sleep(4)

		stamp=time.time()
		self.real_change_up(20)
		print >> f, stamp,"2 degree up 5s"  #in file        #07 degree up 5s
		print(stamp,"2 degree up 5s") 
		time.sleep(5)

		stamp=time.time()
		self.real_change_up(0)                              #8 neutral temp 5s
		print >> f, stamp,"back to neutral 2s"  #in file
		print(stamp,"back to neutral 2s")
		time.sleep(2)

		stamp=time.time()
		self.real_change_up(-40)  
		print >> f, stamp,"4 degree down 4"  #in file        #08 degree down 4s
		print(stamp,"4 degree down 4") 
		time.sleep(4)

		stamp=time.time()
		self.real_change_up(0)                             #9 neutral temp 3s
		print >> f, stamp,"back to neutral 3"  #in file
		print(stamp,"back to neutral 3")
		time.sleep(3)

		stamp=time.time()
		self.real_change_up(50) 
		print >> f, stamp,"5 degree up 5"  #in file        #09 degree up 5s
		print(stamp,"5 degree up 5") 
		time.sleep(5)

		stamp=time.time()
		self.real_change_up(0)                             #10 neutral temp 3s
		print >> f, stamp,"back to neutral 3"  #in file
		print(stamp,"back to neutral 3")
		time.sleep(3)

		stamp=time.time()
		self.real_change_up(-50)  
		print >> f, stamp,"5 degree down 5"  #in file        #10 degree down 5s
		print(stamp,"5 degree down 5") 
		time.sleep(5)

		stamp=datetime.datetime.now()
		self.real_change_up(0)                             #10 neutral temp 3s
		print >> f, stamp,"round4 end"  #in file
		print(stamp,"round 4 end")
		time.sleep(3)

		self.do_disable_1()
		self.do_disable_2()
		f.close()
#--------------------------------------------------------------------------------------------------------------------------------------
	
	def temp_change(self,num):   #a convenient way to control the temp in 1 line
		temp = self.peltier.convert(num) 
		self.peltier.set_temp(1, temp)
		self.peltier.set_temp(2, temp)
		self.peltier.read_line()
	
	def real_change_up(self,change_vol):   #get real-time temp and up X(change_vol) degreeC
		temp = self.peltier.convert(real_time_numTemp+change_vol) 
		self.peltier.set_temp(1, temp) #by here add pump 2
		self.peltier.set_temp(2, temp)
		self.peltier.read_line()
	

	def do_temp1_button(self):
		temp = self.peltier.convert(self.p1_temp.get())
		self.peltier.set_temp(1, temp)
		#print 
		print(self.peltier.read_line())  #"Copyright 2017 SAMH Engineering Services "
		print(self.peltier.get_channel_temp(1))
		#self.peltier.set_temp(3, temp)
	
	def do_temp2_button(self):
		temp = self.peltier.convert(self.p2_temp.get())
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
		timefile.close()
		self.peltier.close()
		self.quit() 

	def printtime(self):
		stamp=datetime.datetime.now()
		print >> timefile, stamp
		print (stamp)
	
	def start_measure(self):
		T2 = threading.Thread(target=self.__start_measure)
		T2.start() 

	def __start_measure(self):
		global flag
		global real_time_temp
		global ser
		stamp=datetime.datetime.now()
		timehint=time.time()
		temp_file = open('temp_file.txt', 'w+')
		print("start measuring") 
		print >> temp_file, stamp,timehint,"start measuring"    #while opening file, start measuring
		while flag == 0:
			#time.sleep(5)
			real_time_temp = ser.readline()
			
			stamp=time.time()
			timehint=time.time()
			print >> temp_file,stamp,timehint,real_time_temp
			print (datetime.datetime.now(),real_time_temp)
			#time.sleep(6)
        
        	if flag!=0:
        		print >> temp_file, datetime.datetime.now(),timehint,"stop measuring"
        		temp_file.close()
            	#break	
	
	def stop_measure(self):
		global flag
		flag = 1       #just change the global and nothing else
		print("stop measuring")	
		
	def round1(self):
		T1 = threading.Thread(target=self.do_heat1, args=())
		T1.start()

	def round2(self):
		T2 = threading.Thread(target=self.do_heat2, args=())
		T2.start()
	
	def round3(self):
		T2 = threading.Thread(target=self.do_heat3, args=())
		T2.start()
	
	def round4(self):
		T2 = threading.Thread(target=self.do_heat4, args=())
		T2.start()

	




app = Peltier_Control()					
app.master.title("test code version2")

app.mainloop()
