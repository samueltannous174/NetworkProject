import os
from socket import *

serverPort = 7788

serverSocket = socket(AF_INET, SOCK_STREAM)        # bind TCP socket
serverSocket.bind(("", serverPort))
serverSocket.listen(1)

print("Server is ready to recieve")
while True:
    connectionSocket, addr = serverSocket.accept()         # accept connections from client

    sentence = connectionSocket.recv(1024).decode()               # recieve data

    print(addr)
    print(sentence)
    ip = addr[0]               # ipaddress of the client
    port = addr[1]                  # port of the client
    print("ip is " + str(ip))
    print("port is " + str(port))
    if not sentence:
        continue

    FirstLine = sentence.splitlines()[0]               # first line

    FirstLineWithoutSpaces = FirstLine.split(" ")      # split http header

    token = FirstLineWithoutSpaces[1]                     # path of the file
    tokenwithoutslash = token.split("/")[1]

    if token == "/" or token == "/index.html" or token == "/main_en.html" or token == "/en":      # here if the path of file does not have dot and only have specific value which we determined below

        connectionSocket.send("HTTP/1.1 200 OK \r\n".encode())                          # send response http headers
        connectionSocket.send("Content-Type: text/html \r\n".encode())
        connectionSocket.send("\r\n".encode())
        f1 = open("main_en.html", "rb")                              # open main_en file and read it's content
        connectionSocket.send(f1.read())                      # send the content of the file
        connectionSocket.close()                  # close client socket after sending data


    elif token == "/ar":                           # return main_ar file

        connectionSocket.send("HTTP/1.1 200 OK \r\n".encode())
        connectionSocket.send("Content-Type: text/html \r\n".encode())
        connectionSocket.send("\r\n".encode())
        f1 = open("main_ar.html", "rb")           # open main_ar file and read it's content
        connectionSocket.send(f1.read())            # send the content of the file
        connectionSocket.close()              # close client socket after sending data


    elif token == "/go":               # handle go redirect cases

        connectionSocket.send("HTTP/1.1 307 Temporary Redirect \r\n".encode())              # send response with status code 307 to the browser client
        connectionSocket.send("Location: https://www.google.com \r\n".encode())                # send new url for the redirected page
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()                   # close client socket after sending data


    elif token == "/so":                                   # handle so redirect cases

        connectionSocket.send("HTTP/1.1 307 Temporary Redirect \r\n".encode())                 # send response with status code 307 to the browser client
        connectionSocket.send("Location: https://www.stackoverflow.com \r\n".encode())                  # send new url for the redirected page
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()                       # close client socket after sending data


    # handle bzu redirect cases
    elif token == "/bzu":
        connectionSocket.send("HTTP/1.1 307 Temporary Redirect \r\n".encode())                   # send response with status code 307 to the browser client

        connectionSocket.send("Location: https://www.birzeit.edu/en/b-hub \r\n".encode())                 # send new url for the redirected page

        connectionSocket.send("\r\n".encode())
        connectionSocket.close()                 # close client socket after sending data


    # connectionSocket.send("HTTP/1.1 307 Temporary Redirect \r\n".encode())
    # connectionSocket.send("Location: https://www.google.com \r\n".encode())

    else:                                    #here only the path have dot in of its value and we also determined some of wanted values
        if os.path.isfile(tokenwithoutslash):        #check if the path exists
            tokenwithoutdotbefore = tokenwithoutslash.split(".")[0]                     # send normal file
            tokenwithoutdotafter = tokenwithoutslash.split(".")[1]

            if tokenwithoutdotafter == "html":                       # handle html file
                connectionSocket.send("HTTP/1.1 200 OK \r\n".encode())            # set Content-Type: text/html  for the response
                connectionSocket.send("Content-Type: text/html \r\n".encode())
                connectionSocket.send("\r\n".encode())     # read file as bytes

                f1 = open(tokenwithoutslash, "rb")
                connectionSocket.send(f1.read())                      # send content of the html file
                connectionSocket.close()

            elif tokenwithoutdotafter == "css":                  # handle css file

                connectionSocket.send("HTTP/1.1 200 OK \r\n".encode())                       # set Content-Type: text/css  for the response
                connectionSocket.send("Content-Type: text/css \r\n".encode())
                connectionSocket.send("\r\n".encode())
                f1 = open(tokenwithoutslash, "rb")                   # read file as bytes
                connectionSocket.send(f1.read())                      # send content of the html file
                connectionSocket.close()

            elif tokenwithoutdotafter == "png":                         # handle png file
                connectionSocket.send("HTTP/1.1 200 OK \r\n".encode())
                connectionSocket.send("Content-Type: image/png \r\n".encode())                    # set Content-Type: image/png
                connectionSocket.send("\r\n".encode())
                f1 = open(tokenwithoutslash, "rb")
                connectionSocket.send(f1.read())
                connectionSocket.close()

            elif tokenwithoutdotafter == "jpg":                     # handle jpg file
                connectionSocket.send("HTTP/1.1 200 OK \r\n".encode())
                connectionSocket.send("Content-Type: image/jpeg \r\n".encode())
                connectionSocket.send("\r\n".encode())
                f1 = open(tokenwithoutslash, "rb")
                connectionSocket.send(f1.read())
                connectionSocket.close()            # handle 404 page not found case
            else:
                connectionSocket.send("“HTTP/1.1 200 OK \r\n".encode())
                connectionSocket.send("Content-Type: text/html \r\n".encode())
                connectionSocket.send("\r\n".encode())
                f1 = open("404.html", "rb")                       # send 404 html page
                connectionSocket.send(f1.read())
                connectionSocket.close()

        else:
            connectionSocket.send("HTTP/1.1 404 Not Found \r\n".encode())                   # handle error file
            connectionSocket.send("Content-Type: text/html \r\n".encode())
            connectionSocket.send("\r\n".encode())
            f1 = open("404.html", "rb")
            errorFile = open("404.html", "w")                     # Creating an HTML file
            # error file content html
            # Adding input data to the HTML file
            errorFile.write("<!DOCTYPE html> \
                            <html> \
                            <head> \
                            <title>Error</title> \
                            <style> \
                                .ForPort{ \
                                    font - weight: bold; \
                                } \
                            </style> \
                            </head> \
                            <body> \
                            <h1 align=""center"" style=""color:red;""> \
                            <br><br><br><br><br><br> ""The file is not found"" <br> \
                            </h1> \
                            <h2 align=""center"" class=""h2""> \
                             ""Ayman Salama 1200488"" <br> \
                             ""Ahmad Bakri 1201509"" <br> \
                             ""Samuel Tannous 1201123"" <br> \
                            </h2> \
                            </body> \
                            </html>")
            errorFile.write("<br><br><h1 class=""ForPort"">IP is </h1>" + str(ip))
            errorFile.write("<h1 class=""ForPort"">port is </h1>" + str(port))
            errorFile.close()                 # Saving the data into the HTML file
            connectionSocket.send(f1.read())               # send file
            connectionSocket.close()                # close connection