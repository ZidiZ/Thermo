##############
## Script listens to serial port and writes contents into a file
##############
## requires pySerial to be installed 
import serial


#baud_rate = 9600; #In arduino, Serial.begin(baud_rate)
write_to_file_path = "C:/Users/Administrator/Downloads/project/PeltierControlDemoOriginal/PeltierControlDemoOriginal/Thermo/testfile.txt"
print(write_to_file_path)


ser = serial.Serial('COM3',9600)

f = open('testfile1.txt', 'w+')
print(f)

while True:
    

    line = ser.readline()
    line = line.decode("utf-8") #ser.readline returns a binary, convert to string
    
    #output_file.write(line)
    print >> f, "line"
    print(line)