import socket,sys


address = sys.argv[1]
port = int(sys.argv[2]) if len(sys.argv) > 2 else 80

client_socket = socket.socket()
client_socket.connect((address,port))


method = "GET / HTTP/1.1"
host = "Host: " + address
connection = "Connection: close"

header = "\r\n".join((method,host,connection)) + "\r\n" + "\r\n"
encoded_header = header.encode("ISO-8859-1")
client_socket.sendall(encoded_header)

response_list = []
response = client_socket.recv(4096)
while len(response) != 0:
    response_list.append(response)
    response = client_socket.recv(4096)

decoded_response = "".join([ b.decode("ISO-8859-1") for b in response_list])
print(decoded_response)

client_socket.close()

