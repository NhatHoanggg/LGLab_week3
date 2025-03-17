import socket
import struct
import threading

def handle_ipv4_unicast():
    host, port = '0.0.0.0', 5000
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        print(f"Listening for IPv4 Unicast messages on {host}:{port}...")
        while True:
            data, addr = s.recvfrom(1024)
            print(f"[IPv4 Unicast] From {addr}: {data.decode()}")

def handle_ipv4_broadcast():
    host, port = '0.0.0.0', 5001
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        print(f"Listening for IPv4 Broadcast messages on {port}...")
        while True:
            data, addr = s.recvfrom(1024)
            print(f"[IPv4 Broadcast] From {addr}: {data.decode()}")

def handle_ipv4_multicast():
    multicast_group, port = '224.12.1.1', 5002
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    mreq = struct.pack("4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    print(f"Listening for IPv4 Multicast messages on {multicast_group}:{port}...")
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"[IPv4 Multicast] From {addr}: {data.decode()}")

def handle_ipv6_unicast():
    host, port = '::', 6000
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        print(f"Listening for IPv6 Unicast messages on {host}:{port}...")
        while True:
            data, addr = s.recvfrom(1024)
            print(f"[IPv6 Unicast] From {addr}: {data.decode()}")

def handle_ipv6_multicast():
    multicast_group, port = 'ff02::1', 6001
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    group = socket.inet_pton(socket.AF_INET6, multicast_group)
    mreq = group + struct.pack('@I', 0)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
    print(f"Listening for IPv6 Multicast messages on {multicast_group}:{port}...")
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"[IPv6 Multicast] From {addr}: {data.decode()}")

def handle_ipv6_anycast():
    host, port = '::', 6002
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        print(f"Listening for IPv6 Anycast messages on {host}:{port}...")
        while True:
            data, addr = s.recvfrom(1024)
            print(f"[IPv6 Anycast] From {addr}: {data.decode()}")

# Run all listeners in separate threads
threads = [
    threading.Thread(target=handle_ipv4_unicast),
    threading.Thread(target=handle_ipv4_broadcast),
    threading.Thread(target=handle_ipv4_multicast),
    threading.Thread(target=handle_ipv6_unicast),
    threading.Thread(target=handle_ipv6_multicast),
    threading.Thread(target=handle_ipv6_anycast),
]

for thread in threads:
    thread.daemon = True
    thread.start()

# Ensure all threads have started before printing the message
for thread in threads:
    while not thread.is_alive():
        pass

print("All listeners are running. Press Ctrl+C to stop.")

# Keep the main thread alive
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Stopping all listeners.")