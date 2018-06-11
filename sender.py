import os
import socket
import sys
import time

#ServerIP = sys.argv[1]
#ServerPORT = int(sys.argv[2])
#filePath = sys.argv[3]
#40.74.129.169 -> azure ip
ServerIP = '40.74.129.169'
ServerPORT = 5005
filePath = '/home/u201203406/Desktop/packet.py'
addr = (ServerIP, ServerPORT)

buff = 1024
frameNumber = 0
current_size = 0
ACK = 0
#if len(sys.argv) < 3:
#	print '[Dest IP Addr] [ Dest Port] [File Path]'
#	sys.exit()


try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    fileName = os.path.basename(filePath)
    fileSize = os.path.getsize(filePath)
    data = fileName +"|||"+ str(fileSize)
    sock.sendto(data, addr)

    f = open(filePath, 'rb')
    data = f.read(buff-1)
    data = str(frameNumber) + data

    while True:
        sock.sendto(data, addr)
        current_size = current_size + len(data)-1           
        if current_size >= fileSize:
            current_size = fileSize
        rate = round(float(current_size) / float(fileSize) * 100,2)
        print current_size, "/", fileSize, rate , "%\n"

        if current_size == fileSize:
            print "Success"
            break
        while not ACK:
            try:
                ACK, address = sock.recvfrom(buff)
                data = f.read(buff-1)
                frameNumber = (frameNumber + 1)%2
                data = str(frameNumber) + data
                ACK = 1
            except socket.timeout:
                print "Time Out"
                sock.sendto(data, addr)

        print "Recieved ACK : " ,  ACK

    sock.close()
    f.close()

except socket.error as e:
    print e
    sys.exit()

