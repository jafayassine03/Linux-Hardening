import os
import random
import string
import socket
import subprocess
import time
from datetime import datetime

LOG_FILE = "/var/log/linux_hardening_tool.log"


def log_action(action):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"[{datetime.now()}] {action}\n")
    except Exception:
        pass


def run(cmd):
    print()
    subprocess.run(cmd, shell=True)
    log_action(cmd)


def password(length):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(random.choice(chars) for _ in range(length))


def pause():
    input("\nPress Enter to continue...")


if os.geteuid() != 0:
    print("Run as root.")
    raise SystemExit

while True:

    print("\n" + "=" * 40)
    print("ADVANCED LINUX HARDENING TOOL")
    print("=" * 40)

    print("1  - Update system")
    print("2  - Enable firewall")
    print("3  - Disable root SSH login")
    print("4  - Change SSH port")
    print("5  - Create sudo user")
    print("6  - Password policy")
    print("7  - Install Fail2Ban")
    print("8  - Secure shared memory")
    print("9  - Generate password")
    print("10 - Open ports")
    print("11 - Install ClamAV")
    print("12 - Disable unused services")
    print("13 - System information")
    print("14 - Failed logins")
    print("15 - Backup configs")
    print("16 - World writable files")
    print("17 - Lock user")
    print("18 - Unlock user")
    print("19 - Running services")
    print("20 - Disk usage")
    print("21 - CPU and RAM")
    print("22 - Active users")
    print("23 - Internet test")
    print("24 - Security audit")
    print("25 - Available updates")
    print("26 - View logs")
    print("27 - Sudo users")
    print("28 - Kernel version")
    print("29 - Reboot")
    print("30 - Shutdown")
    print("31 - Exit")

    choice = input("\nChoice: ").strip()

    if choice == "1":
        run("apt update && apt upgrade -y")

    elif choice == "2":
        run("ufw allow OpenSSH")
        run("ufw --force enable")

    elif choice == "3":
        run("sed -i 's/^#*PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config")
        run("systemctl restart ssh")

    elif choice == "4":
        port = input("New SSH port: ")

        if port.isdigit():
            run(f"sed -i 's/^#*Port.*/Port {port}/' /etc/ssh/sshd_config")
            run(f"ufw allow {port}/tcp")
            run("systemctl restart ssh")
        else:
            print("Invalid port.")

    elif choice == "5":
        user = input("Username: ")
        run(f"adduser {user}")
        run(f"usermod -aG sudo {user}")

    elif choice == "6":
        run("sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS 90/' /etc/login.defs")
        run("sed -i 's/^PASS_MIN_DAYS.*/PASS_MIN_DAYS 7/' /etc/login.defs")
        run("sed -i 's/^PASS_WARN_AGE.*/PASS_WARN_AGE 14/' /etc/login.defs")

    elif choice == "7":
        run("apt install fail2ban -y")
        run("systemctl enable fail2ban")
        run("systemctl start fail2ban")

    elif choice == "8":
        run("grep -q '/run/shm' /etc/fstab || echo 'tmpfs /run/shm tmpfs defaults,noexec,nosuid 0 0' >> /etc/fstab")
        run("mount -o remount /run/shm")

    elif choice == "9":
        try:
            length = int(input("Length: "))
            print("\n" + password(length))
        except ValueError:
            print("Invalid length.")

    elif choice == "10":
        run("ss -tulnp")

    elif choice == "11":
        run("apt install clamav clamav-daemon -y")
        run("freshclam")

    elif choice == "12":
        for svc in ["telnet", "rpcbind", "avahi-daemon"]:
            run(f"systemctl disable {svc} 2>/dev/null")
            run(f"systemctl stop {svc} 2>/dev/null")

    elif choice == "13":
        print(f"\nHostname: {socket.gethostname()}")
        run("uname -a")
        run("uptime")
        run("free -h")
        run("df -h")

    elif choice == "14":
        run("lastb | head -20")

    elif choice == "15":
        backup = "/root/security_backups"
        run(f"mkdir -p {backup}")

        for f in [
            "/etc/passwd",
            "/etc/group",
            "/etc/shadow",
            "/etc/ssh/sshd_config",
        ]:
            run(f"cp {f} {backup}")

    elif choice == "16":
        run("find / -type f -perm -0002 2>/dev/null | head -50")

    elif choice == "17":
        user = input("User to lock: ")
        run(f"passwd -l {user}")

    elif choice == "18":
        user = input("User to unlock: ")
        run(f"passwd -u {user}")

    elif choice == "19":
        run("systemctl list-units --type=service --state=running")

    elif choice == "20":
        run("du -sh /* 2>/dev/null | sort -h")

    elif choice == "21":
        run("top")

    elif choice == "22":
        run("who")
        run("w")

    elif choice == "23":
        result = os.system("ping -c 1 8.8.8.8 > /dev/null 2>&1")
        print("Internet is active." if result == 0 else "No connection.")

    elif choice == "24":

        print("\nFIREWALL")
        run("ufw status")

        print("\nSSH")
        run("grep PermitRootLogin /etc/ssh/sshd_config")

        print("\nFAIL2BAN")
        run("systemctl is-active fail2ban")

        print("\nPORTS")
        run("ss -tulnp")

    elif choice == "25":
        run("apt update")
        run("apt list --upgradable")

    elif choice == "26":
        if os.path.exists(LOG_FILE):
            run(f"cat {LOG_FILE}")
        else:
            print("No logs found.")

    elif choice == "27":

        print("\nSudo Group")
        run("getent group sudo")

        print("\nUID 0 Accounts")
        run("awk -F: '$3 == 0 {print $1}' /etc/passwd")

    elif choice == "28":
        run("uname -r")

    elif choice == "29":
        confirm = input("Reboot system? (yes/no): ")
        if confirm.lower() == "yes":
            run("reboot")

    elif choice == "30":
        confirm = input("Shutdown system? (yes/no): ")
        if confirm.lower() == "yes":
            run("shutdown now")

    elif choice == "31":
        print("Goodbye.")
        break

    else:
        print("Invalid choice.")

    time.sleep(1)
    pause()