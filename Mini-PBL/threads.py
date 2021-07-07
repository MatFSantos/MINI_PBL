import threading
from random import randint

sem = threading.Semaphore()
sem2 = threading.Semaphore()
sincronizado = True
buff = []

processos_escritores = 0

class Sync(threading.Thread):
    def __init__ (self):
        print("Criando Thread de sincronização")
        threading.Thread.__init__(self)
    def run(self):
        sem.acquire()
        print("Arquivos estão sendo sincronizados...")
        # recently_file = open(f"arquivo{}.txt","r")
        # content = recently_file.read()
        # recently_file.close()
        for i in range(3):
            file = open(f"arquivo{i}.txt", "a")
            for content in buff:
                file.write(content)
            file.close()
        print("Arquivos sincronizados!")
        buff.clear()
        global sincronizado
        sincronizado = True
        sem.release()


class Manager(threading.Thread):
    def __init__ (self, file_number, num):
        print("Criando Thread n° " + str(num) + " manager")
        threading.Thread.__init__(self)
        self.num = num
        self.file_number = file_number
        self.path = f"arquivo{file_number}.txt"
    
    def run(self):
        a = randint(0,1)
        if a == 0:
            sem.acquire()
            print("Thread " + str(self.num) + " está escrevendo no " + self.path)

            buff.append("Thread " + str(self.num) + " passou por aqui\n")

            # file = open(self.path,"a")
            # file.write("Thread " + str(self.file_number) + " passou por aqui")
            # file.close()

            print("Thread " + str(self.num) + " terminou de escrever no " + self.path)

            global sincronizado
            sincronizado = False
            global processos_escritores
            processos_escritores += 1
            print("processos escritores: " + str(processos_escritores))
            sem.release()
        else:
            print("Thread " + str(self.num) + " Tentando ler arquivo " + self.path + ". . . ")
            while not sincronizado:
                print(". ")
            
            print("Thread " + str(self.num) + " está lendo no " + self.path)

            file = open(self.path, "r")
            line = file.read()
            print(line)
            file.close()

            print("Thread " + str(self.num) + " terminou de ler no " + self.path)


thread_number = 0
while thread_number != 40:
    if randint(0,1) != 0:
        Manager(randint(0,2),thread_number).start()
        thread_number += 1
    else:
        Sync().start()
        
Sync.start()
