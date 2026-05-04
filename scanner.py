import socket
import threading
import time
from collections import defaultdict
from utils import validate_ip, get_service_name, banner_grab

class PortScanner:
    def __init__(self, target, start_port=1, end_port=1024, timeout=1, threads=50):
        """
        Initialize the port scanner.
        
        Args:
            target: Target IP address or hostname
            start_port: Starting port number
            end_port: Ending port number
            timeout: Socket timeout in seconds
            threads: Number of threads for concurrent scanning
        """
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.timeout = timeout
        self.threads = threads
        self.open_ports = []
        self.lock = threading.Lock()
        self.scanned_ports = 0
        self.total_ports = end_port - start_port + 1
        self.progress_callback = None
        
        # Resolve hostname if needed
        try:
            self.target_ip = socket.gethostbyname(target)
        except socket.gaierror:
            raise ValueError(f"Invalid IP address or hostname: {target}")
    
    def set_progress_callback(self, callback):
        """Set a callback function for progress updates."""
        self.progress_callback = callback
    
    def scan_port(self, port):
        """
        Scan a single port.
        
        Args:
            port: Port number to scan
            
        Returns:
            Dictionary with port info if open, None if closed
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            result = sock.connect_ex((self.target_ip, port))
            
            if result == 0:
                service = get_service_name(port)
                banner = banner_grab(self.target_ip, port, self.timeout)
                
                port_info = {
                    'port': port,
                    'service': service,
                    'banner': banner
                }
                
                with self.lock:
                    self.open_ports.append(port_info)
                
                return port_info
            
            sock.close()
        except socket.timeout:
            pass
        except Exception as e:
            print(f"Error scanning port {port}: {e}")
        
        finally:
            with self.lock:
                self.scanned_ports += 1
                if self.progress_callback:
                    self.progress_callback(self.scanned_ports, self.total_ports, port)
        
        return None
    
    def worker(self, port_queue):
        """
        Worker thread that processes ports from the queue.
        
        Args:
            port_queue: Queue of ports to scan
        """
        while True:
            try:
                port = port_queue.get(block=False)
                self.scan_port(port)
                port_queue.task_done()
            except:
                break
    
    def start_scan(self):
        """
        Start the port scanning process with multi-threading.
        
        Returns:
            List of open ports with their information
        """
        print(f"\n{'='*60}")
        print(f"🔍 PORT SCANNER")
        print(f"{'='*60}")
        print(f"Target: {self.target} ({self.target_ip})")
        print(f"Scanning ports: {self.start_port} - {self.end_port}")
        print(f"Threads: {self.threads}")
        print(f"Timeout: {self.timeout}s")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        
        # Create port queue
        port_queue = []
        for port in range(self.start_port, self.end_port + 1):
            port_queue.append(port)
        
        # Create and start threads
        thread_list = []
        for _ in range(min(self.threads, len(port_queue))):
            thread = threading.Thread(target=self._threaded_scan, args=(port_queue,))
            thread.daemon = True
            thread.start()
            thread_list.append(thread)
        
        # Wait for all threads to complete
        for thread in thread_list:
            thread.join()
        
        scan_time = time.time() - start_time
        
        return self.open_ports, scan_time
    
    def _threaded_scan(self, port_queue):
        """Helper method for threaded scanning."""
        while port_queue:
            try:
                port = port_queue.pop(0)
                self.scan_port(port)
            except IndexError:
                break
    
    def display_results(self, open_ports, scan_time):
        """
        Display scan results in a formatted way.
        
        Args:
            open_ports: List of open ports
            scan_time: Total scan time in seconds
        """
        print(f"\n{'='*60}")
        print(f"✅ SCAN RESULTS")
        print(f"{'='*60}\n")
        
        if open_ports:
            print(f"[OPEN PORTS FOUND: {len(open_ports)}]\n")
            for port_info in open_ports:
                port = port_info['port']
                service = port_info['service']
                banner = port_info['banner']
                
                print(f"  [OPEN] Port {port} → {service}")
                if banner:
                    print(f"         └─ {banner[:60]}")
        else:
            print("❌ No open ports found.")
        
        print(f"\n{'='*60}")
        print(f"⏱️  Scan completed in {scan_time:.2f} seconds")
        print(f"📊 Total ports scanned: {self.total_ports}")
        if open_ports:
            print(f"🎯 Open ports: {len(open_ports)}")
        print(f"{'='*60}\n")
        
        return open_ports
    
    def save_results(self, open_ports, scan_time, filename="scan_results.txt"):
        """
        Save scan results to a file.
        
        Args:
            open_ports: List of open ports
            scan_time: Total scan time
            filename: Output filename
        """
        try:
            with open(filename, 'w') as f:
                f.write("="*60 + "\n")
                f.write("PORT SCANNER RESULTS\n")
                f.write("="*60 + "\n\n")
                
                f.write(f"Target: {self.target} ({self.target_ip})\n")
                f.write(f"Port Range: {self.start_port} - {self.end_port}\n")
                f.write(f"Scan Time: {scan_time:.2f} seconds\n")
                f.write(f"Total Ports Scanned: {self.total_ports}\n\n")
                
                if open_ports:
                    f.write(f"OPEN PORTS ({len(open_ports)}):\n")
                    f.write("-"*60 + "\n")
                    for port_info in open_ports:
                        f.write(f"Port {port_info['port']}: {port_info['service']}\n")
                        if port_info['banner']:
                            f.write(f"  Banner: {port_info['banner']}\n")
                else:
                    f.write("No open ports found.\n")
                
                f.write("\n" + "="*60 + "\n")
            
            print(f"✅ Results saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {e}")


class QuickScan(PortScanner):
    """Quick scan of common ports."""
    
    COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5900, 8080, 8443]
    
    def __init__(self, target, timeout=1, threads=10):
        self.custom_ports = self.COMMON_PORTS
        super().__init__(target, 1, 65535, timeout, threads)
    
    def _threaded_scan(self, port_queue):
        """Override to use common ports only."""
        for port in self.custom_ports:
            self.scan_port(port)


class FullScan(PortScanner):
    """Full scan of all ports (1-65535)."""
    
    def __init__(self, target, timeout=1, threads=100):
        super().__init__(target, 1, 65535, timeout, threads)
