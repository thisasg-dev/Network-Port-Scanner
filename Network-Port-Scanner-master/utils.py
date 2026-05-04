import socket
import re

# Common port to service mapping
PORT_SERVICE_MAP = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    9200: "Elasticsearch",
    27017: "MongoDB",
    6379: "Redis",
}

def validate_ip(ip_string):
    """
    Validate if the given string is a valid IP address.
    
    Args:
        ip_string: IP address string
        
    Returns:
        True if valid, False otherwise
    """
    # IPv4 pattern
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    
    if re.match(ipv4_pattern, ip_string):
        parts = ip_string.split('.')
        for part in parts:
            if int(part) > 255:
                return False
        return True
    
    # Try hostname resolution
    try:
        socket.gethostbyname(ip_string)
        return True
    except socket.gaierror:
        return False


def get_service_name(port):
    """
    Get service name for a given port.
    
    Args:
        port: Port number
        
    Returns:
        Service name string
    """
    # Try using system service database first
    try:
        service = socket.getservbyport(port)
        return service.upper()
    except OSError:
        pass
    
    # Fall back to custom mapping
    if port in PORT_SERVICE_MAP:
        return PORT_SERVICE_MAP[port]
    
    return "UNKNOWN"


def banner_grab(host, port, timeout=2):
    """
    Attempt to grab banner from open port.
    
    Args:
        host: Target IP address
        port: Target port
        timeout: Socket timeout in seconds
        
    Returns:
        Banner string or None
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        
        try:
            banner = sock.recv(1024)
            if banner:
                return banner.decode('utf-8', errors='ignore').strip()[:100]
        except socket.timeout:
            pass
        
        sock.close()
    except Exception:
        pass
    
    return None


def get_hostname(ip):
    """
    Get hostname from IP address.
    
    Args:
        ip: IP address
        
    Returns:
        Hostname or None
    """
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except socket.herror:
        return None


def parse_port_range(range_string):
    """
    Parse port range string (e.g., "80,443,8080-8090").
    
    Args:
        range_string: Port range string
        
    Returns:
        List of port numbers
    """
    ports = []
    
    for part in range_string.split(','):
        part = part.strip()
        
        if '-' in part:
            try:
                start, end = part.split('-')
                start, end = int(start.strip()), int(end.strip())
                ports.extend(range(start, end + 1))
            except ValueError:
                continue
        else:
            try:
                ports.append(int(part))
            except ValueError:
                continue
    
    return sorted(list(set(ports)))


def format_size(bytes_size):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} TB"
