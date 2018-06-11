import socket
import os
import sys
import time

#ServerIP = sys.argv[1]
#ServerPORT = int(sys.argv[2])
#filePath = sys.argv[3]
#40.74.129.169 -> azure ip
ServerIP =''
ServerPORT = 5005

buff = 1024
current_size = 0
ACK = 0
#if len(sys.argv) < 3:
#	print '[Dest IP Addr] [ Dest Port] [File Path]'
#	sys.exit()

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((ServerIP, ServerPORT))

	data, addr = sock.recvfrom(buff)
	
	fileName, total_size = data.split("|||")
	print "Received File : ", fileName
	f = open(fileName, 'wb')

	total_size = int(total_size)
		
		
	while True:
		sock.settimeout(3)
		try:
			data, addr = sock.recvfrom(buff)	
			if int(data[0]) == ACK:
				ACK = (ACK + 1)%2
				sock.sendto(str(ACK), addr)
		except socket.timeout:
			print "Time Out"

		current_size = current_size + len(data)-1
		if current_size >= total_size:
			current_size = total_size
		rate = round(float(current_size) / float(total_size)*100, 2)
		print current_size, "/", total_size, rate, "%\n"
		f.write(data)
		if current_size == total_size:
			print "Success"
			break

	sock.close()
	f.close()


except socket.errno as e:
	print e
	sys.exit()
