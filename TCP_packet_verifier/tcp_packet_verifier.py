import os

# Converts a dot delimited ip address to bytes
def ip_to_bytes(address:str) -> bytes:
    return b''.join([int(x).to_bytes() for x in address.split(".")])

def get_tcp_data(file_name:str) -> bytes:
    file_path = os.path.join("tcp_data", file_name)
    with open(file_path, "rb") as fp:
        tcp_data = fp.read()
    return tcp_data

def get_source_and_destination_ip(file_name:str) -> list[str]:
    file_path = os.path.join("tcp_data", file_name)
    with open(file_path, 'r') as file:
        first_line = file.readline()

    return first_line.split() 

def construct_pseudo_header(source_ip:str, destination_ip:str, tcp_length:int) -> bytes:
    source_ip_bytes = ip_to_bytes(source_ip)
    destination_ip_bytes = ip_to_bytes(destination_ip)
    zero = b'\x00'
    protocol = b'\x06'
    return source_ip_bytes + destination_ip_bytes + zero + protocol + tcp_length.to_bytes(2, 'big')

def checksum(psuedo_header: bytes, tcp_zero_cksum: bytes)-> int:
    if len(tcp_zero_cksum) % 2 == 1:
        tcp_zero_cksum += b'\x00'
    
    data = psuedo_header + tcp_zero_cksum 
    total = 0
    for i in range(0,len(data),2):
        word = int.from_bytes(data[i:i+2], "big")
        
        total += word
        total = (total & 0xffff) + (total >> 16)
        
    return (~total) & 0xffff 



def main(ip_file_name:str, tcp_data_file_name:str):
    source_ip_address, destination_ip_address = get_source_and_destination_ip(ip_file_name)
    tcp_data = get_tcp_data(tcp_data_file_name)
    pseudo_header = construct_pseudo_header(source_ip_address,destination_ip_address, len(tcp_data)) 
    original_cksum = int.from_bytes(tcp_data[16:18], 'big')

    tcp_zero_cksum = tcp_data[:16] + b'\x00\x00' + tcp_data[18:]
    
    calculated_cksum = checksum(pseudo_header,tcp_zero_cksum)
    
    if calculated_cksum == original_cksum: return "PASS"
    else: return "FAIL"


def test():
    print("Running tests...")

    print("test 1:")
    ip_input = "1.2.3.4"
    expected_output = b'\x01\x02\x03\x04'
    result = ip_to_bytes(ip_input) 
    if result == expected_output:
        print("Passed!")
    else: 
        print("Failed!")
        print(f"expected: {expected_output}, recieved: {result}")

    print("test 2:")
    inputs = ("255.0.255.1", "127.255.0.1", 3490)
    expected_output = b'\xff\x00\xff\x01\x7f\xff\x00\x01\x00\x06\x0d\xa2'
    result = construct_pseudo_header(*inputs)

    if expected_output == result:
        print("Passed!")
    else:
        print("Failed!")
        print(f"expected: {expected_output}, recieved: {result}")

    print("Running file tests...")
    tcp_adder = "tcp_addrs_"
    tcp_data = "tcp_data_"
    for i in range(10):
        adder_file = tcp_adder + str(i) + ".txt"
        data_file = tcp_data + str(i) + ".dat"
        result = main(adder_file, data_file)
        if (i <= 4 and result == "PASS") or (i > 4 and result == "FAIL"): print("Passed!")
        else:
            print("Failed!")

test()

