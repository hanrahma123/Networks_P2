## How to Run
1. Make sure you have Python3 installed and the Pycrypto library.
2. open a terminal window and navigate to the folder containing p2p1.py and p2pn.py. Run p2p1.py in python3
```shell
python3 p2p1.py
Hospital Name: Mayo Clinic Hospital(MAYO) with id: 0
Number of total beds -> 1447
Number of unoccupied beds -> 447
Waiting For Hospitals to join network...
Enter Command:
```
This simulates the first hospital, Mayo Hospital, joining the network.

3. open another terminal window and navigate to the same folder and run p2pn.py. 
```shell
python3 p2pn.py
Number of total beds ->  2517
Number of unoccupied beds ->  1717
Enter Command:
Hospital Name: Massachusetts General Hospital(MAST) with id: 1
```
This simulates a new hospital joining the network.

4. You can open a new terminal and p2pn.py up to 4 times to simulate more hospitals joining the peer-to-peer network

## Test cases
1. send any message from one node to another. The most recently joined hospital will send a message to the first hospital. The recieving hospital then prints out the message.

Mayo Clinic Hospital Terminal
```shell
Enter Command:
What kind of ventillators are you using?
```
Mass General Hospital Terminal
```shell
Message from Mayo Clinic Hospital: What kind of ventillators are you using?
```

2. view distributed database table of all hospitals in network by entering command "beds" followed by any string.
```shell
Enter Command:
beds ?
```

3. request information from a specific hospital by entering command "beds" followed by the hospital abbreviation ("MAYO", "MAST", "ADVH", "METO", "CEDS"). This will display the distributed database table with the selected hospital highlighted. The selected hospital must already be active in the network.

MAYO Terminal
```shell
Enter Command:
beds MAST
```
