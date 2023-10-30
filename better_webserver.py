import socket, sys, os
from typing import Optional

def get_file_data(file_name:str):
    try:
        with open(file_name, "rb") as fp:
            data = fp.read() # Read entire file
            file_extension = os.path.splitext(file_name)[-1]
            file_type = None
            match file_extension:

                case ".txt": 
                    file_type = "text/plain"

                case ".html": 
                    file_type = "text/html"
            
        return (data, file_type, len(data))
    except:
        return None, None, 0

def build_response(data:Optional[bytes], file_type:Optional[str], file_len:int):
    encoded_response = None

    match data:

        case None:
            response_status = "HTTP/1.1 404 Not Found"
            content_type = "Content-Type: text/plain"
            content_len = "Content-Length: 13"
            connection = "Connection: close"
            content = "404 not found"
            
            header = "\r\n".join((response_status,content_type,content_len,connection))

            response = header + "\r\n\r\n" + content + "\r\n\r\n"
            
            encoded_response = response.encode("ISO-8859-1")

        case _:
            response_status = "HTTP/1.1 200 OK"
            content_type = "Content-Type: " + file_type if file_type else ""
            content_len = "Content-Length: " + str(file_len)
            connection = "Connection: close"
            
            header = "\r\n".join((response_status,content_type,content_len,connection))
            response = header + "\r\n\r\n"
            encoded_response = response.encode("ISO-8859-1")

            encoded_response = encoded_response + data + "\r\n\r\n".encode("ISO-8859-1")
    
    
    return encoded_response

        

server_port = int(sys.argv[1]) if len(sys.argv) > 1 else 33490

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
    
    decoded_request = "".join(response_list)
    print(decoded_request)
    header = decoded_request.split("\r\n")[0].split()
    file_name = header[1].split("/")[-1]
    file_data, file_type, file_len = get_file_data(file_name)
    encoded_response = build_response(file_data,file_type,file_len)
    new_socket.sendall(encoded_response)
    new_socket.close()
