import socket, sys

server_port = int(sys.argv[1]) if len(sys.argv) > 1 else 28333

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', server_port))

server_socket.listen()
while True:
    new_conn = server_socket.accept()
    new_socket = new_conn[0]
    response_list = []

    response = new_socket.recv(4096)
    while True:
        decoded = response.decode("ISO-8859-1")
        response_list.append(decoded)
        if "\r\n\r\n" in decoded: break
        response = new_socket.recv(4096)
    
    decoded_response = "".join(response_list)
    print(decoded_response)

    response_status = "HTTP/1.1 200 OK"
    content_type = "Content-Type: text/plain"
    content_len = "Content-Length: 6"
    connection = "Connection: close"
    content = "Hello!"

    header = "\r\n".join((response_status,content_type,content_len,connection)) 
    header += "\r\n" "\r\n" + content + "\r\n" + "\r\n"
    encoded_header = header.encode("ISO-8859-1") 
    new_socket.sendall(encoded_header)
    new_socket.close()

