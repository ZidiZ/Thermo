import serial
from PeltierBoard import PeltierBoard  #
import time

temp1=input("input a temp: \n")
#print(temp)

class Peltier_Control():			 
	def __init__(self, master=None):  #
	
		self.peltier = PeltierBoard(1)
		#self.peltier.disable_roc_limit()
		self.roc_limited = False
		#print 
		self.peltier.read_line()
		
	
		
	def do_temp1_button(self):  #tab
		temp = self.peltier.convert(temp1) #p1_temp?37 change self.peltier
		self.peltier.set_temp(1, temp)  #channel1 temperature
		print (temp)
		read_set=self.peltier.read_line()
		print(read_set)
		#self.peltier.set_temp(3, temp)

	




			
app = Peltier_Control()					
app.do_temp1_button()
app.peltier.get_channel_temp(1)
app.peltier.get_channel_set_point(1)