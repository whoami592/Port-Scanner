import socket
import threading
import time
from queue import Queue

# Anonymous Hacker Style Banner
def print_banner():
    banner = """
    ╔════════════════════════════════════════════════════╗
    ║                                                    ║
    ║       ANONYMOUS HACKER STYLE PORT SCANNER          ║
    ║                                                    ║
    ╚════════════════════════════════════════════════════╝
         ╔═╗  ╔═╗  ╔═╗  ╔╦╗  ╔═╗  ╔═╗  ╔═╗  ╔═╗
         ║╩╠═╦╦╗  ║╩╠═╦╦╗╔╦╦╗  ╚╦╦╗  ╚╦╦╗  ║╬║  ╚╦╦╗
         ║╦║╬║╬╬╗ ║╦║╬║╬╬╩╩╩╩   ║╩╬═╦╦╦╦╗  ║╬╬═╦╦╦╦╦╦╦╦╦╗
         ╚╩╩╩╩╬╬╬ ╚╩╩╩╩╩╬╦╦╦╗  ╚╦╦╬╩╩╩╩╩  ╚╩╩╩╩╩╩╩╩╩╩╩╝
         ╚════╩╩╬╬ ╔╦╦╦╦╦╦╦╦╦╦╦╗ ╚╩╩╩╩╩╩╩╩╩ ╚╩╩╩╩╩╩╩╩╩╩
               ╩╩╩ ╚╩╩╩╩╩╩╩╩╩╩╩╝
    ╔════════════════════════════════════════════════════╗
    ║  CODED BY: Pakistani Ethical Hacker Mr. Sabaz Ali Khan  ║
    ║  PURPOSE: Ethical Network Analysis Tool            ║
    ║  USE RESPONSIBLY AND WITH PERMISSION ONLY          ║
    ╚════════════════════════════════════════════════════╝
    """
    print(banner)

# Port Scanner Function
def scan_port(ip, port, open_ports):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    except:
        pass

# Worker Thread Function
def threader(ip, queue, open_ports):
    while True:
        port = queue.get()
        scan_port(ip, port, open_ports)
        queue.task_done()

# Main Scanning Function
def scan(ip, start_port=1, end_port=1024, num_threads=100):
    print(f"[*] Scanning {ip} from port {start_port} to {end_port}...")
    queue = Queue()
    open_ports = []
    
    # Start threads
    for _ in range(num_threads):
        t = threading.Thread(target=threader, args=(ip, queue, open_ports))
        t.daemon = True
        t.start()
    
    # Fill queue with ports
    for port in range(start_port, end_port + 1):
        queue.put(port)
    
    # Wait for queue to empty
    queue.join()
    
    # Print results
    if open_ports:
        print(f"\n[+] Open ports found: {sorted(open_ports)}")
    else:
        print("\n[-] No open ports found.")
    return open_ports

# Main Program
def main():
    print_banner()
    time.sleep(1)
    
    try:
        target = input("[*] Enter target IP or hostname: ")
        start_port = int(input("[*] Enter start port (default 1): ") or 1)
        end_port = int(input("[*] Enter end port (default 1024): ") or 1024)
        
        # Resolve hostname to IP
        ip = socket.gethostbyname(target)
        print(f"[*] Resolved {target} to {ip}")
        
        start_time = time.time()
        scan(ip, start_port, end_port)
        print(f"[*] Scan completed in {time.time() - start_time:.2f} seconds")
        
    except KeyboardInterrupt:
        print("\n[!] Scan aborted by user.")
    except Exception as e:
        print(f"\n[!] Error: {e}")

if __name__ == "__main__":
    main()