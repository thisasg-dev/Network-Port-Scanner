# 📁 Network Port Scanner - Project File Guide

## 📂 Project Directory Structure

```
port_scanner/
│
├── 📄 CORE MODULES
│   ├── scanner.py              # Core scanning engine
│   ├── utils.py                # Utility functions & helpers
│   └── main.py                 # CLI interface
│
├── 🖥️  GUI & INTERFACE
│   └── gui.py                  # Tkinter GUI application
│
├── 🧪 TESTING & EXAMPLES
│   ├── test_scanner.py         # Test suite
│   └── EXAMPLES.py             # Usage examples
│
├── ⚙️  CONFIGURATION
│   ├── config.ini              # Configuration file
│   └── requirements.txt        # Python dependencies
│
├── 📚 DOCUMENTATION
│   ├── README.md               # Main documentation
│   └── FILE_GUIDE.md           # This file
│
└── 🚀 WINDOWS LAUNCHERS
    ├── run_cli.bat             # Launch CLI version
    ├── run_gui.bat             # Launch GUI version
    ├── run_tests.bat           # Run test suite
    └── run_examples.bat        # Run examples
```

## 📋 File Descriptions

### Core Modules (Required)

#### 1. **scanner.py** (Core Scanning Engine)
- **Purpose:** Main port scanning functionality
- **Classes:**
  - `PortScanner`: Main scanner class with custom port ranges
  - `QuickScan`: Pre-configured quick scanner (common ports)
  - `FullScan`: Pre-configured full scanner (1-65535)
- **Key Methods:**
  - `scan_port()`: Scan individual port
  - `start_scan()`: Multi-threaded scanning
  - `display_results()`: Format and show results
  - `save_results()`: Export to file
- **Features:**
  - Multi-threading support
  - Banner grabbing
  - Service detection
  - Progress tracking
  - Timeout control
- **Dependencies:** Python standard library only

#### 2. **utils.py** (Utility Functions)
- **Purpose:** Helper functions for scanning operations
- **Key Functions:**
  - `validate_ip()`: IP address validation
  - `get_service_name()`: Get service by port number
  - `banner_grab()`: Retrieve service banner
  - `get_hostname()`: Reverse DNS lookup
  - `parse_port_range()`: Parse port range strings
  - `format_size()`: Format byte sizes
- **Constants:**
  - `PORT_SERVICE_MAP`: Built-in port-to-service mapping
- **Dependencies:** Python standard library only

#### 3. **main.py** (CLI Interface)
- **Purpose:** Command-line interface for the scanner
- **Features:**
  - Interactive user prompts
  - IP validation
  - Scan mode selection
  - Progress display
  - Results saving
  - Error handling
- **Functions:**
  - `print_banner()`: Display header
  - `get_ip_input()`: Get and validate IP
  - `get_port_range_input()`: Get scan mode
  - `get_scan_options()`: Get advanced options
  - `display_progress()`: Show progress bar
- **Usage:** `python main.py`
- **Dependencies:** scanner.py, utils.py

### GUI & Interface

#### 4. **gui.py** (Tkinter GUI Application)
- **Purpose:** Graphical user interface for the scanner
- **Features:**
  - Tabbed interface (Scanner, Results, About)
  - Real-time progress display
  - Results viewing and export
  - Service banner grabbing
  - Multi-threaded scanning
  - Copy to clipboard
  - Save results
- **Classes:**
  - `PortScannerGUI`: Main GUI application
- **Components:**
  - Scan configuration tab
  - Results display tab
  - Help/About tab
  - Progress bar
  - Logging text area
- **Usage:** `python gui.py`
- **Dependencies:** tkinter (built-in), scanner.py, utils.py

### Testing & Examples

#### 5. **test_scanner.py** (Test Suite)
- **Purpose:** Verify all components are working correctly
- **Tests (11 Total):**
  1. Module imports
  2. IP validation
  3. Service detection
  4. Port range parsing
  5. Socket connectivity
  6. QuickScan class
  7. Custom PortScanner
  8. Error handling
  9. Performance metrics
  10. File operations
  11. CLI compatibility
- **Usage:** `python test_scanner.py`
- **Output:** Pass/fail status for each test

#### 6. **EXAMPLES.py** (Usage Examples)
- **Purpose:** Demonstrate various usage patterns
- **Examples (6 Total):**
  1. Quick scan implementation
  2. Custom range scanning
  3. Full network scan
  4. Batch scanning
  5. Specific port scanning
  6. Error handling patterns
- **Common Use Cases:**
  - Quick service verification
  - Network auditing
  - Batch operations
  - Continuous monitoring
- **Usage:** `python EXAMPLES.py`
- **Output:** Demonstrates different scanning techniques

### Configuration Files

#### 7. **config.ini** (Configuration)
- **Purpose:** Store default values and configuration
- **Sections:**
  - `[DEFAULTS]`: Default scanning parameters
  - `[OUTPUT]`: Output file settings
  - `[ADVANCED]`: Advanced options
  - `[COMMON_PORTS]`: Quick scan port list
  - `[SERVICE_MAPPING]`: Port-to-service mapping
- **Editable:** Yes, customize for your needs
- **Format:** INI format
- **Current Status:** Template (not actively used in v1.0)

#### 8. **requirements.txt** (Dependencies)
- **Purpose:** List Python package dependencies
- **Current Status:** Empty (all built-in modules used)
- **Future:** May be needed for additional features
- **Usage:** `pip install -r requirements.txt`

### Documentation

#### 9. **README.md** (Main Documentation)
- **Purpose:** Comprehensive user guide
- **Sections:**
  - Features overview
  - Installation instructions
  - Usage guide (CLI & GUI)
  - Configuration options
  - Common ports reference
  - Legal notice
  - Troubleshooting
  - Development guide
  - API documentation
- **Target Audience:** All users
- **Format:** Markdown

#### 10. **FILE_GUIDE.md** (Project Guide)
- **Purpose:** Detailed file descriptions
- **Sections:**
  - Directory structure
  - File purposes
  - Code documentation
  - Module dependencies
  - Developer guide
- **Target Audience:** Developers
- **Format:** Markdown

### Windows Launchers (Optional)

#### 11. **run_cli.bat** (CLI Launcher)
- **Purpose:** Easy CLI launch on Windows
- **Features:**
  - Python verification
  - Error checking
  - Auto-run with output
  - Pause on completion
- **Usage:** Double-click to run

#### 12. **run_gui.bat** (GUI Launcher)
- **Purpose:** Easy GUI launch on Windows
- **Features:**
  - Python verification
  - Error checking
  - Tkinter verification
  - Auto-run in new window
- **Usage:** Double-click to run

#### 13. **run_tests.bat** (Test Launcher)
- **Purpose:** Run test suite on Windows
- **Features:**
  - Python verification
  - Error checking
  - Run full test suite
  - Display results
- **Usage:** Double-click to run

#### 14. **run_examples.bat** (Examples Launcher)
- **Purpose:** Run examples on Windows
- **Features:**
  - Python verification
  - Error checking
  - Run demonstrations
  - Display results
- **Usage:** Double-click to run

---

## 🔄 Module Dependencies

```
main.py
├── scanner.py
│   ├── utils.py
│   │   └── socket (Python stdlib)
│   └── threading (Python stdlib)
└── utils.py

gui.py
├── tkinter (Python stdlib)
├── threading (Python stdlib)
├── scanner.py
│   └── utils.py
└── socket (Python stdlib)

test_scanner.py
├── scanner.py
├── utils.py
├── socket (Python stdlib)
└── time (Python stdlib)

EXAMPLES.py
├── scanner.py
├── utils.py
└── time (Python stdlib)
```

## 📊 Size & Complexity

| File | Lines | Purpose | Complexity |
|------|-------|---------|-----------|
| scanner.py | ~300 | Core scanning engine | High |
| utils.py | ~150 | Helper functions | Medium |
| main.py | ~250 | CLI interface | Medium |
| gui.py | ~500 | GUI application | High |
| test_scanner.py | ~300 | Testing suite | Medium |
| EXAMPLES.py | ~400 | Usage examples | Medium |
| README.md | ~600 | Documentation | Low |
| FILE_GUIDE.md | ~400 | File guide | Low |
| Total | ~3000 | Full project | - |

## 🚀 Getting Started

### Quick Start
1. **Run CLI version:** `python main.py`
2. **Run GUI version:** `python gui.py`
3. **Run tests:** `python test_scanner.py`
4. **View examples:** `python EXAMPLES.py`

### On Windows
1. **CLI:** Double-click `run_cli.bat`
2. **GUI:** Double-click `run_gui.bat`
3. **Tests:** Double-click `run_tests.bat`
4. **Examples:** Double-click `run_examples.bat`

### On Linux/Mac
```bash
# CLI version
python3 main.py

# GUI version
python3 gui.py

# Tests
python3 test_scanner.py

# Examples
python3 EXAMPLES.py
```

## 🔧 Customization

### Modifying Default Settings
Edit `config.ini`:
```ini
DEFAULT_TARGET = 127.0.0.1
DEFAULT_SCAN_MODE = quick
DEFAULT_TIMEOUT = 1
DEFAULT_THREADS = 50
```

### Adding New Services
Update `PORT_SERVICE_MAP` in `utils.py`:
```python
PORT_SERVICE_MAP = {
    ...
    9200: "Elasticsearch",  # Add new entry
    ...
}
```

### Creating Custom Scanners
Use `scanner.py` classes:
```python
from scanner import PortScanner

scanner = PortScanner("target.com", 1, 1000)
scanner.start_scan()
```

## 📈 Performance Metrics

| Operation | Time (typical) |
|-----------|----------------|
| Quick scan (common ports) | 1-3 seconds |
| Port 1-1000 scan | 5-15 seconds |
| Port 1-10000 scan | 20-60 seconds |
| Full scan (1-65535) | 5-30 minutes |
| Single port check | ~100ms |

## 🐛 Troubleshooting Issues

### Importing Errors
- Ensure all Python files are in same directory
- Check Python 3.7+ installation
- Verify tkinter for GUI: `python -m tkinter`

### Scanning Issues
- Use `run_tests.bat` to diagnose
- Check firewall settings
- Try with admin/sudo privileges
- Increase timeout for slow networks

### GUI Issues
- Ensure tkinter installed: `pip install tk`
- On Linux: `sudo apt install python3-tk`
- On Mac: Included with Python.org download

## 📝 Code Statistics

- **Total Lines of Code:** ~3000
- **Functions:** 50+
- **Classes:** 4
- **Test Cases:** 11
- **Documented:** 100%

## 🎯 Use Case Matrix

| Use Case | Best Tool | File(s) |
|----------|-----------|---------|
| Quick scan | CLI or GUI | main.py, gui.py |
| Batch scanning | Programmatic | scanner.py, EXAMPLES.py |
| Educational | GUI | gui.py |
| Automation | CLI | main.py |
| Development | Code | scanner.py |
| Testing | test_scanner.py | test_scanner.py |

## 💡 Pro Tips

1. **Performance:** Use CLI for batch operations
2. **Learning:** Start with GUI to understand features
3. **Testing:** Run test_scanner.py before first use
4. **Examples:** Study EXAMPLES.py for advanced usage
5. **Customization:** Edit config.ini for defaults
6. **Maintenance:** Keep all .py files in same directory

---

**Version:** 1.0  
**Last Updated:** March 2026  
**Python Version:** 3.7+  
**License:** Educational Use
