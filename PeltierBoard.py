import serial

class PeltierBoard:
	
	def __init__(self, board_num):
		#self.peltier = serial.Serial('/dev/tty.usbserial-A7005tIa',460800)
		#self.peltier = serial.Serial('/dev/tty.SKHP2SN0000-SPPDev',460800)

		self.peltier = serial.Serial('COM4',460800)#USB

#		self.disable_streaming()
#		for i in xrange(4):
		print (self.peltier.readline())
		
	#sets the temperature, temp, for a peltier channel(1-4) in tenths of a degree C
	#e.g. to set to 38.5degC temp = 385; to set to 10degC = 100
	def set_temp(self, peltier_channel, temp):
		channel = "0"+str(peltier_channel)
		self.peltier.write('$CMD,'+temp+','+channel+"\n")
		
	#disables a single peltier channel(1-4). Cuts off voltage to channel
	def disable_channel(self, peltier_channel):
		channel = "0"+str(peltier_channel)
		self.peltier.write('$CMD,FFFF,'+channel+"\n")
		
	#prints the current temperature of the given peltier channel(1-4) to console
	def get_channel_temp(self, peltier_channel):
		channel = "000"+str(peltier_channel)
		self.peltier.write('$CMD,'+channel+',05\n')
		response = "Channel "+str(peltier_channel)+" Temp: "
		response += self.peltier.readline()
		print(response)
		
	#prints the last set_temp value sent to the given peltier channel(1-4) to console
	def get_channel_set_point(self, peltier_channel):
		channel = "000"+str(peltier_channel)
		self.peltier.write('$CMD,'+channel+',06\n')
		response = "Channel "+str(peltier_channel)+" Set-Point Temp: "
		response += self.peltier.readline()
		print (response)
		
	def led_red_on_green_off(self):
		self.peltier.write('$CMD,0001,00\n')
	
	def led_green_on_red_off(self):
		self.peltier.write('$CMD,0002,00\n')

	def led_both_off(self):
		self.peltier.write('$CMD,0000,00\n')
		
	def led_both_on(self):
		self.peltier.write('$CMD,0003,00\n')
		
	#starts streaming the current temp and the last set temp of all Peltiers
	def enable_streaming(self):
		self.peltier.write('$CMD,0001,07\n')
	
	#stream the current temp and last set temp of all Peltiers for a given number of readings
	def stream_num_readings(self, num_readings):
		self.peltier.write("$CMD,0001,07\n")
		#print 
		self.peltier.readline()
		for i in range(num_readings):
			response = self.peltier.readline()
			#print response
		self.peltier.write("$CMD,0000,07\n")
		#print 
		self.peltier.readline()
		
	#stops streaming the current temp and the last set temp of all Peltiers
	def disable_streaming(self):
		self.peltier.write('$CMD,0000,07\n')
		response = ("Data Streaming Disabled: ")
		response += self.peltier.readline()
		#print response
		
	#limits temperature change to ~1degC/sec
	def enable_roc_limit(self):
		self.peltier.write('$CMD,0001,08\n')
		
	#sets temperature change to ~3degC/sec
	def disable_roc_limit(self):
		self.peltier.write('$CMD,0000,08\n')
		
	#reads from the top of the response stack
	def read_line(self):
		temp = self.peltier.readline()
		return temp
	
	def read_bytes(self, num_bytes):
		return self.peltier.read(num_bytes)
		
	#due to a dodgy native Python hex conversion function, this takes a temperature as an int (e.g. 320 for 32degC)
	#and returns it as a hex string, i.e. "0140" for 320
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
		
	def close(self):
		self.peltier.close()
		