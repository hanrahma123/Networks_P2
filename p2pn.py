#Player_n

from socket import *
from threading import Thread
import asyncio
import sys
import time

serverSocket = socket(AF_INET, SOCK_DGRAM)


Host = '127.0.0.1'  #host ip {README!! ip->ipv4}
Port = 3000        #my port

hosp_id = 1
hosp_code = ["MAYO", "MAST", "ADVH", "METO", "CEDS"]
hosp_name = ["Mayo Clinic Hospital", "Massachusetts General Hospital", "AdventHealth Orlando",
"Methodist Hospital", "Cedars-Sinai Medical Center"]


xtrans =-999  #arbitrary value for bed init value
next_set =0 #tracks whether or not node is connected 0/1
next = (Host,Port)   #neighbour node address {important!!}  #issue atm quick-fixed

try: serverSocket.sendto(str(xtrans).encode('utf-8'), (Host, Port))  #check if already exists
except: print('Waiting For Hospital to Join network...')

def interpreter(dmsg):
   global hosp_id, next
   dmsg_arr = dmsg.split()
   if dmsg_arr[0] == "ID": #assigning ID to this hospital
      hosp_id = int(dmsg_arr[1])
      print("My ID is", hosp_id)
      print("Abreviation->", hosp_code[hosp_id])
      print("Hospital Name->", hosp_name[hosp_id])
   elif dmsg_arr[0] == "beds":
      print("received a beds message")
      if dmsg_arr[1] != str(hosp_id):
         print("passing message")
         pasmsg = dmsg
         serverSocket.sendto(str(pasmsg).encode('utf-8'), next)
         print("message passed")
      else:
         print("message returned home")

def formatter():
   global xtrans, reqlocation, hosp_id
   xtrans_arr = xtrans.split()
   if xtrans_arr[0] == "beds":
      reqlocation = xtrans_arr[1]
      test = xtrans.replace(reqlocation, str(hosp_id))
      print("beds message:", test)
      xtrans = test


def receivemsg():
   global next, next_set, msg

   if next_set == 0: #should be 0 set up node/client
      next_set =1
  
      print("My next node is:" +str(next) ) #debug

   # if (str(msg)[3] == '('):
   #    print("already formatted")
   #    return 1 #already formatted
   return 0

def scanforchangeNext():
   global next,msg
   #hopefully msg is for this node...
   if(next == (Host,Port) and msg.decode('utf-8')[0] == '('):      #if msg received is about to go to host then point to included ip address!!!
      print("must intercept")
      newaddrr = msg.decode('utf-8').split("-999")
      newerAddr = newaddrr[0].split(",")
      
      newhost = str(newerAddr[0]).split("'")
      #print("ip fn:"+newhost[1]) #final val for host ip  debug

      newport = str(newerAddr[1]).split(")")
      #print("port fn:"+ newport[0]) #final port val   debug
      
      serverSocket.sendto(str(xtrans).encode('utf-8'), (str(newhost[1]), int(newport[0])))
      next = (str(newhost[1]), int(newport[0]))
      print("Just changed next to:" + str(next))
      return 1
   return 0

def passOn():
   global msg,next_set
   if(msg.decode('utf-8')[0] == '('):     #if already formatted but not for me
      serverSocket.sendto(msg, next)
      print("Passed on msg")
      return 1
   return 0

def displayforme():
   global addr,msg, xtrans,next
   print('Number of Beds from:',addr,'==' ,msg.decode('utf-8'))

def inputSend():
   global xtrans
   xtrans = input('Enter command:\n')
   formatter()
   serverSocket.sendto(str(xtrans).encode('utf-8'), next)
   #print("sent to next:"+str(next))

def lookatport():
   global msg, addr
   msg,addr = serverSocket.recvfrom(2048)  #wait to receive

async def receiveandPrint():
   global msg
   while True:
      lookatport()
      receivemsg() 
      if scanforchangeNext() ==1:
         displayforme()
      else: 
         passOn()
         displayforme()
      interpreter(msg.decode('utf-8'))
      

async def requestandSend():
   while True:
      try : 
         inputSend()
      except IOError:
         #sys.exit()  #Terminate the program 
         print("err")

def start_loop(loop):
   asyncio.set_event_loop(loop)
   loop.run_forever()


   ##Essentially the main()
 ##if you want to update a global within a function declare as global at start of function 
   
loop1 = asyncio.new_event_loop()
t1 = Thread(target=start_loop, args=(loop1,))
loop2 = asyncio.new_event_loop()
t2 = Thread(target=start_loop, args=(loop2,))

t1.start()  ##2 threads running in parallel
t2.start()


asyncio.run_coroutine_threadsafe(receiveandPrint(),loop1)
asyncio.run_coroutine_threadsafe(requestandSend(),loop2)


   