import threading
import sys
from random import randint

sem0 = threading.Semaphore()
sem1 = threading.Semaphore()
sem2 = threading.Semaphore()
sems = {"sem0" : sem0, "sem1": sem1, "sem2": sem2}


# class Sync(Thread):
#     def __init__ (self):
    
class Manager(threading.Thread):
    def __init__ (self, file_number, num):
        print("Criando Thread n° " + str(num))
        threading.Thread.__init__(self)
        self.num = num
        self.file_number = file_number
        self.path = f"arquivo{file_number}.txt"
    
    def run(self):
        correlate_semaphore = sems[f"sem{self.file_number}"]
        a = randint(0,1)
        correlate_semaphore.acquire()
        if a == 0:
            print("Thread " + str(self.num) + " está escrevendo no " + self.path)
            file = open(self.path,"a")
            file.write("Thread " + str(self.num) + " passou por aqui")
            file.close()
            print("Thread " + str(self.num) + " terminou de escrever no " + self.path);
        else:
            print("Thread " + str(self.num) + " está lendo no " + self.path + "\n")
            file = open(self.path, "r")
            line = file.read()
            print(line)
            file.close()
            print("Thread " + str(self.num) + " terminou de ler no " + self.path)
        correlate_semaphore.release()
        
for thread_number in range (10):
    thread = Manager(randint(0,2), thread_number)
    thread.start()