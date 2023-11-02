import socket, time
address = "time.nist.gov"
port = 37

client_socket = socket.socket()
client_socket.connect((address,port))


response = client_socket.recv(4096)

time_from_nist = int.from_bytes(response,"big")
seconds_delta = 2208988800
seconds_since_unix_epoch = int(time.time())
seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

print(time_from_nist)
print(seconds_since_1900_epoch)
print("difference:", abs(time_from_nist - seconds_since_1900_epoch))
client_socket.close()

