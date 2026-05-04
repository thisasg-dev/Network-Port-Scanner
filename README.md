# 🔍 Network Port Scanner

A comprehensive Python-based network port scanner with both CLI and GUI interfaces. Scan open ports on any device to discover services and assess network security.

## ✨ Features

### 🎯 Core Features
- ✅ IP address validation and hostname resolution
- ✅ Customizable port range selection
- ✅ Multi-threaded scanning for fast performance
- ✅ Open port detection with service identification
- ✅ Accurate scan time measurement

### ⚡ Intermediate Features
- ✅ Service name detection (SSH, HTTP, FTP, etc.)
- ✅ Quick scan (common ports) and Full scan (1-65535) modes
- ✅ Comprehensive error handling
- ✅ Real-time progress display
- ✅ Thread count optimization
- ✅ Customizable socket timeout

### 🔥 Advanced Features
- ✅ Banner grabbing from open ports
- ✅ Hostname/reverse DNS lookup
- ✅ Save scan results to file
- ✅ GUI interface with tkinter
- ✅ Multi-threaded architecture
- ✅ Service mapping database

## 📂 Project Structure

```
port_scanner/
│
├── main.py              # CLI interface
├── gui.py               # GUI interface (tkinter)
├── scanner.py           # Core scanning engine
├── utils.py             # Utility functions
├── requirements.txt     # Dependencies
└── README.md            # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- No external dependencies (uses only standard library)

### Installation

1. **Clone or download the project:**
```bash
cd port_scanner
```

2. **Verify Python installation:**
```bash
python --version
```

## 📱 Usage

### CLI Version (Command Line)

Run the CLI scanner:
```bash
python main.py
```

**Interactive Prompts:**
1. Enter target IP address (e.g., 127.0.0.1 or localhost)
2. Select scan mode:
   - Quick Scan (common ports)
   - Full Scan (1-65535)
   - Custom Range
   - Specific Ports
3. Configure timeout and thread count
4. View results and optionally save

**Example:**
```
Enter target IP: 127.0.0.1
[OPEN] Port 22 → SSH
[OPEN] Port 80 → HTTP
[OPEN] Port 443 → HTTPS

Scan completed in 1.8 seconds
```

### GUI Version (Graphical Interface)

Run the GUI scanner:
```bash
python gui.py
```

**Features:**
- 📡 Scanner tab for configuration
- 📊 Results tab for viewing scan results
- ℹ️ About tab with help information
- 🎨 Tabbed interface for organization
- 💾 Save and copy functionality

## 🔧 Configuration Options

### Scan Modes

**⚡ Quick Scan:**
- Fastest method
- Scans common ports only
- Good for initial reconnaissance
- Ports: 21, 22, 80, 443, 3306, 3389, 5900, 8080, etc.

**🔥 Full Scan:**
- Complete port enumeration
- Scans all 65535 ports
- Slowest but comprehensive
- May take several minutes

**🎯 Custom Range:**
- User-defined port range
- Balance between speed and coverage
- Example: 1-1024 for well-known ports

**🔨 Specific Ports:**
- Scan exact ports
- Format: 22,80,443,8080-8090
- Most efficient for targeted scans

### Advanced Options

```python
timeout=1        # Socket timeout in seconds (0.1-10)
threads=50       # Number of concurrent threads (1-200)
banner=True      # Enable service banner grabbing
```

## 📊 Output Examples

### Successful Scan
```
============================================================
🔍 PORT SCANNER
============================================================
Target: 127.0.0.1 (127.0.0.1)
Scanning ports: 1 - 1024
Threads: 50
============================================================

[OPEN PORTS FOUND: 3]

  [OPEN] Port 22 → SSH
         └─ OpenSSH_7.4 (protocol 2.0)
  
  [OPEN] Port 80 → HTTP
         └─ Apache/2.4.6 (CentOS)
  
  [OPEN] Port 443 → HTTPS
         └─ Apache/2.4.6 (CentOS)

============================================================
⏱️  Scan completed in 2.34 seconds
📊 Total ports scanned: 1024
🎯 Open ports: 3
============================================================
```

### No Results
```
❌ No open ports found.

Scan completed in 1.2 seconds
Total ports scanned: 1024
```

## 🔐 Common Ports Reference

| Port | Service | Description |
|------|---------|-------------|
| 21   | FTP     | File Transfer Protocol |
| 22   | SSH     | Secure Shell |
| 23   | Telnet  | Remote Login |
| 25   | SMTP    | Email Sending |
| 53   | DNS     | Domain Name System |
| 80   | HTTP    | Web Server |
| 110  | POP3    | Email Retrieval |
| 143  | IMAP    | Email Protocol |
| 443  | HTTPS   | Secure Web |
| 445  | SMB     | File Sharing |
| 3306 | MySQL   | Database |
| 3389 | RDP     | Remote Desktop |
| 5432 | PostgreSQL | Database |
| 5900 | VNC     | Remote Viewer |
| 8080 | HTTP-Alt | Alternate Web |
| 27017| MongoDB | NoSQL Database |
| 6379 | Redis   | Cache Server |

## ⚠️ Important Legal Notice

### ✅ LEGAL USE:
- Scan **only your own systems**
- Scan **authorized lab environments**
- Scan **networks you own or have permission to test**
- Use for **cybersecurity education and training**
- Use for **authorized security assessments**

### ❌ ILLEGAL USE:
- Scanning **unknown/public systems** without permission
- Scanning **other people's networks**
- Unauthorized **security testing**
- **Port scanning for malicious purposes**
- Violation of **Computer Fraud and Abuse Act (CFAA)**

**Using this tool without authorization may result in:**
- Criminal charges
- Civil liability
- Imprisonment
- Fines

## 💡 Tips & Tricks

### Performance Tips
1. **Use Quick Scan first** - identify services quickly
2. **Adjust threads** - increase to 100+ for faster scans
3. **Reduce timeout** - faster on responsive networks
4. **Scan specific ranges** - avoid unnecessary port checks

### Troubleshooting

**"Invalid IP address"**
- Verify IP format: XXX.XXX.XXX.XXX
- Or use hostname: localhost, example.com

**"Connection refused"**
- Normal response for closed ports
- No action required

**"Permission denied"**
- On Windows: Run as Administrator
- On Linux/Mac: Use `sudo python3 main.py`

**Slow scans**
- Increase thread count
- Reduce socket timeout
- Use Quick Scan mode
- Reduce port range

## 🎓 Learning Outcomes

By using this project, you'll learn:
- ✅ How networks and TCP/IP work
- ✅ Socket programming in Python
- ✅ Multi-threading concepts
- ✅ Port scanning techniques
- ✅ Service identification
- ✅ Cybersecurity fundamentals
- ✅ Network reconnaissance
- ✅ Ethical hacking concepts

## 🛠️ Development

### Code Structure

**scanner.py** - Core scanning logic
```python
PortScanner         # Main scanner class
├── scan_port()     # Single port scan
├── start_scan()    # Multi-threaded scanning
├── display_results()
└── save_results()

QuickScan          # Pre-configured quick scan
FullScan           # Pre-configured full scan
```

**utils.py** - Utility functions
```python
validate_ip()      # IP validation
get_service_name() # Service lookup
banner_grab()      # Banner grabbing
get_hostname()     # Reverse DNS lookup
parse_port_range() # Port range parsing
```

**main.py** - CLI interface
```python
print_banner()     # Display header
get_ip_input()     # Input validation
get_port_range_input()
get_scan_options()
```

**gui.py** - GUI implementation
```python
PortScannerGUI     # Main GUI class
├── setup_ui()
├── setup_scan_tab()
├── setup_results_tab()
└── _perform_scan()
```

### Extending the Project

1. **Add nmap integration:**
```python
import subprocess
subprocess.run(['nmap', '-p', ports, target])
```

2. **Add database logging:**
```python
import sqlite3
conn = sqlite3.connect('scans.db')
```

3. **Add scheduling:**
```python
from apscheduler.schedulers.background import BackgroundScheduler
scheduler.add_job(scan_network, 'cron', day_of_week='mon-fri', hour=9)
```

4. **Add web interface:**
```python
from flask import Flask
app = Flask(__name__)
@ app.route('/scan')
def web_scan():
    return render_template('scan.html')
```

## 🐛 Known Limitations

1. **Firewall blocking** - Results may be inaccurate behind firewalls
2. **Network latency** - Slow networks may show false negatives
3. **Rate limiting** - ISPs may block excessive scan traffic
4. **UDP ports** - Currently scans TCP only (UDP scanning requires root)
5. **IPv6** - Currently supports IPv4 only

## 📝 Version History

### v1.0 (Current)
- ✅ Core CLI scanner
- ✅ Multi-threading support
- ✅ GUI interface
- ✅ Banner grabbing
- ✅ Service detection
- ✅ Results saving

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- UDP port scanning
- IPv6 support
- Detection evasion techniques
- Performance optimization
- Additional GUI features

## 📄 License

This educational project is provided for learning cybersecurity concepts. Use responsibly and legally.

## 📞 Support & Documentation

- **Python Socket Module:** https://docs.python.org/3/library/socket.html
- **Threading:** https://docs.python.org/3/library/threading.html
- **Tkinter GUI:** https://docs.python.org/3/library/tkinter.html

## ⚡ Quick Reference

**Check port 80:**
```bash
python main.py
# Enter: 127.0.0.1
# Select: Custom Range
# Ports: 80-80
```

**Scan localhost quickly:**
```bash
python main.py
# Enter: localhost
# Select: Quick Scan
```

**Full scan with GUI:**
```bash
python gui.py
# Enter: 192.168.1.1
# Select: Full Scan
# Click: Start Scan
```

---

**⚠️ Remember:** Only scan systems you own or have explicit permission to test. Unauthorized port scanning is illegal and unethical.

🎯 **Happy Scanning!** (ethically and legally)
