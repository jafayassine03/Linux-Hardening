import os
import random
import string

print("=== Simple Linux Hardening Tool ===")

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
    print("10. Exit")

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
        print("Exiting...")
        break

    else:
        print("Invalid choice.")