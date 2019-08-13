import socket
import sys
import json
import numpy as np

port = 8220
address = ('', port)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)
server_socket.listen(5)

print "Listening for client . . ."
conn, address = server_socket.accept()
print "Connected to client at ", address
#pick a large output buffer size because i dont necessarily know how big the incoming packet is                                                    
i=0
while i<10:
    output = conn.recv(2048);
    if output.strip() == "disconnect":
        conn.close()
        sys.exit("Received disconnect message.  Shutting down.")
        conn.send("dack")
	break
    elif output:
	print "Message received from client:"
        #print json.loads(output)
	json_load = json.loads(output)
	restored = np.asarray(json_load["data"])
	#print(restored)
	np.save("otherCameraCenter",restored)
        conn.send("ack")
        i=i+1                     
