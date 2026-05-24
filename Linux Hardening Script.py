import os

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
    print("6. Exit")

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

    # 5. Create new user
    elif choice == "5":
        username = input("Enter username: ")

        os.system(f"adduser {username}")
        os.system(f"usermod -aG sudo {username}")

        print(f"User {username} created and added to sudo group.")

    # 6. Exit
    elif choice == "6":
        print("Exiting...")
        break

    else:
        print("Invalid choice.")