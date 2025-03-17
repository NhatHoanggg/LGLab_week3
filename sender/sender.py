import socket
import time
import psutil

def measure_performance(func):
    """Decorator measuring the efficiency"""
    def wrapper(*args, **kwargs):
        process = psutil.Process()
        cpu_before = process.cpu_percent(interval=None)
        mem_before = process.memory_info().rss

        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        cpu_after = process.cpu_percent(interval=None)
        mem_after = process.memory_info().rss

        # print(f"Performance Metrics:")
        print(f"Execution Time: {end_time - start_time:.6f} seconds")
        # print(f"CPU Usage: {cpu_after - cpu_before:.2f}%")
        # print(f"Memory Usage: {(mem_after - mem_before) / 1024:.2f} KB")
        # print("-" * 50)

        return result
    return wrapper

@measure_performance
def send_ipv4_unicast():
    TARGET_IP = '10.12.1.22'  
    PORT = 5000
    MESSAGE = "Hello Ipv4 Unicast!"
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(MESSAGE.encode(), (TARGET_IP, PORT))
        print(f"Sent message to {TARGET_IP}:{PORT}")

@measure_performance
def send_ipv4_broadcast():
    BROADCAST_IP = '255.255.255.255'
    PORT = 5001
    MESSAGE = "Hello Ipv4 Broadcast!"
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(MESSAGE.encode(), (BROADCAST_IP, PORT))
        print(f"Broadcast message sent to {BROADCAST_IP}:{PORT}")

@measure_performance
def send_ipv4_multicast():
    MULTICAST_GROUP = '224.0.0.1'
    PORT = 5002
    MESSAGE = "Hello Ipv4 Multicast!"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    sock.sendto(MESSAGE.encode(), (MULTICAST_GROUP, PORT))
    print(f"Sent multicast message to {MULTICAST_GROUP}:{PORT}")

@measure_performance
def send_ipv6_unicast():
    TARGET_IP = 'fe80::da3a:ddff:fea4:bfbe%eth0'  
    PORT = 6000
    MESSAGE = "Hello IPv6 Unicast!"

    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
        s.sendto(MESSAGE.encode(), (TARGET_IP, PORT))
        print(f"Sent message to {TARGET_IP}:{PORT}")

@measure_performance
def send_ipv6_multicast():
    MULTICAST_GROUP = 'ff02::1'
    PORT = 6001
    MESSAGE = "Hello IPv6 Multicast!"
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 2)

    sock.sendto(MESSAGE.encode(), (MULTICAST_GROUP, PORT))
    print(f"Sent multicast message to {MULTICAST_GROUP}:{PORT}")

@measure_performance
def send_ipv6_anycast():
    """Sends a message to the nearest IPv6 Anycast node."""
    ANYCAST_ADDRESS = '2001:db8::1'  # Replace with your configured IPv6 Anycast address
    PORT = 6002
    MESSAGE = "Hello IPv6 Anycast!"
    
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
        s.sendto(MESSAGE.encode(), (ANYCAST_ADDRESS, PORT))
        print(f"Sent Anycast message to {ANYCAST_ADDRESS}:{PORT}")

def run_menu():
    option = 0
    print("Enter 1 for IPv4 Unicast\n"+
        "Enter 2 for IPv4 Broadcast\n"+
        "Enter 3 for IPv4 Multicast\n"+
        "Enter 4 for IPv6 Unicast\n"+
        "Enter 5 for IPv6 Multicast\n"+
        "Enter 6 for IPv6 Anycast\n"+
        "Enter 0 to exit\n")
    while True:
        try:
            option = int(input("Pick your option: "))
            if option == 1:
                send_ipv4_unicast()
            elif option == 2:
                send_ipv4_broadcast()
            elif option == 3:
                send_ipv4_multicast()
            elif option == 4:
                send_ipv6_unicast()
            elif option == 5:
                send_ipv6_multicast()
            elif option == 6:
                send_ipv6_anycast()
            elif option == 0:
                break
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    run_menu()