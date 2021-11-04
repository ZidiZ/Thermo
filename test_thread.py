import threading
import time

def thread1():
    while True:
        time.sleep(1)
        print(time.strftime('%H:%M:%S'),'hahaha')

def thread2():
    while True:
        time.sleep(2)
        print(time.strftime('%H:%M:%S'),'lalala')

thread_thred1 = threading.Thread(target=thread1)
thread_thred1.start()
thread_thread2 = threading.Thread(target=thread2)
thread_thread2.start()