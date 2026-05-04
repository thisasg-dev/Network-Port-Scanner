#!/usr/bin/env python3
"""
Network Port Scanner - Professional GUI Edition
Modern, beautiful UI with dark theme and smooth interactions
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from scanner import PortScanner, QuickScan, FullScan
from utils import validate_ip, get_hostname


class ModernEntry(tk.Entry):
    """Custom Entry widget with better styling"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            font=("Segoe UI", 10),
            bg="#2a2f36",
            fg="#ffffff",
            insertbackground="#00d9ff",
            relief=tk.FLAT,
            bd=1,
            padx=10,
            pady=8
        )


class PortScannerGUI:
    # Professional color scheme
    PRIMARY_BG = "#0f1419"        # Very dark background
    SECONDARY_BG = "#1a1f26"      # Dark card background
    TERTIARY_BG = "#2a2f36"       # Input background
    ACCENT_CYAN = "#00d9ff"       # Primary accent
    ACCENT_GREEN = "#51cf66"      # Success
    ACCENT_RED = "#ff6b6b"        # Danger
    ACCENT_YELLOW = "#ffd43b"     # Warning
    TEXT_PRIMARY = "#ffffff"      # Main text
    TEXT_SECONDARY = "#b0b8c1"    # Secondary text
    TEXT_MUTED = "#7a8189"        # Muted text
    BORDER_COLOR = "#2a2f36"      # Borders

    def __init__(self, root):
        self.root = root
        self.root.title("Network Port Scanner - Professional Edition")
        self.root.geometry("1100x900")
        self.root.resizable(True, True)
        
        # Configure main background
        self.root.configure(bg=self.PRIMARY_BG)
        
        self.scanner = None
        self.scanning = False
        
        self.setup_styles()
        self.setup_ui()
    
    def setup_styles(self):
        """Configure custom ttk styles for professional dark theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # ===== GENERAL FRAMES =====
        style.configure("TFrame", background=self.PRIMARY_BG)
        style.configure("Module.TFrame", background=self.PRIMARY_BG)
        style.configure("Card.TFrame", background=self.SECONDARY_BG)
        
        # ===== LABELS =====
        style.configure("TLabel", background=self.PRIMARY_BG, foreground=self.TEXT_PRIMARY,
                       font=("Segoe UI", 10))
        style.configure("Title.TLabel", background=self.PRIMARY_BG, foreground=self.ACCENT_CYAN,
                       font=("Segoe UI", 22, "bold"))
        style.configure("Heading.TLabel", background=self.SECONDARY_BG, foreground=self.ACCENT_CYAN,
                       font=("Segoe UI", 11, "bold"), padding=5)
        style.configure("SubHeading.TLabel", background=self.SECONDARY_BG, foreground=self.TEXT_PRIMARY,
                       font=("Segoe UI", 10, "bold"), padding=3)
        style.configure("Status.TLabel", background=self.PRIMARY_BG, foreground=self.ACCENT_GREEN,
                       font=("Segoe UI", 9, "bold"))
        style.configure("Muted.TLabel", background=self.SECONDARY_BG, foreground=self.TEXT_MUTED,
                       font=("Segoe UI", 9))
        
        # ===== BUTTONS =====
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=10)
        style.configure("Secondary.TButton", font=("Segoe UI", 9), padding=8)
        style.map("Accent.TButton",
                 foreground=[("pressed", self.TEXT_PRIMARY), ("", self.TEXT_PRIMARY)])
        
        # ===== NOTEBOOK (TABS) =====
        style.configure("TNotebook", background=self.PRIMARY_BG, borderwidth=1)
        style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=[15, 12])
        style.map("TNotebook.Tab",
                 background=[("selected", self.SECONDARY_BG), ("", self.PRIMARY_BG)],
                 foreground=[("selected", self.ACCENT_CYAN), ("", self.TEXT_SECONDARY)],
                 padding=[("selected", [15, 12]), ("", [15, 12])])
        
        # ===== LABELFRAME =====
        style.configure("Card.TLabelframe", background=self.SECONDARY_BG, 
                       foreground=self.TEXT_PRIMARY, bordercolor=self.BORDER_COLOR,
                       relief="flat", padding=15)
        style.configure("Card.TLabelframe.Label", background=self.SECONDARY_BG, 
                       foreground=self.ACCENT_CYAN, font=("Segoe UI", 11, "bold"))
        
        # ===== CHECKBUTTONS & RADIOBUTTONS =====
        style.configure("TCheckbutton", background=self.SECONDARY_BG, foreground=self.TEXT_PRIMARY,
                       font=("Segoe UI", 10), focuscolor="none", padding=5)
        style.configure("TRadiobutton", background=self.SECONDARY_BG, foreground=self.TEXT_PRIMARY,
                       font=("Segoe UI", 10), focuscolor="none", padding=5)
        style.map("TCheckbutton", background=[("active", self.TERTIARY_BG)])
        style.map("TRadiobutton", background=[("active", self.TERTIARY_BG)])
        
        # ===== SPINBOX =====
        style.configure("TSpinbox", font=("Segoe UI", 10), padding=5)
        
        # ===== COMBOBOX =====
        style.configure("TCombobox", font=("Segoe UI", 10))
        
        # ===== PROGRESSBAR =====
        style.configure("TProgressbar", background=self.ACCENT_CYAN, 
                       troughcolor=self.TERTIARY_BG, bordercolor=self.BORDER_COLOR,
                       lightcolor=self.ACCENT_CYAN, darkcolor=self.ACCENT_CYAN)
    
    def setup_ui(self):
        """Setup the main GUI layout"""
        # Create header frame
        header_frame = tk.Frame(self.root, bg=self.PRIMARY_BG, height=60)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title in header
        title = tk.Label(header_frame, text="🔍 Network Port Scanner", 
                        bg=self.PRIMARY_BG, fg=self.ACCENT_CYAN,
                        font=("Segoe UI", 18, "bold"))
        title.pack(side=tk.LEFT, padx=20, pady=10)
        
        subtitle = tk.Label(header_frame, text="Professional Port Enumeration Tool",
                           bg=self.PRIMARY_BG, fg=self.TEXT_SECONDARY,
                           font=("Segoe UI", 9))
        subtitle.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Create separator
        sep = tk.Frame(self.root, bg=self.BORDER_COLOR, height=1)
        sep.pack(fill=tk.X, padx=0, pady=0)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Scanner Tab
        self.scan_frame = tk.Frame(self.notebook, bg=self.PRIMARY_BG)
        self.notebook.add(self.scan_frame, text="⚙️  Scanner Configuration")
        self.setup_scan_tab()
        
        # Results Tab
        self.results_frame = tk.Frame(self.notebook, bg=self.PRIMARY_BG)
        self.notebook.add(self.results_frame, text="📊 Scan Results")
        self.setup_results_tab()
        
        # About Tab
        self.about_frame = tk.Frame(self.notebook, bg=self.PRIMARY_BG)
        self.notebook.add(self.about_frame, text="ℹ️  Documentation")
        self.setup_about_tab()
    
    def setup_scan_tab(self):
        """Setup the scan tab."""
        # Title
        title_label = ttk.Label(
            self.scan_frame,
            text="Network Port Scanner",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Target Frame
        target_frame = ttk.LabelFrame(self.scan_frame, text="Target Configuration", padding=10)
        target_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(target_frame, text="Target IP/Hostname:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.target_entry = ttk.Entry(target_frame, width=40)
        self.target_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.target_entry.insert(0, "127.0.0.1")
        
        # Scan Mode Frame
        mode_frame = ttk.LabelFrame(self.scan_frame, text="Scan Mode", padding=10)
        mode_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.scan_mode = tk.StringVar(value="quick")
        
        ttk.Radiobutton(mode_frame, text="⚡ Quick Scan (Common Ports)", 
                       variable=self.scan_mode, value="quick", 
                       command=self.on_mode_change).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(mode_frame, text="🔥 Full Scan (1-65535)", 
                       variable=self.scan_mode, value="full",
                       command=self.on_mode_change).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(mode_frame, text="🎯 Custom Range", 
                       variable=self.scan_mode, value="custom",
                       command=self.on_mode_change).pack(anchor=tk.W, pady=2)
        
        # Custom range frame
        self.custom_range_frame = ttk.Frame(mode_frame)
        self.custom_range_frame.pack(anchor=tk.W, pady=5, padx=20)
        
        ttk.Label(self.custom_range_frame, text="Start Port:").pack(side=tk.LEFT, padx=5)
        self.start_port_entry = ttk.Entry(self.custom_range_frame, width=10)
        self.start_port_entry.pack(side=tk.LEFT, padx=5)
        self.start_port_entry.insert(0, "1")
        
        ttk.Label(self.custom_range_frame, text="End Port:").pack(side=tk.LEFT, padx=5)
        self.end_port_entry = ttk.Entry(self.custom_range_frame, width=10)
        self.end_port_entry.pack(side=tk.LEFT, padx=5)
        self.end_port_entry.insert(0, "1024")
        
        self.custom_range_frame.pack_forget()  # Hide initially
        
        # Options Frame
        options_frame = ttk.LabelFrame(self.scan_frame, text="Scan Options", padding=10)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(options_frame, text="Timeout (seconds):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.timeout_var = tk.StringVar(value="1")
        timeout_spin = ttk.Spinbox(options_frame, from_=0.1, to=10, textvariable=self.timeout_var, width=10)
        timeout_spin.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(options_frame, text="Threads:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.threads_var = tk.StringVar(value="50")
        threads_spin = ttk.Spinbox(options_frame, from_=1, to=200, textvariable=self.threads_var, width=10)
        threads_spin.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        self.banner_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="🎣 Enable Banner Grabbing", 
                       variable=self.banner_var).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # Progress Frame
        progress_frame = ttk.Frame(self.scan_frame)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="Ready to scan")
        self.progress_label.pack(anchor=tk.W)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Button Frame
        button_frame = ttk.Frame(self.scan_frame)
        button_frame.pack(pady=15)
        
        self.scan_button = ttk.Button(button_frame, text="🚀 Start Scan", command=self.start_scan)
        self.scan_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="⛔ Stop", command=self.stop_scan, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="🗑️ Clear", command=self.clear_all).pack(side=tk.LEFT, padx=5)
    
    def setup_results_tab(self):
        """Setup the results tab."""
        title_label = ttk.Label(self.results_frame, text="Scan Results", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(
            self.results_frame,
            width=100,
            height=25,
            font=("Courier", 10)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.results_text.config(state=tk.DISABLED)
        
        # Save button
        button_frame = ttk.Frame(self.results_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="💾 Save Results", command=self.save_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📋 Copy All", command=self.copy_results).pack(side=tk.LEFT, padx=5)
    
    def setup_about_tab(self):
        """Setup the about tab."""
        about_text = scrolledtext.ScrolledText(
            self.about_frame,
            width=100,
            height=30,
            font=("Arial", 10)
        )
        about_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        about_text.config(state=tk.NORMAL)
        
        content = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          🔍 NETWORK PORT SCANNER 🔍
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 FEATURES:

Core Features:
  ✓ IP Address validation
  ✓ Custom port range selection
  ✓ Multi-threaded scanning
  ✓ Open ports detection
  ✓ Scan time measurement

Intermediate Features:
  ✓ Service name detection
  ✓ Quick & Full scan modes
  ✓ Error handling
  ✓ Progress display
  ✓ Threading optimization

Advanced Features:
  ✓ Banner grabbing
  ✓ Hostname lookup
  ✓ Save results to file
  ✓ GUI interface
  ✓ Timeout control

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 HOW TO USE:

1. Enter target IP address or hostname
2. Select scan mode (Quick, Full, or Custom)
3. Adjust timeout and thread settings if needed
4. Click "Start Scan"
5. View results in the Results tab

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  IMPORTANT LEGAL NOTICE:

  ⚠️  ONLY SCAN:
    • Your own computer
    • Authorized networks/devices
    • Lab/testing environments

  ❌ DO NOT SCAN:
    • Unknown systems
    • Public networks
    • Systems without permission
    (This is ILLEGAL and unethical)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 SCAN MODES:

⚡ Quick Scan:
  Scans only common ports (21, 22, 80, 443, etc.)
  Fastest option for initial reconnaissance

🔥 Full Scan:
  Scans all ports (1-65535)
  Slowest but most thorough

🎯 Custom Range:
  Scan specific port ranges you define
  Balance between speed and coverage

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 COMMON PORTS:

  21   → FTP          (File Transfer)
  22   → SSH          (Secure Shell)
  80   → HTTP         (Web)
  443  → HTTPS        (Secure Web)
  3306 → MySQL        (Database)
  5432 → PostgreSQL   (Database)
  27017→ MongoDB      (NoSQL Database)
  3389 → RDP          (Remote Desktop)
  5900 → VNC          (Remote Viewer)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        about_text.insert('1.0', content)
        about_text.config(state=tk.DISABLED)
    
    def on_mode_change(self):
        """Handle scan mode change."""
        if self.scan_mode.get() == "custom":
            self.custom_range_frame.pack(anchor=tk.W, pady=5, padx=20)
        else:
            self.custom_range_frame.pack_forget()
    
    def update_progress(self, scanned, total, port):
        """Update progress display."""
        percentage = (scanned / total) * 100
        self.progress_var.set(percentage)
        self.progress_label.config(text=f"Scanning... {percentage:.1f}% (Port {port})")
        self.root.update_idletasks()
    
    def start_scan(self):
        """Start the scanning process."""
        if self.scanning:
            return
        
        # Validate input
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Please enter a target IP address or hostname")
            return
        
        if not validate_ip(target):
            messagebox.showerror("Error", "Invalid IP address or hostname")
            return
        
        # Disable UI
        self.scanning = True
        self.scan_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.target_entry.config(state=tk.DISABLED)
        
        # Clear previous results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete('1.0', tk.END)
        
        # Start scan in thread
        scan_thread = threading.Thread(target=self._perform_scan, args=(target,))
        scan_thread.daemon = True
        scan_thread.start()
    
    def _perform_scan(self, target):
        """Perform the actual scan (runs in thread)."""
        try:
            # Get options
            timeout = float(self.timeout_var.get())
            threads = int(self.threads_var.get())
            mode = self.scan_mode.get()
            
            # Create scanner
            if mode == "quick":
                self.scanner = QuickScan(target, timeout=timeout, threads=threads)
            elif mode == "full":
                self.scanner = FullScan(target, timeout=timeout, threads=threads)
            else:  # custom
                try:
                    start = int(self.start_port_entry.get())
                    end = int(self.end_port_entry.get())
                    if start < 1 or end > 65535 or start > end:
                        raise ValueError
                    self.scanner = PortScanner(target, start, end, timeout, threads)
                except ValueError:
                    self.append_results("❌ Invalid port range!")
                    self.enable_ui()
                    return
            
            self.scanner.set_progress_callback(self.update_progress)
            
            # Perform scan
            open_ports, scan_time = self.scanner.start_scan()
            
            # Display results
            self.append_results("="*70)
            self.append_results("✅ SCAN RESULTS")
            self.append_results("="*70)
            self.append_results(f"\nTarget: {target}")
            self.append_results(f"Port Range: {self.scanner.start_port} - {self.scanner.end_port}")
            
            # Hostname lookup
            try:
                import socket
                hostname = get_hostname(socket.gethostbyname(target))
                if hostname:
                    self.append_results(f"Hostname: {hostname}")
            except:
                pass
            
            self.append_results(f"Timeout: {timeout}s")
            self.append_results(f"Threads: {threads}")
            self.append_results(f"Scan Time: {scan_time:.2f} seconds\n")
            
            if open_ports:
                self.append_results(f"[OPEN PORTS FOUND: {len(open_ports)}]\n")
                for port_info in open_ports:
                    port = port_info['port']
                    service = port_info['service']
                    banner = port_info['banner']
                    
                    self.append_results(f"[OPEN] Port {port} → {service}")
                    if banner:
                        self.append_results(f"       Banner: {banner[:60]}")
            else:
                self.append_results("❌ No open ports found.")
            
            self.append_results("\n" + "="*70)
        
        except Exception as e:
            self.append_results(f"❌ Error: {e}")
        
        finally:
            self.enable_ui()
    
    def append_results(self, text):
        """Append text to results text area."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, text + "\n")
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def stop_scan(self):
        """Stop the current scan."""
        if self.scanner:
            self.scanner.scanned_ports = self.scanner.total_ports
        self.enable_ui()
        self.append_results("\n⚠️  Scan stopped by user.")
    
    def enable_ui(self):
        """Re-enable UI elements."""
        self.scanning = False
        self.scan_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.target_entry.config(state=tk.NORMAL)
        self.progress_var.set(0)
        self.progress_label.config(text="Ready to scan")
    
    def clear_all(self):
        """Clear all inputs and results."""
        self.target_entry.delete(0, tk.END)
        self.target_entry.insert(0, "127.0.0.1")
        self.start_port_entry.delete(0, tk.END)
        self.start_port_entry.insert(0, "1")
        self.end_port_entry.delete(0, tk.END)
        self.end_port_entry.insert(0, "1024")
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete('1.0', tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.progress_var.set(0)
    
    def save_results(self):
        """Save results to file."""
        results = self.results_text.get('1.0', tk.END)
        if not results.strip():
            messagebox.showwarning("Warning", "No results to save")
            return
        
        try:
            with open("scan_results.txt", "w") as f:
                f.write(results)
            messagebox.showinfo("Success", "Results saved to scan_results.txt")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")
    
    def copy_results(self):
        """Copy results to clipboard."""
        results = self.results_text.get('1.0', tk.END)
        if results:
            self.root.clipboard_clear()
            self.root.clipboard_append(results)
            messagebox.showinfo("Success", "Results copied to clipboard")


def main():
    """Main GUI application."""
    root = tk.Tk()
    
    # Set style
    style = ttk.Style()
    style.theme_use('clam')
    
    app = PortScannerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
