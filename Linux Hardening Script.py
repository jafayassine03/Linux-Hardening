import os
import random
import string
import socket
import subprocess
import time

print("=== Advanced Linux Hardening Tool ===")

if os.geteuid() != 0:
    print("Please run this script as root.")
    exit()

while True:
    print("\nChoose an option:")
    print("1. Update system")
    print("2. Enable firewall")
    print("3. Disable root SSH login")
    print("4. Change SSH port")
    print("5. Create new user")
    print("6. Set password policy")
    print("7. Install Fail2Ban")
    print("8. Secure shared memory")
    print("9. Generate random password")
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
    print("24. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        print("Updating system...")
        os.system("apt update && apt upgrade -y")

    elif choice == "2":
        print("Enabling firewall...")
        os.system("ufw allow OpenSSH")
        os.system("ufw --force enable")
        print("Firewall enabled.")

    elif choice == "3":
        print("Disabling root SSH login...")

        os.system(
            "sed -i 's/^#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config"
        )

        os.system(
            "sed -i 's/^PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config"
        )

        os.system("systemctl restart ssh")

        print("Root SSH login disabled.")

    elif choice == "4":
        new_port = input("Enter new SSH port: ")

        os.system(
            f"sed -i 's/^#Port 22/Port {new_port}/' /etc/ssh/sshd_config"
        )

        os.system(
            f"sed -i 's/^Port 22/Port {new_port}/' /etc/ssh/sshd_config"
        )

        os.system(f"ufw allow {new_port}/tcp")
        os.system("systemctl restart ssh")

        print(f"SSH port changed to {new_port}")

    elif choice == "5":
        username = input("Enter username: ")

        os.system(f"adduser {username}")
        os.system(f"usermod -aG sudo {username}")

        print(f"User {username} created and added to sudo group.")

    elif choice == "6":
        print("Setting password policy...")

        os.system(
            "sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS   90/' /etc/login.defs"
        )

        os.system(
            "sed -i 's/^PASS_MIN_DAYS.*/PASS_MIN_DAYS   7/' /etc/login.defs"
        )

        os.system(
            "sed -i 's/^PASS_WARN_AGE.*/PASS_WARN_AGE   14/' /etc/login.defs"
        )

        print("Password policy updated.")

    elif choice == "7":
        print("Installing Fail2Ban...")

        os.system("apt install fail2ban -y")
        os.system("systemctl enable fail2ban")
        os.system("systemctl start fail2ban")

        print("Fail2Ban installed and running.")

    elif choice == "8":
        print("Securing shared memory...")

        os.system(
            "echo 'tmpfs /run/shm tmpfs defaults,noexec,nosuid 0 0' >> /etc/fstab"
        )

        os.system("mount -o remount /run/shm")

        print("Shared memory secured.")

    elif choice == "9":
        length = int(input("Enter password length: "))

        chars = string.ascii_letters + string.digits + "!@#$%^&*"

        password = "".join(random.choice(chars) for _ in range(length))

        print(f"Generated Password: {password}")

    elif choice == "10":
        print("Showing open ports...")
        os.system("ss -tulnp")

    elif choice == "11":
        print("Installing ClamAV antivirus...")

        os.system("apt install clamav clamav-daemon -y")
        os.system("freshclam")
        os.system("systemctl enable clamav-daemon")
        os.system("systemctl start clamav-daemon")

        print("ClamAV installed.")

    elif choice == "12":
        print("Disabling unused services...")

        services = ["telnet", "rpcbind", "avahi-daemon"]

        for service in services:
            os.system(f"systemctl disable {service} 2>/dev/null")
            os.system(f"systemctl stop {service} 2>/dev/null")

        print("Unused services disabled.")

    elif choice == "13":
        print("\n=== System Information ===")

        hostname = socket.gethostname()

        print(f"Hostname: {hostname}")

        os.system("uname -a")
        os.system("uptime")
        os.system("df -h")
        os.system("free -h")

    elif choice == "14":
        print("Checking failed login attempts...")
        os.system("lastb | head")

    elif choice == "15":
        backup_dir = "/root/security_backups"

        os.system(f"mkdir -p {backup_dir}")

        files = [
            "/etc/ssh/sshd_config",
            "/etc/passwd",
            "/etc/shadow",
            "/etc/group"
        ]

        for file in files:
            os.system(f"cp {file} {backup_dir}")

        print(f"Configs backed up to {backup_dir}")

    elif choice == "16":
        print("Scanning for world writable files...")
        os.system("find / -type f -perm -0002 2>/dev/null | head -50")

    elif choice == "17":
        username = input("Enter username to lock: ")

        os.system(f"passwd -l {username}")

        print(f"User {username} locked.")

    elif choice == "18":
        username = input("Enter username to unlock: ")

        os.system(f"passwd -u {username}")

        print(f"User {username} unlocked.")

    elif choice == "19":
        print("Checking listening services...")
        os.system("systemctl list-units --type=service --state=running")

    elif choice == "20":
        print("Checking disk usage...")
        os.system("du -sh /* 2>/dev/null | sort -h")

    elif choice == "21":
        print("Monitoring CPU and RAM...")
        os.system("top")

    elif choice == "22":
        confirm = input("Are you sure you want to reboot? (yes/no): ")

        if confirm.lower() == "yes":
            os.system("reboot")

    elif choice == "23":
        confirm = input("Are you sure you want to shutdown? (yes/no): ")

        if confirm.lower() == "yes":
            os.system("shutdown now")

    elif choice == "24":
        print("Exiting...")
        break

    else:
        print("Invalid choice.")

    time.sleep(2)