#Header - David
#('192.168.1.14', 49343)0 pull host and port from that
#Player_1 Apex of p2p network
import asyncio
from threading import Thread
from socket import *
import random

serverSocket = socket(AF_INET, SOCK_DGRAM)


Host = '127.0.0.1' #my ip origin device {find local ip -> ipconfig -> ipv4} README!!
Port = 3000        #myport
serverSocket.bind((Host,Port))

hosp_id = 0
hosp_code = ["MAYO", "MAST", "ADVH", "METO", "CEDS"]
hosp_name = ["Mayo Clinic Hospital", "Massachusetts General Hospital", "AdventHealth Orlando",
"Methodist Hospital", "Cedars-Sinai Medical Center"]
other_hosp_id = 0       #sends hospital ids to new hosital on network

#Data initliasation
num_beds = 5000 - random.randint(1,2000)
num_free_beds = num_beds - random.randint(1,num_beds)
print("Number of beds ->", num_beds)
print("Number of unoccupied beds ->", num_free_beds)

xtrans = 1  #arbitrary value 
next_set =0  #tracks whether or not node is connected 0/1

print('Waiting for hospitals to join network...')
 
def interpreter(dmsg):
   global other_hosp_id, addr, next, num_free_beds
   dmsg_arr = dmsg.split()
   if dmsg == "-999":
      print("New node on network")
      other_hosp_id = other_hosp_id + 1
      id = str(other_hosp_id)
      reply = "ID " + id
      serverSocket.sendto(str(reply).encode('utf-8'), addr) 
      #replies to address where it received the message from the new node
      
   elif dmsg_arr[0] == "beds":
      print("received a beds message")
      if dmsg_arr[1] != str(hosp_id):
         print("passing message")
         pasmsg = dmsg
         #adjust number of free beds for sense of realism
         num_free_beds = num_free_beds + random.randint(1,100) - 50
         #attach this hospital's data
         pasmsg = pasmsg + " " + str(hosp_id) + " " + str(num_beds) + " " + str(num_free_beds)
         #ENCRYPT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
         serverSocket.sendto(str(pasmsg).encode('utf-8'), next)
         print("message passed")
      else:
         print("message returned home")
         #now print the data into a table
         table(dmsg)
         
def table(ctable):
   #print("entered table function")
   global reqlocation #the hospital abrevation that was requested by this node
   ctable_arr = ctable.split()
   print("HospID\t Abrev\t Total Beds\t Free Beds\t Hospital")
   print(hosp_id, "\t", hosp_code[hosp_id], "\t", num_beds, "\t\t", num_free_beds, "\t\t", hosp_name[hosp_id])

   arraysize = 0
   for n in ctable_arr:
      arraysize = arraysize + 1

   index = 2   #index 2 is id, 3 is number of beds, 4 is number of unoccupied beds
   while(arraysize > index):
      cid = ctable_arr[index]
      ctotbeds = ctable_arr[index + 1]
      cfree = ctable_arr[index+2]
      cid = int(cid)
      if reqlocation == hosp_code[cid]:
         print("This hospital was selected, colours to be added")
      else:
         print(cid, "\t", hosp_code[cid], "\t", ctotbeds, "\t\t", cfree, "\t\t", hosp_name[cid])
      index = index + 3




def formatter():
   global xtrans, reqlocation, hosp_id
   xtrans_arr = xtrans.split()
   if xtrans_arr[0] == "beds":
      reqlocation = xtrans_arr[1]
      test = xtrans.replace(reqlocation, str(hosp_id))
      print("beds message:", test)
      xtrans = test




def receivemsg():
   global next_set,next,addr,msg
   if next_set == 0: #should be 0 set up node/client
      next_set =1
      next = addr   #neighbour node address {important!!}
      print("My next node is:" +str(next)+ str(msg) ) #debug
   if addr != next:
      if (str(msg)[3] == '('):
         print("already formatted")
         return 1 #already formatted
   
      if str(msg.decode('utf-8')) == "-999":  #fresh node after 1st connected node
         serverSocket.sendto((str(addr).encode('utf-8') + msg) , next) #if not for that node send to (next)
         print("passed msg to next node" +str(next)) #debug
         return 1 #dont display msg
   return 0

def displayforme():
   global msg
   #hopefully msg is for this node
   print('Number of Beds from:',addr,'==' ,msg.decode('utf-8'))

def requestSend():
   
   global xtrans,next
   xtrans = input('Enter command:\n') 
   formatter()
   serverSocket.sendto(str(xtrans).encode('utf-8'), next)
      
def lookatport():
   global msg, addr
   print("Waiting to receive...")
   msg,addr = serverSocket.recvfrom(2048)  #wait to receive
   print("A message has been received")


async def receiveandPrint():
   global msg
   while True:
      #print("recPrint")
      lookatport()
      #DECRYPT msg!!!!!!!!!!!!!!!!!!!!!!!!!!!
      response = receivemsg()
      #if response==0: 
      displayforme()
      interpreter(msg.decode('utf-8'))
     
   

async def requestandSend():
   while True:
     # print("reqSend")
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
   
  



