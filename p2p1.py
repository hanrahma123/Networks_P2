#Header - David
#('192.168.1.14', 49343)0 pull host and port from that
#Player_1 Apex of p2p network
import asyncio
from threading import Thread
from socket import *
import sys 

serverSocket = socket(AF_INET, SOCK_DGRAM)

#Hospital names and abbreviation setup
cur_hosp = "Mayo Clinic Hospital - Sain Marys Campus (Rochester, Minn.)"
cur_habv = "MAYO"

Host = '127.0.0.1' #my ip origin device {find local ip -> ipconfig -> ipv4} README!!
Port = 3000        #myport
serverSocket.bind((Host,Port))


xtrans = 1  #arbitrary value 
next_set =0  #tracks whether or not node is connected 0/1

print('Setting up hospital data network...')
 
 
def receivemsg():
   global next_set,next,addr,msg, next_habv
   if next_set == 0: #should be 0 set up node/client
      next_set =1
      next = addr   #neighbour node address {important!!}
      print("A new hospital has joined the network!\n")
   if addr != next:
      if (str(msg)[3] == '('):
         print("already formatted")
         return 1 #already formatted
   
      if int(msg.decode('utf-8')) == -999:  #fresh node after 1st connected node, NEW HOSPITAL HAS JOINED NETWORK
         serverSocket.sendto((str(addr).encode('utf-8') + msg) , next) #if not for that node send to (next)
         print("passed msg to next node" +str(next)) #debug
         return 1 #dont display msg
   return 0

def displayforme():
   global msg
   #hopefully msg is for this node
   print('\nNumber of Beds from ',next_habv,': ' ,msg.decode('utf-8'))

def requestSend():
   
   global xtrans,next
   xtrans = input('Enter Available Hospital Beds:') 
   serverSocket.sendto(str(xtrans).encode('utf-8'), next)
      
def lookatport():
   global msg, addr
   msg,addr = serverSocket.recvfrom(2048)  #wait to receive


async def receiveandPrint():
   while True:
      print("recPrint")
      lookatport()
      response = receivemsg()
      #if response==0: 
      displayforme()
     
   

async def requestandSend():
   while True:
      print("reqSend")
      try:
         requestSend()
      except IOError:
         #sys.exit()  #Terminate the program 
         print("err")

def start_loop(loop):
   asyncio.set_event_loop(loop)
   loop.run_forever()

 #infinite loop
   #task1 = asyncio.create_task(receiveandPrint())
   #task2 = asyncio.create_task(requestandSend())
  # asyncio.run(receiveandPrint())
  # asyncio.run(requestandSend())
loop1 = asyncio.new_event_loop()
t1 = Thread(target=start_loop, args=(loop1,))
loop2 = asyncio.new_event_loop()
t2 = Thread(target=start_loop, args=(loop2,))

t1.start()  ## 2 threads running parallel
t2.start()

asyncio.run_coroutine_threadsafe(receiveandPrint(),loop1)
asyncio.run_coroutine_threadsafe(requestandSend(),loop2)
   #loop = asyncio.get_event_loop()
   # tasks =[asyncio.ensure_future(receiveandPrint()),
   # asyncio.ensure_future(requestandSend())]
   # loop.run_until_complete(asyncio.gather(*tasks))
   #await task1, task2
   
  



