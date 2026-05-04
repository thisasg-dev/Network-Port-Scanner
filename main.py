
"""
Network Port Scanner - CLI Version
Scan for open ports on a target IP address
"""

import sys
import os
from scanner import PortScanner, QuickScan, FullScan
from utils import validate_ip, get_hostname

def print_banner():
    """Print application banner."""
    print("\n" + "="*60)
    print("  🔍 NETWORK PORT SCANNER 🔍")
    print("="*60)
    print("Scan open ports on any IP address")
    print("(Only scan YOUR OWN systems or authorized networks)")
    print("="*60 + "\n")


def get_ip_input():
    """Get and validate IP address from user."""
    while True:
        target = input("Enter target IP address or hostname: ").strip()
        
        if not target:
            print("❌ IP address cannot be empty!")
            continue
        
        if validate_ip(target):
            return target
        else:
            print("❌ Invalid IP address or hostname!")


def get_port_range_input():
    """Get port range from user with preset options."""
    print("\n📊 Scan Mode Selection:")
    print("1. Quick Scan (common ports)")
    print("2. Full Scan (1-65535)")
    print("3. Custom Range")
    print("4. Specific Ports (comma-separated)")
    
    choice = input("\nSelect mode (1-4): ").strip()
    
    if choice == '1':
        return 'quick', None, None
    elif choice == '2':
        return 'full', None, None
    elif choice == '3':
        while True:
            try:
                start = int(input("Enter start port (1-65535): ").strip())
                end = int(input("Enter end port (1-65535): ").strip())
                
                if 1 <= start <= 65535 and 1 <= end <= 65535 and start <= end:
                    return 'custom', start, end
                else:
                    print("❌ Invalid port range!")
            except ValueError:
                print("❌ Please enter valid numbers!")
    elif choice == '4':
        ports_str = input("Enter ports (e.g., 22,80,443,8080-8090): ").strip()
        try:
            ports = []
            for part in ports_str.split(','):
                if '-' in part:
                    s, e = part.split('-')
                    ports.extend(range(int(s), int(e) + 1))
                else:
                    ports.append(int(part))
            return 'specific', ports, None
        except ValueError:
            print("❌ Invalid port format!")
            return get_port_range_input()
    else:
        print("❌ Invalid choice!")
        return get_port_range_input()


def get_scan_options():
    """Get additional scan options."""
    print("\n⚙️  Scan Options:")
    
    try:
        timeout = float(input("Socket timeout in seconds (default 1): ").strip() or "1")
        threads = int(input("Number of threads (default 50): ").strip() or "50")
        
        if timeout <= 0:
            timeout = 1
        if threads <= 0:
            threads = 50
        if threads > 200:
            threads = 200  # Safety limit
        
        return timeout, threads
    except ValueError:
        return 1, 50


def display_progress(scanned, total, current_port):
    """Display scanning progress."""
    percentage = (scanned / total) * 100
    progress_bar = f"[{'█' * int(percentage/5)}{' ' * (20 - int(percentage/5))}]"
    print(f"\r🔄 Scanning... {progress_bar} {percentage:.1f}% (Port {current_port})", end='', flush=True)


def main():
    """Main CLI application."""
    try:
        print_banner()
        
        # Get target IP
        target_ip = get_ip_input()
        
        # Display resolved IP if hostname was used
        try:
            import socket
            resolved_ip = socket.gethostbyname(target_ip)
            if resolved_ip != target_ip:
                print(f"✅ Resolved to: {resolved_ip}")
            
            # Try to get hostname
            hostname = get_hostname(resolved_ip)
            if hostname:
                print(f"🌍 Hostname: {hostname}")
        except:
            pass
        
        # Get scan mode and port range
        mode, start_port, end_port = get_port_range_input()
        
        # Get scan options
        timeout, threads = get_scan_options()
        
        # Create scanner based on mode
        if mode == 'quick':
            print("\n⚡ Quick scan selected (common ports)...")
            scanner = QuickScan(target_ip, timeout=timeout, threads=threads)
        elif mode == 'full':
            print("\n🔥 Full scan selected (1-65535)...")
            scanner = FullScan(target_ip, timeout=timeout, threads=threads)
        elif mode == 'custom':
            print(f"\n🎯 Custom scan selected ({start_port}-{end_port})...")
            scanner = PortScanner(target_ip, start_port, end_port, timeout, threads)
        elif mode == 'specific':
            print(f"\n🎯 Scanning specific ports...")
            scanner = PortScanner(target_ip, 1, 1, timeout, threads)
            scanner.custom_ports = sorted(start_port)
            scanner.total_ports = len(start_port)
        
        # Set progress callback
        scanner.set_progress_callback(display_progress)
        
        # Start scanning
        open_ports, scan_time = scanner.start_scan()
        
        # Display results
        scanner.display_results(open_ports, scan_time)
        
        # Ask to save results
        save_choice = input("\n💾 Save results to file? (y/n): ").strip().lower()
        if save_choice == 'y':
            filename = input("Enter filename (default: scan_results.txt): ").strip() or "scan_results.txt"
            scanner.save_results(open_ports, scan_time, filename)
        
        print("\n✅ Scan completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrupted by user.")
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
