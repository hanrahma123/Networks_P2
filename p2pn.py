#Player_n

from socket import *
from threading import Thread
import asyncio
import sys 
from Crypto.PublicKey import RSA
from Crypto import Random

serverSocket = socket(AF_INET, SOCK_DGRAM)
#generate an new public key from the fetch the file to get private key, create new public key from it, then you can encrypt whatever you want
file = open("Keys.txt", "r")
privateKeyString = file.read() 
file.close()
RSAkey = RSA.importKey(privateKeyString,passphrase='savelives')
publickey = RSAkey.publickey()

Host = '127.0.0.1'  #host ip {README!! ip->ipv4}
Port = 3000        #my port



xtrans =-999  #arbitrary value for bed init value
next_set =0 #tracks whether or not node is connected 0/1
next = (Host,Port)   #neighbour node address {important!!}  #issue atm quick-fixed

def encrypt(msg):
   bytes_msg = msg.encode()
   enc_data = publickey.encrypt(bytes_msg, 16) #encrypt message with public key
   print('encrypted message is: ' + str(enc_data[0]))
   return enc_data


def decrypt(msg):
   print('in decrypt')
   # retrieve exported private key from file
   file = open("Keys.txt", "r")
   privateKeyString = file.read() 
   file.close()
   print('private key is: ')
   print(privateKeyString)
   privatekey = RSA.importKey(privateKeyString,passphrase = "savelives")
   dec_data = privatekey.decrypt(msg)
   #print("before stringing dec_data")
   dec_data = str(dec_data.decode())
   #print('dec_data is: ' + dec_data)
   return dec_data

try: 
   print('xtrans is: ' + str(xtrans))
   serverSocket.sendto(encrypt(str(xtrans))[0], (Host, Port))  #check if already exists
   print("\nsent" )
#try: serverSocket.sendto(str(xtrans).encode('utf-8'), (Host, Port))
except: print('Waiting For Hospital to Join network...')


def receivemsg():
   global next, next_set,msg
   
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
   print("entered scanforchangeNext()")
   
   charmsg = [] 
   charmsg[:0] = msg
   print("The 0 character is", charmsg[0])

   if(next == (Host,Port) and charmsg[0] == '('):      #if msg received is about to go to host then point to included ip address!!!
      print("must intercept")
      newaddrr = msg.split("-999")
      print("message split")
      newerAddr = newaddrr[0].split(",")
      print("updated the address")
      
      newhost = str(newerAddr[0]).split("'")
      #print("ip fn:"+newhost[1]) #final val for host ip  debug

      newport = str(newerAddr[1]).split(")")
      #print("port fn:"+ newport[0]) #final port val   debug
      print("going to encrypt the message")
      encrypted = encrypt(str(xtrans))
      print("message encrypted")

      print("new host is", str(newhost[1]), "and new port is", int(newport[0]))

      print("sending the message")
      serverSocket.sendto(encrypted[0], (str(newhost[1]), int(newport[0])))
      print("message was sent")
      next = (str(newhost[1]), int(newport[0]))
      print("Just changed next to:" + str(next))
      return 1
   return 0

def passOn():
   global msg,next_set
   charmsg = [] 
   charmsg[:0] = msg
   print("The 0 character is", charmsg[0])
   if(charmsg[0] == '('):     #if already formatted but not for me
      encrypted = encrypt(msg)
      serverSocket.sendto(encrypted[0], next)
      print("Passed on msg")
      return 1
   return 0

def displayforme():
   global addr,msg, xtrans,next
   print('Number of Beds from:',addr,'==' ,msg)

def inputSend():
   xtrans = input('Enter Available hospital beds:\n')
   encrypted = encrypt(xtrans) 
   xtrans = encrypted[0]
   #NOT WORKING. possibly because it got confused what next is?

   #need to extract[0] b/c RSA encode returns a tuple with one element as the encrypted message
   #serverSocket.sendto(encrypted[0], next)
   print("\nnext="+str(next))
   print("\nsent to next:"+str(xtrans))
   
   serverSocket.sendto(encrypted[0], next)
   #print("\nsent to next:"+str(xtrans))

def lookatport():
   global msg, addr
   msg,addr = serverSocket.recvfrom(2048)  #wait to receive
   print("msg received:",msg)

async def receiveandPrint():
   global msg
   while True:
      lookatport()
      msg = decrypt(msg)
      #print("\nmsg: " +msg)
      receivemsg() 
      if scanforchangeNext() ==1:
         displayforme()
      else: 
         passOn()
         displayforme()
      

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


   
