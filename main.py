import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import platform, os, shutil, socket, subprocess, psutil
from datetime import datetime

APP_TITLE = "PC Doctor"

def fmt_bytes(n):
    for unit in ["B","KB","MB","GB","TB"]:
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"

def add_text(title, content):
    win = tk.Toplevel(root)
    win.title(title)
    win.geometry("760x520")
    win.configure(bg="#101418")
    txt = tk.Text(win, wrap="word", bg="#151b21", fg="#e8eef5",
                  insertbackground="white", font=("Consolas", 10))
    txt.pack(fill="both", expand=True, padx=12, pady=12)
    txt.insert("1.0", content)
    txt.config(state="disabled")

def system_info():
    mem = psutil.virtual_memory()
    boot = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    text = f"""PC DOCTOR — SYSTEM INFORMATION

Computer: {platform.node()}
OS: {platform.system()} {platform.release()} ({platform.version()})
Architecture: {platform.machine()}
Processor: {platform.processor()}
CPU Cores: {psutil.cpu_count(logical=False)}
Logical CPUs: {psutil.cpu_count(logical=True)}
RAM: {fmt_bytes(mem.total)}
RAM Used: {mem.percent}%
Boot Time: {boot}
Python: {platform.python_version()}
"""
    add_text("System Information", text)

def disk_info():
    lines = ["PC DOCTOR — DISK SPACE", ""]
    for p in psutil.disk_partitions():
        try:
            u = psutil.disk_usage(p.mountpoint)
            lines.append(f"{p.device}  |  Total: {fmt_bytes(u.total)}  |  Free: {fmt_bytes(u.free)}  |  Used: {u.percent}%")
        except Exception:
            pass
    add_text("Disk Space", "\n".join(lines))

def network_test():
    host = "8.8.8.8"
    result = []
    result.append("PC DOCTOR — NETWORK TEST")
    result.append("")
    result.append(f"Local hostname: {socket.gethostname()}")
    try:
        result.append(f"Local IP: {socket.gethostbyname(socket.gethostname())}")
    except Exception:
        result.append("Local IP: Could not determine")
    result.append(f"Testing connection to {host}...")
    try:
        s = socket.create_connection((host, 53), timeout=3)
        s.close()
        result.append("STATUS: Internet/network connection appears reachable.")
    except Exception as e:
        result.append("STATUS: Connection test failed.")
        result.append(f"Reason: {e}")
    add_text("Network Test", "\n".join(result))

def windows_info():
    text = f"""PC DOCTOR — WINDOWS INFORMATION

System: {platform.platform()}
Release: {platform.release()}
Version: {platform.version()}
Machine: {platform.machine()}
Processor: {platform.processor()}

This tool only reads system information; it does not change Windows settings.
"""
    add_text("Windows Information", text)

def processes():
    rows = []
    for p in psutil.process_iter(["pid","name","cpu_percent","memory_percent"]):
        try:
            info = p.info
            rows.append(f'{info["pid"]:>6}  {str(info["name"])[:38]:38}  CPU {info["cpu_percent"]:5.1f}%  RAM {info["memory_percent"]:5.1f}%')
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    rows.sort()
    add_text("Running Processes", "PID     NAME                                    CPU       RAM\n" + "-"*75 + "\n" + "\n".join(rows))

def startup_apps():
    items = []

    if os.name == "nt":
        try:
            import winreg

            locations = [
                (
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Run"
                ),
                (
                    winreg.HKEY_LOCAL_MACHINE,
                    r"Software\Microsoft\Windows\CurrentVersion\Run"
                )
            ]

            for root_key, path in locations:
                try:
                    with winreg.OpenKey(root_key, path) as key:
                        i = 0

                        while True:
                            try:
                                name, value, _ = winreg.EnumValue(key, i)
                                items.append(f"{name}: {value}")
                                i += 1
                            except OSError:
                                break

                except (PermissionError, FileNotFoundError):
                    pass

        except Exception as e:
            items.append(f"Could not read startup entries: {e}")

    add_text(
        "Startup Apps",
        "PC DOCTOR — STARTUP ENTRIES\n\n"
        + (
            "\n".join(items)
            if items
            else "No entries found or this OS is not Windows."
        )
    )
    
def generate_report():
    mem = psutil.virtual_memory()
    lines = [
        "PC DOCTOR REPORT",
        "="*60,
        f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}",
        f"Computer: {platform.node()}",
        f"OS: {platform.platform()}",
        f"Processor: {platform.processor()}",
        f"CPU logical cores: {psutil.cpu_count(logical=True)}",
        f"RAM: {fmt_bytes(mem.total)} (used {mem.percent}%)",
        "",
        "DISKS:"
    ]
    for p in psutil.disk_partitions():
        try:
            u = psutil.disk_usage(p.mountpoint)
            lines.append(f"  {p.device} {fmt_bytes(u.total)} total, {fmt_bytes(u.free)} free, {u.percent}% used")
        except Exception:
            pass
    content = "\n".join(lines)
    path = filedialog.asksaveasfilename(
        title="Save PC Report",
        defaultextension=".txt",
        filetypes=[("Text file","*.txt"),("All files","*.*")]
    )
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("PC Doctor", "Report saved successfully.")

def about():
    messagebox.showinfo("About PC Doctor",
        "PC Doctor v1.0\n\nA simple Windows system information and troubleshooting helper.\n\nBuilt with Python + Tkinter + psutil.")

root = tk.Tk()
root.title(APP_TITLE)
root.geometry("760x620")
root.minsize(650, 540)
root.configure(bg="#0d1117")

style = ttk.Style()
try:
    style.theme_use("clam")
except Exception:
    pass
style.configure("TButton", font=("Segoe UI", 11), padding=10)
style.configure("TLabel", background="#0d1117", foreground="#e6edf3", font=("Segoe UI", 10))

header = tk.Frame(root, bg="#111827", height=105)
header.pack(fill="x")
tk.Label(header, text="🖥️ PC DOCTOR", bg="#111827", fg="#f3f4f6",
         font=("Segoe UI", 25, "bold")).pack(pady=(18,0))
tk.Label(header, text="Windows System Information & Troubleshooting Helper",
         bg="#111827", fg="#9ca3af", font=("Segoe UI", 10)).pack()

main = tk.Frame(root, bg="#0d1117")
main.pack(fill="both", expand=True, padx=28, pady=22)

buttons = [
    ("System Information", system_info),
    ("Check Disk Space", disk_info),
    ("Network Test", network_test),
    ("Windows Information", windows_info),
    ("Running Processes", processes),
    ("Startup Apps", startup_apps),
    ("Generate PC Report", generate_report),
    ("About", about),
]
for i, (label, cmd) in enumerate(buttons):
    b = ttk.Button(main, text=label, command=cmd)
    b.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="ew")
main.columnconfigure(0, weight=1)
main.columnconfigure(1, weight=1)

tk.Label(root, text="PC Doctor v1.0  •  Read-only diagnostic tools",
         bg="#0d1117", fg="#6b7280", font=("Segoe UI", 9)).pack(pady=(0,15))

root.mainloop()
