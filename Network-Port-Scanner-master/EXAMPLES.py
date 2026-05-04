#!/usr/bin/env python3
"""
QUICK START GUIDE - Network Port Scanner

This file demonstrates various ways to use the port scanner.
"""

# ============================================================================
# EXAMPLE 1: Using the CLI Scanner (Command Line)
# ============================================================================
"""
1. Open command prompt/terminal
2. Navigate to the port_scanner directory
3. Run: python main.py
4. Follow the interactive prompts

Example Session:
```
Enter target IP address or hostname: 127.0.0.1
Select mode (1-4): 1
Socket timeout in seconds (default 1): 1
Number of threads (default 50): 50

[OPEN] Port 22 → SSH
[OPEN] Port 80 → HTTP

Scan completed in 1.8 seconds
```
"""

# ============================================================================
# EXAMPLE 2: Using the GUI Scanner (Graphical)
# ============================================================================
"""
1. Open command prompt/terminal
2. Navigate to the port_scanner directory
3. Run: python gui.py
4. Enter IP address in the text field
5. Select scan mode
6. Click "Start Scan"
7. View results in the Results tab
"""

# ============================================================================
# EXAMPLE 3: Using Scanner Programmatically
# ============================================================================

from scanner import PortScanner, QuickScan, FullScan
from utils import validate_ip

# Example 3a: Quick Scan (Common Ports)
print("=" * 60)
print("EXAMPLE 3a: Quick Scan")
print("=" * 60)

target = "127.0.0.1"
scanner = QuickScan(target, timeout=1, threads=20)
open_ports, scan_time = scanner.start_scan()
scanner.display_results(open_ports, scan_time)


# Example 3b: Custom Port Range Scan
print("\n" + "=" * 60)
print("EXAMPLE 3b: Custom Range")
print("=" * 60)

target = "127.0.0.1"
scanner = PortScanner(target, start_port=1, end_port=100, timeout=1, threads=30)
open_ports, scan_time = scanner.start_scan()
scanner.display_results(open_ports, scan_time)

# Save results
scanner.save_results(open_ports, scan_time, "custom_scan_results.txt")


# Example 3c: Full Network Scan
print("\n" + "=" * 60)
print("EXAMPLE 3c: Full Scan (All Ports)")
print("=" * 60)

target = "127.0.0.1"
scanner = FullScan(target, timeout=1, threads=50)

# Set progress callback for real-time updates
def show_progress(scanned, total, port):
    percentage = (scanned / total) * 100
    print(f"Progress: {percentage:.1f}% (Port {port})", end='\r')

scanner.set_progress_callback(show_progress)

open_ports, scan_time = scanner.start_scan()
scanner.display_results(open_ports, scan_time)


# Example 3d: Batch Scanning Multiple IPs
print("\n" + "=" * 60)
print("EXAMPLE 3d: Batch Scanning")
print("=" * 60)

targets = ["127.0.0.1", "192.168.1.1", "localhost"]
results = {}

for target in targets:
    if validate_ip(target):
        try:
            scanner = QuickScan(target, timeout=1, threads=20)
            open_ports, scan_time = scanner.start_scan()
            results[target] = {
                'open_ports': open_ports,
                'scan_time': scan_time
            }
        except Exception as e:
            print(f"Error scanning {target}: {e}")
            results[target] = {'error': str(e)}

# Display batch results
print("\n" + "=" * 60)
print("BATCH SCAN SUMMARY")
print("=" * 60)

for target, result in results.items():
    if 'error' in result:
        print(f"{target}: ERROR - {result['error']}")
    else:
        port_count = len(result['open_ports'])
        print(f"{target}: {port_count} open ports ({result['scan_time']:.2f}s)")


# Example 3e: Scanning Specific Ports Only
print("\n" + "=" * 60)
print("EXAMPLE 3e: Specific Ports")
print("=" * 60)

target = "127.0.0.1"
specific_ports = [21, 22, 80, 443, 3306, 3389, 8080]

# Create scanner and override scan method
scanner = PortScanner(target, 1, 1, timeout=1, threads=10)
scanner.total_ports = len(specific_ports)

print(f"Scanning {target} for specific ports: {specific_ports}\n")

for port in specific_ports:
    open_port = scanner.scan_port(port)
    if open_port:
        print(f"[OPEN] Port {port} → {open_port['service']}")

print("\nSpecific port scan complete!")


# ============================================================================
# EXAMPLE 4: Error Handling
# ============================================================================

print("\n" + "=" * 60)
print("EXAMPLE 4: Error Handling")
print("=" * 60)

def safe_scan(target, mode="quick"):
    """Safely scan with error handling."""
    try:
        # Validate IP
        if not validate_ip(target):
            print(f"❌ Invalid IP: {target}")
            return
        
        # Create appropriate scanner
        if mode == "quick":
            scanner = QuickScan(target, timeout=1)
        elif mode == "full":
            scanner = FullScan(target, timeout=1)
        else:
            print(f"❌ Unknown mode: {mode}")
            return
        
        # Perform scan
        open_ports, scan_time = scanner.start_scan()
        scanner.display_results(open_ports, scan_time)
        
    except ValueError as e:
        print(f"❌ Invalid input: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Test error handling
safe_scan("127.0.0.1", "quick")
safe_scan("invalid_ip", "quick")  # This will handle error gracefully


# ============================================================================
# EXAMPLE 5: Performance Comparison
# ============================================================================

print("\n" + "=" * 60)
print("EXAMPLE 5: Performance Comparison")
print("=" * 60)

target = "127.0.0.1"
port_range = (1, 1000)

print("Testing different thread counts...")

for thread_count in [5, 10, 20, 50]:
    scanner = PortScanner(target, port_range[0], port_range[1], 
                         timeout=1, threads=thread_count)
    open_ports, scan_time = scanner.start_scan()
    print(f"Threads: {thread_count:3d} | Time: {scan_time:.2f}s | Ports: {len(open_ports)}")


# ============================================================================
# EXAMPLE 6: Exporting Results
# ============================================================================

print("\n" + "=" * 60)
print("EXAMPLE 6: Exporting Results")
print("=" * 60)

target = "127.0.0.1"
scanner = QuickScan(target)
open_ports, scan_time = scanner.start_scan()

# Save to file
scanner.save_results(open_ports, scan_time, "exported_results.txt")

# Display in different formats
print("\nJSON-like format:")
import json
for port_info in open_ports:
    print(json.dumps(port_info, indent=2))


# ============================================================================
# COMMON USE CASES
# ============================================================================

"""
USE CASE 1: Check if specific services are running
--------
scanner = PortScanner("localhost", 80, 80, timeout=1)
open_ports = scanner.start_scan()[0]
if open_ports:
    print("Web server is running!")

USE CASE 2: Find all open ports on localhost
--------
scanner = QuickScan("localhost")
open_ports, _ = scanner.start_scan()
for port_info in open_ports:
    print(f"Port {port_info['port']}: {port_info['service']}")

USE CASE 3: Perform security audit on network
--------
from utils import validate_ip

network_ips = ["192.168.1.1", "192.168.1.10", "192.168.1.20"]
for ip in network_ips:
    if validate_ip(ip):
        scanner = QuickScan(ip, threads=50)
        open_ports, _ = scanner.start_scan()
        print(f"{ip}: {len(open_ports)} open ports")

USE CASE 4: Continuous monitoring
--------
import time
while True:
    scanner = QuickScan("localhost")
    open_ports, _ = scanner.start_scan()
    print(f"[{time.strftime('%H:%M:%S')}] Open ports: {len(open_ports)}")
    time.sleep(300)  # Check every 5 minutes

"""

# ============================================================================
# TIPS & TRICKS
# ============================================================================

"""
PERFORMANCE TIPS:
1. Use Quick Scan for initial reconnaissance
2. Increase threads (50-100) for faster scans
3. Reduce timeout on responsive networks
4. Use Custom Range for targeted scans
5. Scan during off-peak hours

TROUBLESHOOTING:
1. Check firewall settings
2. Ensure network connectivity
3. Try with admin/sudo privileges
4. Reduce thread count if crashes
5. Increase timeout for slow networks

OPTIMIZATION:
1. Profile code with cProfile
2. Use asyncio for even faster scanning
3. Implement result caching
4. Add request rate limiting
5. Use native code (Cython) for speed

"""

print("\n✅ All examples completed!")
print("📖 Review the code above for more usage patterns.")
print("🚀 Run main.py or gui.py to start scanning!")
