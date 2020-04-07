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

#Generate hospital data
hosp_id = 1
hosp_code = ["MAYO", "MAST", "ADVH", "METO", "CEDS"]
hosp_name = ["Mayo Clinic Hospital", "Massachusetts General Hospital", "AdventHealth Orlando",
"Methodist Hospital", "Cedars-Sinai Medical Center"]

#Data initliasation
num_beds = 5000 - 100
num_free_beds = num_beds - 800
print("Number of beds ->", num_beds)
print("Number of unoccupied beds ->", num_free_beds)

def interpreter(dmsg):
   global hosp_id, next, num_free_beds
   dmsg_arr = dmsg.split()

   if dmsg_arr[0] == "ID": #assigning ID to this hospital
      hosp_id = int(dmsg_arr[1])
      print("My ID is", hosp_id)
      print("Abreviation->", hosp_code[hosp_id])
      print("Hospital Name->", hosp_name[hosp_id])

   elif dmsg_arr[0] == "beds": #recieved a bed message
      if dmsg_arr[1] != str(hosp_id):
         pasmsg = dmsg #passing message
         #adjust number of free beds for sense of realism
         num_free_beds = num_free_beds
         #attach this hospital's data
         pasmsg = pasmsg + " " + str(hosp_id) + " " + str(num_beds) + " " + str(num_free_beds)
         encrypted = encrypt(pasmsg)
         serverSocket.sendto(encrypted[0], next)
      else:
         table(dmsg)


def table(ctable):
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
      print("beds message:", test)
      xtrans = test

def encrypt(msg):
   bytes_msg = msg.encode()
   enc_data = publickey.encrypt(bytes_msg, 16) #encrypt message with public key
   return enc_data


def decrypt(msg):
   # retrieve exported private key from file
   file = open("Keys.txt", "r")
   privateKeyString = file.read() 
   file.close()
   privatekey = RSA.importKey(privateKeyString,passphrase = "savelives")
   dec_data = privatekey.decrypt(msg)
   dec_data = str(dec_data.decode())
   return dec_data

try: 
   serverSocket.sendto(encrypt(str(xtrans))[0], (Host, Port))  #check if already exists
except: print('Waiting For Hospital to Join network...')


def receivemsg():
   global next, next_set,msg
   if next_set == 0: #should be 0 set up node/client
      next_set =1
   return 0

def scanforchangeNext():
   global next,msg
   #hopefully msg is for this node...
   
   charmsg = [] 
   charmsg[:0] = msg

   if(next == (Host,Port) and charmsg[0] == '('):      #if msg received is about to go to host then point to included ip address!!!
      newaddrr = msg.split("-999")
      newerAddr = newaddrr[0].split(",")
      newhost = str(newerAddr[0]).split("'")
      newport = str(newerAddr[1]).split(")")
      encrypted = encrypt(str(xtrans))
      serverSocket.sendto(encrypted[0], (str(newhost[1]), int(newport[0])))
      next = (str(newhost[1]), int(newport[0]))
      return 1
   return 0

def passOn():
   global msg,next_set
   charmsg = [] 
   charmsg[:0] = msg
   if(charmsg[0] == '('):     #if already formatted but not for me
      encrypted = encrypt(msg)
      serverSocket.sendto(encrypted[0], next)
      return 1
   return 0

def displayforme():
   global addr,msg, xtrans,next, hosp_id
   print('Message from ',hosp_name[hosp_id-1] ,' is: ' ,msg)

def inputSend():
   global xtrans
   xtrans = input('Enter Available hospital beds:\n')
   formatter()
   encrypted = encrypt(xtrans) 
   xtrans = encrypted[0]
   serverSocket.sendto(encrypted[0], next)

def lookatport():
   global msg, addr
   msg,addr = serverSocket.recvfrom(2048)  #wait to receive

async def receiveandPrint():
   global msg
   while True:
      lookatport()
      msg = decrypt(msg)
      receivemsg() 
      interpreter(msg)
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


   
