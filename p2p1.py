#('192.168.1.14', 49343)0 pull host and port from that
#Player_1 Apex of p2p network
import asyncio
from threading import Thread
from socket import *
import sys 
from Crypto import Random
from Crypto.Random import random as rand
import Crypto.Cipher.AES as AES
from Crypto.PublicKey import RSA

#generate keys
random = Random.new().read
RSAkey = RSA.generate(1024, random) 
private = RSAkey #private key used for decryption
public = RSAkey.publickey() #public key used for encryption
#save private key to password protected file shared among hospitals in network
file = open("Keys.txt", "w")
file.write(private.exportKey(passphrase='savelives').decode()) #save exported private key
file.close()

#generate hospital data
hosp_id = 0
hosp_code = ["MAYO", "MAST", "ADVH", "METO", "CEDS"]
hosp_name = ["Mayo Clinic Hospital", "Massachusetts General Hospital", "AdventHealth Orlando",
"Methodist Hospital", "Cedars-Sinai Medical Center"]
other_hosp_id = 0       #sends hospital ids to new hospital on network

num_beds = rand.randint(1000,5000)
num_free_beds = num_beds - 1000
print("Hospital Name: " +  hosp_name[hosp_id] + "(" + hosp_code[hosp_id] + ") with id: " + str(hosp_id))
print("Number of total beds ->", num_beds)
print("Number of unoccupied beds ->", num_free_beds)


serverSocket = socket(AF_INET, SOCK_DGRAM)

Host = '127.0.0.1' #my ip origin device {find local ip -> ipconfig -> ipv4} README!!
Port = 3000        #myport
serverSocket.bind((Host,Port))


xtrans = 1  #arbitrary value 
next_set =0  #tracks whether or not node is connected 0/1

print('Waiting For Hospitals to join network...')

def interpreter(dmsg):
   global other_hosp_id, addr, next, num_free_beds
   dmsg_arr = dmsg.split()
   if dmsg == "-999":
      other_hosp_id = other_hosp_id + 1
      id = str(other_hosp_id)
      reply = "ID " + id
      encrypted = encrypt(reply)
      serverSocket.sendto(encrypted[0], addr) 
      #replies to address where it received the message from the new node
      
   elif dmsg_arr[0] == "beds":
      if dmsg_arr[1] != str(hosp_id):
         pasmsg = dmsg
         #adjust number of free beds for sense of realism
         num_free_beds = num_free_beds
         #attach this hospital's data
         pasmsg = pasmsg + " " + str(hosp_id) + " " + str(num_beds) + " " + str(num_free_beds)
         #ENCRYPT HERE
         encrypted = encrypt(pasmsg)
         serverSocket.sendto(encrypted[0], next)
      else:
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
         print("\033[1;32;41m") #text colour changed to green
         print(cid, "\t", hosp_code[cid], "\t", ctotbeds, "\t\t", cfree, "\t\t", hosp_name[cid])
         print('\033[0m')  #text reset to normal again
      else:
         print(cid, "\t", hosp_code[cid], "\t", ctotbeds, "\t\t", cfree, "\t\t", hosp_name[cid])
      index = index + 3

def formatter():
   global xtrans, reqlocation, hosp_id
   xtrans_arr = xtrans.split()
   if xtrans_arr[0] == "beds":
      reqlocation = xtrans_arr[1]
      test = xtrans.replace(reqlocation, str(hosp_id))
      xtrans = test

def encrypt(msg):
   bytes_msg = msg.encode()
   encrypted = public.encrypt(bytes_msg, 16) #encrypt message with public key
   return encrypted

def decrypt(msg):
   global private
   decrypted = private.decrypt(msg)
   decrypted = str(decrypted.decode())
   return decrypted

def receivemsg():
   global next_set,next,addr,msg
   if next_set == 0: #should be 0 set up node/client
      next_set =1
      next = addr   #neighbour node address {important!!}
      
   if addr != next:
      if (msg[3] == '('):
         return 1 #already formatted
      if msg == "-999":  #fresh node after 1st connected node
         adrMsg = str(addr) + " " + msg
         adrMsg = str(adrMsg)
         encrypted = encrypt(adrMsg)
         serverSocket.sendto(encrypted[0], next) #if not for that node send to (next)
         return 1 #dont display msg
   return 0

def displayforme():
   global msg, other_hosp_id
   #hopefully msg is for this node
   if(msg == '-999'): #a node makes first contact
      print(hosp_name[other_hosp_id] + ' just joined the network.')
   elif(msg.split()[0] =='beds'): #other nodes are requesting data to generate table
      pass
   else:
      print('Message from ',hosp_name[other_hosp_id] ,' is: ' ,msg)

def requestSend():
   global xtrans,next
   xtrans = input('Enter Command:\n')
   formatter()
   encrypted = encrypt(xtrans) 
   #need to extract[0] b/c RSA encode returns a tuple with one element as the encrypted message
   serverSocket.sendto(encrypted[0], next)
      
def lookatport():
   global msg, addr
   msg,addr = serverSocket.recvfrom(2048)  #wait to receive
   msg = decrypt(msg)

async def receiveandPrint():
   while True:
      lookatport()
      response = receivemsg()
      interpreter(msg)
      displayforme()
     
async def requestandSend():
   while True:
      try:
         requestSend()
      except IOError:
         print("err")

def start_loop(loop):
   asyncio.set_event_loop(loop)
   loop.run_forever()

loop1 = asyncio.new_event_loop()
t1 = Thread(target=start_loop, args=(loop1,))
loop2 = asyncio.new_event_loop()
t2 = Thread(target=start_loop, args=(loop2,))

t1.start()  ## 2 threads running parallel
t2.start()

asyncio.run_coroutine_threadsafe(receiveandPrint(),loop1)
asyncio.run_coroutine_threadsafe(requestandSend(),loop2)

   
  



