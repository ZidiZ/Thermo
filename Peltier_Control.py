from Tkinter import * #in python3 tkinter; python2 Tkinter
import tkFont # also a fix for python3
import serial
from PeltierBoard import PeltierBoard
import time

class Peltier_Control(Frame):			 
	def __init__(self, master=None):
		# Board 1: A7SDXJ5F
		# Board 4: A7SDXIR8
		# Board 3: A7SDXJIH
#		self.peltier = serial.Serial('/dev/tty.usbserial-A7SDXJ5F',460800)
#		self.peltier = serial.Serial('/dev/tty.SKHP2SN0000-SPPDev',460800)
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
		
		self.p3_label = Label(self, text='Channel 3')
		self.p3_label.grid(column=1, row=5)
		self.p3_temp = Entry(self, width=4)
		self.p3_temp.grid(column=2, row=5)
		self.p3_button = Button(self, text='Set', command=self.do_temp3_button)
		self.p3_button.grid(column=3, row=5, padx=10)
		self.p3_disable = Button(self, text='Disable', command=self.do_disable_3)
		self.p3_disable.grid(column=4, row=5)
		
		self.p4_label = Label(self, text='Channel 4')
		self.p4_label.grid(column=1, row=7)
		self.p4_temp = Entry(self, width=4)
		self.p4_temp.grid(column=2, row=7)
		self.p4_button = Button(self, text='Set', command=self.do_temp4_button)
		self.p4_button.grid(column=3, row=7, padx=10)
		self.p4_disable = Button(self, text='Disable', command=self.do_disable_4)
		self.p4_disable.grid(column=4, row=7)
		
		self.streamButton = Button (self, text='Toggle ROC', command=self.stream_data)	   
		self.streamButton.grid(column=1, row=11, sticky=W) 
		
		self.redButton = Button (self, text='Red LED', command=self.toggle_red)	   
		self.redButton.grid(column=2, row=9, sticky=W) 
		
		self.greenButton = Button (self, text='Green LED', command=self.toggle_green)	   
		self.greenButton.grid(column=1, row=9, sticky=W) 
		
		self.quitButton = Button (self, text='Quit', command=self.quit_control)	   
		self.quitButton.grid(column=1, row=12, sticky=W)   
		
	def do_temp1_button(self):
		temp = self.convert(self.p1_temp.get())
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
		
	def do_temp3_button(self):
		temp = self.convert(self.p3_temp.get())
		self.peltier.set_temp(3, temp)
		#print self.peltier.read_line()
		
	def do_temp4_button(self):
		temp = self.convert(self.p4_temp.get())
		self.peltier.set_temp(4, temp)
#		print self.peltier.read_line()
		
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
		
	def do_disable_3(self):
		self.peltier.disable_channel(3)
		#print 
		self.peltier.read_line()
		#print "Disable 3"
		
	def do_disable_4(self):
		self.peltier.disable_channel(4)
		#print 
		self.peltier.read_line()
		#print "Disable 4"
				
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
				
	def toggle_red(self):
		if self.red_on==True and self.green_on==True:
			self.peltier.led_green_on_red_off()
			response = self.peltier.read_line()
			#print response
			self.red_on=False
		elif self.red_on==True and self.green_on==False:
			self.peltier.led_both_off()
			response = self.peltier.read_line()
			#print response
			self.red_on=False
		elif self.red_on==False and self.green_on==True:
			self.peltier.led_both_on()
			response = self.peltier.read_line()
			#print response
			self.red_on=True
		elif self.red_on==False and self.green_on==False:
			self.peltier.led_red_on_green_off()
			response = self.peltier.read_line()
			#print response
			self.red_on=True
		
	def toggle_green(self):
		if self.red_on==True and self.green_on==True:
			self.peltier.led_red_on_green_off()
			response = self.peltier.read_line()
			#print response
			self.green_on=False
		elif self.red_on==True and self.green_on==False:
			self.peltier.led_both_on()
			response = self.peltier.read_line()
			#print response
			self.green_on=True
		elif self.red_on==False and self.green_on==True:
			self.peltier.led_both_off()
			response = self.peltier.read_line()
			#print response
			self.green_on=False
		elif self.red_on==False and self.green_on==False:
			self.peltier.led_green_on_red_off()
			response = self.peltier.read_line()
			#print response
			self.green_on=True
			
	def convert(self, number):
		number_int = int(number)
		
		digit_1 = 0
		digit_2 = 0
		digit_3 = 0
		degree_tenths = number_int
		if number_int<1000:
			digit_1 = degree_tenths/256
			carry = degree_tenths-(digit_1*256)
			digit_2 = carry/16
			carry2 = carry-(digit_2*16)
			if digit_2 > 9:
				if digit_2==10:
					digit_2 = "A"
				elif digit_2==11:
					digit_2 = "B"
				elif digit_2==12:
					digit_2 = "C"
				elif digit_2==13:
					digit_2 = "D"
				elif digit_2==14:
					digit_2 = "E"
				elif digit_2==15:
					digit_2 = "F"
			
			if carry2 > 9:
				if carry2==10:
					digit_3 = "A"
				elif carry2==11:
					digit_3 = "B"
				elif carry2==12:
					digit_3 = "C"
				elif carry2==13:
					digit_3 = "D"
				elif carry2==14:
					digit_3 = "E"
				elif carry2==15:
					digit_3 = "F"
			else:
				digit_3 = carry2
					
		output = "0"+str(digit_1)+str(digit_2)+str(digit_3)

		#print "Conversion = "+output
		return output
			
	def quit_control(self):
		self.peltier.close()
		self.quit() 

app = Peltier_Control()					
app.master.title("SAMH Peltier Heat Pump Control")
app.mainloop()