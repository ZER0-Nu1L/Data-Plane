from socket import *

#Prepare a sever socket
serverSocket = socket(AF_INET,SOCK_STREAM)
serverPort = 12000
serverSocket.bind(('',serverPort)) 
serverSocket.listen(1)

while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        #Get required message
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()

        #Send one HTTP header line into socket
        connectionSocket.send('HTTP/1.1 200 OK'.encode())

        #Send the content of the requested file
        for i in range(0,len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

    except IOError:
        #Send response message for file not found
        connectionSocket.send('404 Not Found'.encode())
        #Close client socket
        connectionSocket.close()
serverSocket.close()
#Terminate the program
sys.exit()
