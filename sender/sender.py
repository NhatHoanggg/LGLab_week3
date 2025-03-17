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

        message = args[0]
        execution_time = end_time - start_time
        if execution_time > 0 and message:
            data_size = len(message) 
            throughput = data_size / execution_time if execution_time > 0 else 0
            print(f"Throughput: {throughput:.2f} bytes/s")

        print(f"Execution Time: {end_time*1000 - start_time*1000:.3f} ms")
        #print(f"CPU Usage: {cpu_after - cpu_before:.2f}%")
        return result
    return wrapper

@measure_performance
def send_ipv4_unicast(message, target_ip):
    PORT = 5000
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(message.encode(), (target_ip, PORT))
    print(f"Sent message to {target_ip}:{PORT}")

@measure_performance
def send_ipv4_broadcast(message):
    BROADCAST_IP = '255.255.255.255'
    PORT = 5001
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(message.encode(), (BROADCAST_IP, PORT))
    print(f"Sent message to {BROADCAST_IP}:{PORT}")

@measure_performance
def send_ipv4_multicast(message):
    MULTICAST_GROUP = '224.12.1.1'
    PORT = 5002
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.sendto(message.encode(), (MULTICAST_GROUP, PORT))
    print(f"Sent message to {MULTICAST_GROUP}:{PORT}")

@measure_performance
def send_ipv6_unicast(message, target_ip):
    #target = 'fe80::da3a:ddff:fea4:beb8%eth0'
    target = 'fd80:abcd:1234::12'  # Ä á»‹a chá»‰ toÃ n cá»¥c IPv6
    PORT = 6000
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
        s.sendto(message.encode(), (target, PORT))
    print(f"Sent message to {target_ip}:{PORT}")

@measure_performance
def send_ipv6_multicast(message):
    MULTICAST_GROUP = 'ff02::1'
    PORT = 6001
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 2)
    sock.sendto(message.encode(), (MULTICAST_GROUP, PORT))
    print(f"Sent message to {MULTICAST_GROUP}:{PORT}")

@measure_performance
def send_ipv6_anycast(message):
    ANYCAST_ADDRESS = 'fd80:abcd:4567::20'	
    PORT = 6002
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
        s.sendto(message.encode(), (ANYCAST_ADDRESS, PORT))
    print(f"Sent message to {ANYCAST_ADDRESS}:{PORT}")

def run_menu():
    while True:
        print("1. IPv4 Unicast\n"+
              "2. IPv4 Broadcast\n"+
              "3. IPv4 Multicast\n"+
              "4. IPv6 Unicast\n"+
              "5. IPv6 Multicast\n"+
              "6. IPv6 Anycast\n"+
              "0. Exit\n")
        try:
            option = int(input("Pick your option: "))
            if option == 0:
                break
            message = input("Enter your message: ")
            if option == 1:
                target_ip = input("Enter target IPv4 address: ")
                send_ipv4_unicast(message, target_ip)
            elif option == 2:
                send_ipv4_broadcast(message)
            elif option == 3:
                send_ipv4_multicast(message)
            elif option == 4:
                target_ip = input("Enter target IPv6 address: ")
                send_ipv6_unicast(message, target_ip)
            elif option == 5:
                send_ipv6_multicast(message)
            elif option == 6:
                send_ipv6_anycast(message)
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    run_menu() 