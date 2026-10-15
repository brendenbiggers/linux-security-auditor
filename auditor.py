import platform
import socket
from datetime import datetime
import subprocess
import json

# Structured security report
security_report = {
    "system": {},
    "checks": []
}

security_report["system"] = {
    "hostname": socket.gethostname(),
    "operating_system": platform.system(),
    "kernel": platform.release(),
    "scan_time": datetime.now().isoformat()
}

print("=" * 50)
print("       LINUX SECURITY AUDITOR")
print("=" * 50)

print(f"Hostname: {socket.gethostname()}")
print(f"Operating System: {platform.system()}")
print(f"Kernel Version: {platform.release()}")
print(f"Scan Time: {datetime.now()}")

print("=" * 50)
print("\n[+] FIREWALL SECURITY CHECK")

try:
    result = subprocess.run(
        ["firewall-cmd", "--get-default-zone"],
        capture_output=True,
        text=True,
        timeout=10,
        check=True
    )

    zone = result.stdout.strip()

    print(f"Default Firewall Zone: {zone}")

    if zone == "public":
        print("[PASS] Default firewall zone is public.")
        finding = "PASS"
    else:
        print("[REVIEW] Default firewall zone is not public.")
        finding = "REVIEW"

    security_report["checks"].append({
        "name": "Default Firewall Zone",
        "status": finding,
        "result": zone
    })

except FileNotFoundError:
    print("[ERROR] firewall-cmd was not found.")

except subprocess.TimeoutExpired:
    print("[ERROR] Firewall command timed out.")

except subprocess.CalledProcessError as error:
    print(f"[ERROR] {error.stderr.strip()}")
    print("\n[+] SSH SERVER SECURITY CHECK")

print("\n[+] SSH SERVER SECURITY CHECK")   

try:
    result = subprocess.run(
        ["systemctl", "is-active", "sshd"],
        capture_output=True,
        text=True,
        timeout=10
    )

    status = result.stdout.strip()

    print(f"SSH Server Status: {status}")

    if status == "inactive":
        print("[PASS] SSH server is not running.")
        finding = "PASS"
    elif status == "active":
        print("[REVIEW] SSH server is running.")
        finding = "REVIEW"
    else:
        print(f"[INFO] SSH server status: {status}")
        finding = "INFO"

    security_report["checks"].append({
        "name": "SSH Server",
        "status": finding,
        "result": status
    })

except FileNotFoundError:
    print("[ERROR] systemctl was not found.")

except subprocess.TimeoutExpired:
    print("[ERROR] SSH status check timed out.")
    print("\n[+] NETWORK PORT SECURITY CHECK")

print("\n[+] NETWORK PORT SECURITY CHECK")

try:
    result = subprocess.run(
        ["ss", "-tuln"],
        capture_output=True,
        text=True,
        timeout=10,
        check=True
    )

    print("[+] CHECKING FOR KDE CONNECT")

    port_1716_open = any(
        line.split()[4].endswith(":1716")
        for line in result.stdout.splitlines()[1:]
        if len(line.split()) >= 5
    )

    if port_1716_open:
        print("[REVIEW] Port 1716 is listening (KDE Connect uses this port).")
        finding = "REVIEW"
    else:
        print("[PASS] No listener found on port 1716.")
        finding = "PASS"

    security_report["checks"].append({
        "name": "Network Port 1716",
        "status": finding,
        "result": "listening" if port_1716_open else "not listening"
    })

    print(result.stdout)

except FileNotFoundError:
    print("[ERROR] ss command not found.")

except subprocess.TimeoutExpired:
    print("[ERROR] Network scan timed out.")

except subprocess.CalledProcessError as error:
    print(f"[ERROR] {error.stderr.strip()}")

    # Export structured security report
with open("security-report.json", "w") as report_file:
    json.dump(security_report, report_file, indent=4)

print("\n[+] JSON security report generated successfully.")