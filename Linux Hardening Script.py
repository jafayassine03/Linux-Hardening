import os
import random
import string
import socket
import time
from datetime import datetime

LOG_FILE = "/var/log/linux_hardening_tool.log"


def log_action(action):
    try:
        with open(LOG_FILE, "a") as log:
            log.write(f"[{datetime.now()}] {action}\n")
    except:
        pass


def run_command(command):
    os.system(command)
    log_action(f"Executed command: {command}")


def generate_password(length):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(random.choice(chars) for _ in range(length))


print("====================================")
print("   ADVANCED LINUX HARDENING TOOL")
print("====================================")

if os.geteuid() != 0:
    print("Please run this script as root.")
    exit()

while True:

    print("\nChoose an option:")
    print("1.  Update system")
    print("2.  Enable firewall")
    print("3.  Disable root SSH login")
    print("4.  Change SSH port")
    print("5.  Create new user")
    print("6.  Set password policy")
    print("7.  Install Fail2Ban")
    print("8.  Secure shared memory")
    print("9.  Generate random password")
    print("10. Show open ports")
    print("11. Install ClamAV")
    print("12. Disable unused services")
    print("13. System information")
    print("14. Check failed login attempts")
    print("15. Backup important configs")
    print("16. Scan for world writable files")
    print("17. Lock a user account")
    print("18. Unlock a user account")
    print("19. Check listening services")
    print("20. Check disk usage")
    print("21. Monitor CPU and RAM")
    print("22. Reboot system")
    print("23. Shutdown system")
    print("24. Check active users")
    print("25. Check internet connectivity")
    print("26. Security audit")
    print("27. Check updates only")
    print("28. View logs")
    print("29. Exit")

    choice = input("\nEnter choice: ")

    if choice == "1":
        print("Updating system...")
        run_command("apt update && apt upgrade -y")

    elif choice == "2":
        print("Enabling firewall...")
        run_command("ufw allow OpenSSH")
        run_command("ufw --force enable")
        print("Firewall enabled.")

    elif choice == "3":
        print("Disabling root SSH login...")

        run_command(
            "sed -i 's/^#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config"
        )

        run_command(
            "sed -i 's/^PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config"
        )

        run_command("systemctl restart ssh")

        print("Root SSH login disabled.")

    elif choice == "4":

        new_port = input("Enter new SSH port: ")

        if not new_port.isdigit():
            print("Invalid port.")
            continue

        run_command(
            f"sed -i 's/^#Port 22/Port {new_port}/' /etc/ssh/sshd_config"
        )

        run_command(
            f"sed -i 's/^Port 22/Port {new_port}/' /etc/ssh/sshd_config"
        )

        run_command(f"ufw allow {new_port}/tcp")
        run_command("systemctl restart ssh")

        print(f"SSH port changed to {new_port}")

    elif choice == "5":

        username = input("Enter username: ")

        run_command(f"adduser {username}")
        run_command(f"usermod -aG sudo {username}")

        print(f"User {username} created and added to sudo group.")

    elif choice == "6":

        print("Setting password policy...")

        run_command(
            "sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS   90/' /etc/login.defs"
        )

        run_command(
            "sed -i 's/^PASS_MIN_DAYS.*/PASS_MIN_DAYS   7/' /etc/login.defs"
        )

        run_command(
            "sed -i 's/^PASS_WARN_AGE.*/PASS_WARN_AGE   14/' /etc/login.defs"
        )

        print("Password policy updated.")

    elif choice == "7":

        print("Installing Fail2Ban...")

        run_command("apt install fail2ban -y")
        run_command("systemctl enable fail2ban")
        run_command("systemctl start fail2ban")

        print("Fail2Ban installed and running.")

    elif choice == "8":

        print("Securing shared memory...")

        run_command(
            "echo 'tmpfs /run/shm tmpfs defaults,noexec,nosuid 0 0' >> /etc/fstab"
        )

        run_command("mount -o remount /run/shm")

        print("Shared memory secured.")

    elif choice == "9":

        try:
            length = int(input("Enter password length: "))

            if length < 4:
                print("Password length too short.")
                continue

            password = generate_password(length)

            print(f"\nGenerated Password:\n{password}")

            log_action("Generated random password")

        except:
            print("Invalid length.")

    elif choice == "10":

        print("Showing open ports...")
        run_command("ss -tulnp")

    elif choice == "11":

        print("Installing ClamAV antivirus...")

        run_command("apt install clamav clamav-daemon -y")
        run_command("freshclam")
        run_command("systemctl enable clamav-daemon")
        run_command("systemctl start clamav-daemon")

        print("ClamAV installed.")

    elif choice == "12":

        print("Disabling unused services...")

        services = ["telnet", "rpcbind", "avahi-daemon"]

        for service in services:
            run_command(f"systemctl disable {service} 2>/dev/null")
            run_command(f"systemctl stop {service} 2>/dev/null")

        print("Unused services disabled.")

    elif choice == "13":

        print("\n=== System Information ===")

        hostname = socket.gethostname()

        print(f"Hostname: {hostname}")

        run_command("uname -a")
        run_command("uptime")
        run_command("df -h")
        run_command("free -h")

    elif choice == "14":

        print("Checking failed login attempts...")
        run_command("lastb | head")

    elif choice == "15":

        backup_dir = "/root/security_backups"

        run_command(f"mkdir -p {backup_dir}")

        files = [
            "/etc/ssh/sshd_config",
            "/etc/passwd",
            "/etc/shadow",
            "/etc/group"
        ]

        for file in files:
            run_command(f"cp {file} {backup_dir}")

        print(f"Configs backed up to {backup_dir}")

    elif choice == "16":

        print("Scanning for world writable files...")
        run_command("find / -type f -perm -0002 2>/dev/null | head -50")

    elif choice == "17":

        username = input("Enter username to lock: ")

        run_command(f"passwd -l {username}")

        print(f"User {username} locked.")

    elif choice == "18":

        username = input("Enter username to unlock: ")

        run_command(f"passwd -u {username}")

        print(f"User {username} unlocked.")

    elif choice == "19":

        print("Checking listening services...")
        run_command("systemctl list-units --type=service --state=running")

    elif choice == "20":

        print("Checking disk usage...")
        run_command("du -sh /* 2>/dev/null | sort -h")

    elif choice == "21":

        print("Monitoring CPU and RAM...")
        run_command("top")

    elif choice == "22":

        confirm = input("Are you sure you want to reboot? (yes/no): ")

        if confirm.lower() == "yes":
            run_command("reboot")

    elif choice == "23":

        confirm = input("Are you sure you want to shutdown? (yes/no): ")

        if confirm.lower() == "yes":
            run_command("shutdown now")

    elif choice == "24":

        print("Checking active users...")
        run_command("who")
        run_command("w")

    elif choice == "25":

        print("Checking internet connectivity...")

        response = os.system("ping -c 1 google.com > /dev/null 2>&1")

        if response == 0:
            print("Internet connection is ACTIVE.")
        else:
            print("No internet connection.")

    elif choice == "26":

        print("\n=== SECURITY AUDIT ===")

        print("\n[+] Firewall Status")
        run_command("ufw status")

        print("\n[+] SSH Root Login")
        run_command("grep PermitRootLogin /etc/ssh/sshd_config")

        print("\n[+] Fail2Ban Status")
        run_command("systemctl status fail2ban --no-pager")

        print("\n[+] Open Ports")
        run_command("ss -tulnp")

        print("\n[+] Running Services")
        run_command("systemctl list-units --type=service --state=running")

    elif choice == "27":

        print("Checking available updates...")
        run_command("apt update")
        run_command("apt list --upgradable")

    elif choice == "28":

        print(f"\nShowing logs from {LOG_FILE}\n")

        if os.path.exists(LOG_FILE):
            run_command(f"cat {LOG_FILE}")
        else:
            print("No logs found.")

    elif choice == "29":

        print("Exiting...")
        break

    else:
        print("Invalid choice.")

    time.sleep(2)