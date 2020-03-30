#('192.168.1.14', 49343)0 pull host and port from that
#Player_1 Apex of p2p network

from socket import *
import sys 

serverSocket = socket(AF_INET, SOCK_DGRAM)


Host = '127.0.0.1' #my ip origin device {find local ip -> ipconfig -> ipv4} README!!
Port = 3000        #myport
serverSocket.bind((Host,Port))


xtrans = 1  #arbitrary value 
next_set =0  #tracks whether or not node is connected 0/1

print('Waiting For Player to Join network...')
  
 
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
   
      if int(msg.decode('utf-8')) == -999:  #fresh node after 1st connected node
         serverSocket.sendto((str(addr).encode('utf-8') + msg) , next) #if not for that node send to (next)
         print("passed msg to next node" +str(next)) #debug
         return 1 #dont display msg
   return 0

def display():
   global msg
   #hopefully msg is for this node
   print('Prev node has N beds:', msg.decode('utf-8'))

def requestSend():
   global xtrans,next
   xtrans = input('Enter Available Hospital Beds:')
   serverSocket.sendto(str(xtrans).encode('utf-8'), next)
   

while True: #infinite loop
  
   msg,addr = serverSocket.recvfrom(2048)  #wait to receive
   response = receivemsg()
   if response==1: continue
   try:
      display()
      requestSend()
   except IOError:
      #sys.exit()  #Terminate the program 
      print("err")



