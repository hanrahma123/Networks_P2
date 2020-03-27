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


while True:
 
 
   msg, addr = serverSocket.recvfrom(2048)  #wait to receive
   if next_set == 0: #should be 0 set up node/client
      next_set =1
      next = (Host,Port)   #neighbour node address {important!!}  #issue atm quick-fixed
      print("My next node is:" +str(next) ) #debug
   
   print('msg is: ' + str(msg))

   if (str(msg)[3] == '('): #this will throw a string index out of range error bc the msg is only the number of beds
      print("already formatted")
      continue #already formatted

   try:
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
         continue
      if(msg.decode('utf-8')[0] == '('):     #if already formatted but not for me
         serverSocket.sendto(msg, next)

      print('Player Moved to:', msg.decode('utf-8'))
      xtrans = input('Enter Next Move as Number:')
      serverSocket.sendto(str(xtrans).encode('utf-8'), next)
      #print("sent to next:"+str(next))

   except IOError:
      sys.exit()#Terminate the program 