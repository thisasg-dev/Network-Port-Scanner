#!/usr/bin/env python3
"""
Network Port Scanner - Professional GUI Edition
Beautiful dark theme with modern design
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from scanner import PortScanner, QuickScan, FullScan
from utils import validate_ip, get_hostname


class PortScannerGUI:
    # Modern Color Palette
    PRIMARY_BG = "#0f1419"
    SECONDARY_BG = "#1a1f26"
    TERTIARY_BG = "#2a2f36"
    ACCENT_CYAN = "#00d9ff"
    ACCENT_GREEN = "#51cf66"
    ACCENT_RED = "#ff6b6b"
    ACCENT_YELLOW = "#ffd43b"
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#b0b8c1"
    TEXT_MUTED = "#7a8189"

    def __init__(self, root):
        self.root = root
        self.root.title("Network Port Scanner - Professional Edition")
        self.root.geometry("1150x950")
        self.root.resizable(True, True)
        self.root.configure(bg=self.PRIMARY_BG)
        
        self.scanner = None
        self.scanning = False
        
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("TFrame", background=self.PRIMARY_BG)
        style.configure("TLabel", background=self.PRIMARY_BG, foreground=self.TEXT_PRIMARY, font=("Segoe UI", 10))
        style.configure("Heading.TLabel", background=self.SECONDARY_BG, foreground=self.ACCENT_CYAN, font=("Segoe UI", 11, "bold"))
        style.configure("TNotebook", background=self.PRIMARY_BG, borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=[15, 12])
        style.map("TNotebook.Tab", background=[("selected", self.SECONDARY_BG), ("", self.PRIMARY_BG)], foreground=[("selected", self.ACCENT_CYAN), ("", self.TEXT_SECONDARY)])
        style.configure("TCheckbutton", background=self.SECONDARY_BG, foreground=self.TEXT_PRIMARY, font=("Segoe UI", 10))
        style.configure("TRadiobutton", background=self.SECONDARY_BG, foreground=self.TEXT_PRIMARY, font=("Segoe UI", 10))
        style.configure("TProgressbar", background=self.ACCENT_CYAN, troughcolor=self.TERTIARY_BG)

    def setup_ui(self):
        """Setup main UI"""
        # Header
        header = tk.Frame(self.root, bg=self.PRIMARY_BG, height=70)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        title_frame = tk.Frame(header, bg=self.PRIMARY_BG)
        title_frame.pack(side=tk.LEFT, padx=25, pady=15)
        
        tk.Label(title_frame, text="🔍 Network Port Scanner", bg=self.PRIMARY_BG, fg=self.ACCENT_CYAN, font=("Segoe UI", 20, "bold")).pack(anchor=tk.W)
        tk.Label(title_frame, text="Professional Port Reconnaissance Tool", bg=self.PRIMARY_BG, fg=self.TEXT_MUTED, font=("Segoe UI", 9)).pack(anchor=tk.W)
        
        tk.Frame(self.root, bg="#2a2f36", height=1).pack(fill=tk.X)
        
        # Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        self.scan_frame = tk.Frame(self.notebook, bg=self.PRIMARY_BG)
        self.notebook.add(self.scan_frame, text="⚙️  Configuration")
        self.setup_scan_tab()
        
        self.results_frame = tk.Frame(self.notebook, bg=self.PRIMARY_BG)
        self.notebook.add(self.results_frame, text="📊 Results")
        self.setup_results_tab()
        
        self.about_frame = tk.Frame(self.notebook, bg=self.PRIMARY_BG)
        self.notebook.add(self.about_frame, text="ℹ️  About")
        self.setup_about_tab()

    def setup_scan_tab(self):
        """Setup scanner configuration tab"""
        canvas = tk.Canvas(self.scan_frame, bg=self.PRIMARY_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.scan_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.PRIMARY_BG)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Target Card
        card = tk.Frame(scrollable_frame, bg=self.SECONDARY_BG, relief=tk.FLAT, bd=1)
        card.pack(fill=tk.X, padx=15, pady=12)
        tk.Label(card, text="🎯 Target Configuration", bg=self.SECONDARY_BG, fg=self.ACCENT_CYAN, font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        input_frame = tk.Frame(card, bg=self.SECONDARY_BG)
        input_frame.pack(fill=tk.X, padx=15, pady=10)
        tk.Label(input_frame, text="Target IP/Hostname:", bg=self.SECONDARY_BG, fg=self.TEXT_PRIMARY).pack(anchor=tk.W, pady=(0, 5))
        self.target_entry = tk.Entry(input_frame, font=("Segoe UI", 10), bg=self.TERTIARY_BG, fg=self.TEXT_PRIMARY, insertbackground=self.ACCENT_CYAN, relief=tk.FLAT, bd=1)
        self.target_entry.pack(fill=tk.X, ipady=8, padx=2, pady=2)
        self.target_entry.insert(0, "127.0.0.1")
        
        # Scan Mode Card
        card = tk.Frame(scrollable_frame, bg=self.SECONDARY_BG, relief=tk.FLAT, bd=1)
        card.pack(fill=tk.X, padx=15, pady=12)
        tk.Label(card, text="⚡ Scan Mode", bg=self.SECONDARY_BG, fg=self.ACCENT_CYAN, font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        modes_frame = tk.Frame(card, bg=self.SECONDARY_BG)
        modes_frame.pack(fill=tk.X, padx=15, pady=10)
        self.scan_mode = tk.StringVar(value="quick")
        
        modes = [("quick", "⚡ Quick Scan", "Common ports only"), ("full", "🔥 Full Scan", "All 65535 ports"), ("custom", "🎯 Custom", "User-defined range")]
        for val, label, desc in modes:
            mf = tk.Frame(modes_frame, bg=self.SECONDARY_BG)
            mf.pack(fill=tk.X, pady=6)
            tk.Radiobutton(mf, text=label, variable=self.scan_mode, value=val, bg=self.SECONDARY_BG, fg=self.TEXT_PRIMARY, selectcolor=self.TERTIARY_BG, activebackground=self.TERTIARY_BG, font=("Segoe UI", 10), command=self.on_mode_change).pack(anchor=tk.W)
            tk.Label(mf, text=desc, bg=self.SECONDARY_BG, fg=self.TEXT_MUTED, font=("Segoe UI", 8)).pack(anchor=tk.W, padx=25)
        
        self.custom_range_frame = tk.Frame(modes_frame, bg=self.SECONDARY_BG)
        crf = tk.Frame(self.custom_range_frame, bg=self.SECONDARY_BG)
        crf.pack(fill=tk.X, pady=8)
        tk.Label(crf, text="Start:", bg=self.SECONDARY_BG, fg=self.TEXT_PRIMARY, width=8).pack(side=tk.LEFT, padx=2)
        self.start_port_entry = tk.Entry(crf, font=("Segoe UI", 10), bg=self.TERTIARY_BG, fg=self.TEXT_PRIMARY, relief=tk.FLAT, bd=1, width=10)
        self.start_port_entry.pack(side=tk.LEFT, padx=2, ipady=4)
        self.start_port_entry.insert(0, "1")
        tk.Label(crf, text="End:", bg=self.SECONDARY_BG, fg=self.TEXT_PRIMARY, width=6).pack(side=tk.LEFT, padx=2)
        self.end_port_entry = tk.Entry(crf, font=("Segoe UI", 10), bg=self.TERTIARY_BG, fg=self.TEXT_PRIMARY, relief=tk.FLAT, bd=1, width=10)
        self.end_port_entry.pack(side=tk.LEFT, padx=2, ipady=4)
        self.end_port_entry.insert(0, "1024")
        
        # Options Card
        card = tk.Frame(scrollable_frame, bg=self.SECONDARY_BG, relief=tk.FLAT, bd=1)
        card.pack(fill=tk.X, padx=15, pady=12)
        tk.Label(card, text="🔧 Advanced Options", bg=self.SECONDARY_BG, fg=self.ACCENT_CYAN, font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        opts = tk.Frame(card, bg=self.SECONDARY_BG)
        opts.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(opts, text="Timeout (seconds):", bg=self.SECONDARY_BG, fg=self.TEXT_PRIMARY).pack(anchor=tk.W, pady=3)
        self.timeout_var = tk.StringVar(value="1")
        ttk.Spinbox(opts, from_=0.1, to=10, textvariable=self.timeout_var, width=12).pack(anchor=tk.W, ipady=5)
        
        tk.Label(opts, text="Threads:", bg=self.SECONDARY_BG, fg=self.TEXT_PRIMARY).pack(anchor=tk.W, pady=8)
        self.threads_var = tk.StringVar(value="50")
        ttk.Spinbox(opts, from_=1, to=200, textvariable=self.threads_var, width=12).pack(anchor=tk.W, ipady=5)
        
        self.banner_var = tk.BooleanVar(value=True)
        tk.Checkbutton(opts, text="🎣 Enable Banner Grabbing", variable=self.banner_var, bg=self.SECONDARY_BG, fg=self.TEXT_PRIMARY, selectcolor=self.TERTIARY_BG, activebackground=self.TERTIARY_BG, font=("Segoe UI", 10), pady=8).pack(anchor=tk.W)
        
        # Progress Card
        card = tk.Frame(scrollable_frame, bg=self.SECONDARY_BG, relief=tk.FLAT, bd=1)
        card.pack(fill=tk.X, padx=15, pady=12)
        tk.Label(card, text="📈 Progress", bg=self.SECONDARY_BG, fg=self.ACCENT_CYAN, font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        pcf = tk.Frame(card, bg=self.SECONDARY_BG)
        pcf.pack(fill=tk.X, padx=15, pady=10)
        self.progress_label = tk.Label(pcf, text="Ready to scan...", bg=self.SECONDARY_BG, fg=self.ACCENT_GREEN, font=("Segoe UI", 9, "bold"))
        self.progress_label.pack(anchor=tk.W, pady=(0, 8))
        self.progress_var = tk.DoubleVar()
        ttk.Progressbar(pcf, variable=self.progress_var, maximum=100).pack(fill=tk.X, ipady=4)
        
        # Buttons Card
        card = tk.Frame(scrollable_frame, bg=self.SECONDARY_BG, relief=tk.FLAT, bd=1)
        card.pack(fill=tk.X, padx=15, pady=12)
        
        bf = tk.Frame(card, bg=self.SECONDARY_BG)
        bf.pack(fill=tk.X, padx=15, pady=12)
        
        self.scan_button = tk.Button(bf, text="🚀 START SCAN", command=self.start_scan, bg=self.ACCENT_CYAN, fg="#000000", font=("Segoe UI", 11, "bold"), padx=20, pady=10, relief=tk.FLAT, bd=0, cursor="hand2")
        self.scan_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(bf, text="⛔ STOP", command=self.stop_scan, bg=self.ACCENT_RED, fg="#ffffff", font=("Segoe UI", 11, "bold"), padx=20, pady=10, relief=tk.FLAT, bd=0, cursor="hand2", state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        tk.Button(bf, text="🗑️ CLEAR", command=self.clear_all, bg=self.TERTIARY_BG, fg=self.TEXT_PRIMARY, font=("Segoe UI", 10, "bold"), padx=15, pady=10, relief=tk.FLAT, bd=0, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def setup_results_tab(self):
        """Setup results tab"""
        header = tk.Frame(self.results_frame, bg=self.SECONDARY_BG, height=50)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        tk.Label(header, text="📊 Scan Results", bg=self.SECONDARY_BG, fg=self.ACCENT_CYAN, font=("Segoe UI", 14, "bold")).pack(anchor=tk.W, padx=20, pady=10)
        
        cf = tk.Frame(self.results_frame, bg=self.PRIMARY_BG)
        cf.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.results_text = scrolledtext.ScrolledText(cf, width=120, height=30, font=("Consolas", 10), bg=self.TERTIARY_BG, fg=self.TEXT_PRIMARY, insertbackground=self.ACCENT_CYAN, relief=tk.FLAT, bd=1, padx=12, pady=12, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        self.results_text.config(state=tk.DISABLED)
        self.results_text.tag_configure("success", foreground=self.ACCENT_GREEN)
        self.results_text.tag_configure("error", foreground=self.ACCENT_RED)
        self.results_text.tag_configure("warning", foreground=self.ACCENT_YELLOW)
        self.results_text.tag_configure("info", foreground=self.ACCENT_CYAN)
        
        bf = tk.Frame(self.results_frame, bg=self.PRIMARY_BG)
        bf.pack(fill=tk.X, padx=15, pady=15)
        tk.Button(bf, text="💾 SAVE", command=self.save_results, bg=self.ACCENT_CYAN, fg="#000000", font=("Segoe UI", 10, "bold"), padx=15, pady=8, relief=tk.FLAT, bd=0, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="📋 COPY", command=self.copy_results, bg=self.TERTIARY_BG, fg=self.TEXT_PRIMARY, font=("Segoe UI", 10, "bold"), padx=15, pady=8, relief=tk.FLAT, bd=0, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="🗑️ CLEAR", command=self.clear_results, bg=self.ACCENT_RED, fg="#ffffff", font=("Segoe UI", 10, "bold"), padx=15, pady=8, relief=tk.FLAT, bd=0, cursor="hand2").pack(side=tk.LEFT, padx=5)

    def setup_about_tab(self):
        """Setup about tab"""
        canvas = tk.Canvas(self.about_frame, bg=self.PRIMARY_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.about_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.PRIMARY_BG)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        tk.Label(scrollable_frame, text="Network Port Scanner", bg=self.PRIMARY_BG, fg=self.ACCENT_CYAN, font=("Segoe UI", 14, "bold")).pack(pady=20)
        
        for title, content in [("✨ Features", "✓ Multi-threaded scanning\n✓ Service identification\n✓ Banner grabbing\n✓ Custom port ranges\n✓ Real-time progress\n✓ Results export"),
                               ("🔘 Scan Modes", "⚡ Quick: Common ports only\n🔥 Full: All 65535 ports\n🎯 Custom: User-defined"),
                               ("🔌 Common Ports", "22→SSH  80→HTTP  443→HTTPS\n3306→MySQL  5432→PostgreSQL\n27017→MongoDB  3389→RDP"),
                               ("⚠️  Legal Notice", "✅ Legal: Your computer, authorized networks\n❌ Illegal: Unauthorized networks\n⚠️ Violates laws/ethics")]:
            card = tk.Frame(scrollable_frame, bg=self.SECONDARY_BG)
            card.pack(fill=tk.X, padx=15, pady=10)
            tk.Label(card, text=title, bg=self.SECONDARY_BG, fg=self.ACCENT_CYAN, font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, padx=15, pady=(10, 5))
            tk.Label(card, text=content, bg=self.SECONDARY_BG, fg=self.TEXT_PRIMARY, font=("Segoe UI", 9), justify=tk.LEFT).pack(anchor=tk.W, padx=15, pady=(0, 15))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def on_mode_change(self):
        if self.scan_mode.get() == "custom":
            self.custom_range_frame.pack(fill=tk.X, pady=8)
        else:
            self.custom_range_frame.pack_forget()

    def update_progress(self, scanned, total, port):
        if total > 0:
            pct = (scanned / total) * 100
            self.progress_var.set(pct)
            self.progress_label.config(text=f"Scanning... {pct:.1f}% (Port {port})", fg=self.ACCENT_GREEN)
            self.root.update_idletasks()

    def start_scan(self):
        if self.scanning:
            return
        target = self.target_entry.get().strip()
        if not target or not validate_ip(target):
            messagebox.showerror("Error", "Invalid IP address")
            return
        self.scanning = True
        self.scan_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.target_entry.config(state=tk.DISABLED)
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete('1.0', tk.END)
        threading.Thread(target=self._perform_scan, args=(target,), daemon=True).start()

    def _perform_scan(self, target):
        try:
            timeout, threads, mode = float(self.timeout_var.get()), int(self.threads_var.get()), self.scan_mode.get()
            if mode == "quick":
                scanner = QuickScan(target, timeout=timeout, threads=threads)
            elif mode == "full":
                scanner = FullScan(target, timeout=timeout, threads=threads)
            else:
                try:
                    start, end = int(self.start_port_entry.get()), int(self.end_port_entry.get())
                    if not (1 <= start <= end <= 65535):
                        raise ValueError
                    scanner = PortScanner(target, start, end, timeout, threads)
                except:
                    self.append_results("❌ Invalid port range", "error")
                    self.enable_ui()
                    return
            self.scanner = scanner
            self.scanner.set_progress_callback(self.update_progress)
            open_ports, scan_time = self.scanner.start_scan()
            self.append_results("="*70, "info")
            self.append_results("✅ SCAN COMPLETED SUCCESSFULLY", "success")
            self.append_results("="*70, "info")
            self.append_results(f"\n🎯 Target: {target}\nPort Range: {scanner.start_port} - {scanner.end_port}\nScan Time: {scan_time:.2f}s\nThreads: {threads}\n", "info")
            if open_ports:
                self.append_results(f"[{len(open_ports)} OPEN PORTS FOUND]\n", "success")
                for p in open_ports:
                    self.append_results(f"[OPEN] Port {p['port']} → {p['service']}", "success")
                    if p['banner']:
                        self.append_results(f"       └─ {p['banner'][:70]}", "warning")
            else:
                self.append_results("❌ No open ports found.", "error")
            self.append_results("\n" + "="*70, "info")
        except Exception as e:
            self.append_results(f"❌ Error: {e}", "error")
        finally:
            self.enable_ui()

    def append_results(self, text, tag=""):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, text + "\n", tag)
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.root.update_idletasks()

    def stop_scan(self):
        if self.scanner:
            self.scanner.scanned_ports = self.scanner.total_ports
        self.enable_ui()
        self.append_results("\n⚠️  Scan stopped by user.", "warning")

    def enable_ui(self):
        self.scanning = False
        self.scan_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.target_entry.config(state=tk.NORMAL)
        self.progress_var.set(0)
        self.progress_label.config(text="Ready to scan...", fg=self.TEXT_SECONDARY)

    def clear_all(self):
        self.target_entry.delete(0, tk.END)
        self.target_entry.insert(0, "127.0.0.1")
        self.start_port_entry.delete(0, tk.END)
        self.start_port_entry.insert(0, "1")
        self.end_port_entry.delete(0, tk.END)
        self.end_port_entry.insert(0, "1024")
        self.clear_results()
        self.progress_var.set(0)

    def clear_results(self):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete('1.0', tk.END)
        self.results_text.config(state=tk.DISABLED)

    def save_results(self):
        try:
            with open("scan_results.txt", "w") as f:
                f.write(self.results_text.get('1.0', tk.END))
            messagebox.showinfo("Success", "✅ Results saved to scan_results.txt")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def copy_results(self):
        if self.results_text.get('1.0', tk.END):
            self.root.clipboard_clear()
            self.root.clipboard_append(self.results_text.get('1.0', tk.END))
            messagebox.showinfo("Success", "✅ Results copied to clipboard")


def main():
    root = tk.Tk()
    app = PortScannerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
