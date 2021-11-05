import serial
import datetime


#baud_rate = 9600; #In arduino, Serial.begin(baud_rate)



#write_to_file_path = "C:/Users/Administrator/Downloads/project/PeltierControlDemoOriginal/PeltierControlDemoOriginal/Thermo/testfile.txt"

""" f = open('testfile.txt', 'w+')

print >> f, "hello testhhhhh"
print(f) """

ser = serial.Serial('COM3',9600)
with open('testfile1.txt', 'w+') as f:
    while True:
        line = ser.readline()
        print(line)
        #f.writelines([line.strip(), " t = %s \n " % (datetime.datetime.now())])
        f.writelines("hello")

