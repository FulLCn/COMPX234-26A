import threading
import time
import random

from printDoc import printDoc
from printList import printList

class Assignment1:
    # Simulation Initialisation parameters
    NUM_MACHINES = 50        # Number of machines that issue print requests 申请打印的数量
    NUM_PRINTERS = 5         # Number of printers in the system 打印机数量
    SIMULATION_TIME = 30     # Total simulation time in seconds 模拟总时长
    MAX_PRINTER_SLEEP = 3    # Maximum sleep time for printers 打印机休眠最大时长
    MAX_MACHINE_SLEEP = 5    # Maximum sleep time for machines 机器最大休眠时间

    # Initialise simulation variables 初始化
    def __init__(self):
        self.sim_active = True
        self.print_list = printList()  # Create an empty list of print requests 创建打印列表
        self.mThreads = []             # list for machine threads 机器线程列表
        self.pThreads = []             # list for printer threads 打印机线程列表
        #--task2--#
        # 互斥锁：保证队列同一时间只能被一个线程操作
        self.queue_lock = threading.Lock()
        #信号量：empty空位，full待打印项目
        self.empty=threading.Semaphore(5)
        self.full=threading.Semaphore(0)



    def startSimulation(self):
        # Create Machine and Printer threads 创建机器和打印机线程
        # Write code here
        for i in range(self.NUM_MACHINES):#机器线程
            t=self.machineThread(i,self)
            self.mThreads.append(t)
        
        for i in range(self.NUM_PRINTERS):#打印机线程
            t=self.printerThread(t,self)
            self.pThreads.append(t)

        # Start all the threads
        # Write code here
        for t in self.mThreads:#start==>python自带：启动代码
            t.start()
        
        for t in self.pThreads:
            t.start()

        # Let the simulation run for some time #等待线程结束
        time.sleep(self.SIMULATION_TIME)

        # Finish simulation
        self.sim_active = False

        # Wait until all printer threads finish by joining them
        # Write code here
        for t in self.mThreads:
            t.join()
        
        for t in self.pThreads:
            t.join()

    # Printer class
    class printerThread(threading.Thread):
        def __init__(self, printerID, outer):
            threading.Thread.__init__(self)
            self.printerID = printerID
            self.outer = outer  # Reference to the Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Simulate printer taking some time to print the document
                self.printerSleep()
                # Grab the request at the head of the queue and print it
                # Write code here

        def printerSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_PRINTER_SLEEP)
            time.sleep(sleepSeconds)

        def printDox(self, printerID):
            print(f"Printer ID: {printerID} : now available")
            # Print from the queue
            self.outer.print_list.queuePrint(printerID)

    # Machine class
    class machineThread(threading.Thread):
        def __init__(self, machineID, outer):
            threading.Thread.__init__(self)
            self.machineID = machineID
            self.outer = outer  # Reference to the Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Machine sleeps for a random amount of time
                self.machineSleep()
                # Machine wakes up and sends a print request
                # Write code here
                self.printRequest(self.machineID)

        def machineSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_MACHINE_SLEEP)
            time.sleep(sleepSeconds)

        def printRequest(self, id):
            print(f"Machine {id} Sent a print request")
            # Build a print document
            doc = printDoc(f"My name is machine {id}", id)
            # Insert it in the print queue
            self.outer.print_list.queueInsert(doc)