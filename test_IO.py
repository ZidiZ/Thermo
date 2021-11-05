import serial
import re


#write_to_file_path = "C:/Users/Administrator/Downloads/project/PeltierControlDemoOriginal/PeltierControlDemoOriginal/Thermo/testfile.txt"

""" f = open('testfile.txt', 'w+')

print >> f, "hello testhhhhh"
print(f) """

#ser = serial.Serial('COM3',9600)
""" with open('testfile1.txt', 'w+') as f:
    while True:
        line = ser.readline()
        print(line.strip(), " t = %s \n " % (datetime.datetime.now()))
        #f.writelines([line.strip(), " t = %s \n " % (datetime.datetime.now())])
        #f.writelines("hello") """

ser = serial.Serial('COM3',9600)
real_time_temp = ser.readline() # a global
print(real_time_temp)

toolvariable1 = re.findall(r"\d+\.?\d*",real_time_temp) #filt the number out
toolvariable2 = toolvariable1[-1]
print(toolvariable1)
print(toolvariable2)

toolvariable3 = float(toolvariable2)*10
print(int(toolvariable3))
#real_time_numTemp = int(toolvariable)