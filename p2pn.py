#Player_n

from socket import *
#import socket
import sys 

serverSocket = socket(AF_INET, SOCK_DGRAM)


Host = '127.0.0.1'  #host ip {README!! ip->ipv4}
Port = 3000        #my port



xtrans =-999  #arbitrary value for bed init value
next_set =0 #tracks whether or not node is connected 0/1


try: serverSocket.sendto(str(xtrans).encode('utf-8'), (Host, Port))  #check if already exists
except: print('Waiting For Hospital to Join network...')


def receivemsg():
   global next, next_set,msg

   if next_set == 0: #should be 0 set up node/client
      next_set =1
      next = (Host,Port)   #neighbour node address {important!!}  #issue atm quick-fixed
      print("My next node is:" +str(next) ) #debug

   if (str(msg)[3] == '('):
      print("already formatted")
      return 1 #already formatted
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
   xtrans = input('Enter Available hospital beds:')
   serverSocket.sendto(str(xtrans).encode('utf-8'), next)
   #print("sent to next:"+str(next))

while True:   ##Essentially the main()
 ##if you want to update a global within a function declare as global at start of function 
 
   msg, addr = serverSocket.recvfrom(2048)  #wait to receive
   receivemsg()
   try:
      if scanforchangeNext() ==1: continue
      passOn()
      displayforme()

   except IOError:
      #sys.exit()#Terminate the program 
      print("err")