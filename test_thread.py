import threading
import time

globalv=0

def thread1():
    global globalv
    f = open('test_thread.txt', 'w+')
    while True:
        time.sleep(1)
        print(time.strftime('%H:%M:%S'),'hahaha')
        
        print >> f, "hello testhhhhh"
        
        globalv = globalv+1
        if globalv>10:
            f.close()
            break
    
        

def thread2():
    while True:
        time.sleep(2)
        print(time.strftime('%H:%M:%S'),'lalala',globalv)
        

thread_thred1 = threading.Thread(target=thread1)
thread_thred1.start()
thread_thread2 = threading.Thread(target=thread2)
thread_thread2.start()

#great the sub thread could change the global variable and the other thread could read it.