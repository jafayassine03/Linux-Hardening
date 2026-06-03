# Advanced Linux Hardening Tool

A terminal-based Linux security and system administration tool written in Python.

This tool helps system administrators and Linux users perform common hardening tasks, security checks, monitoring, and maintenance from a single interactive menu.

---

## Features

### System Maintenance

* Update and upgrade system packages
* Check available updates
* View system information
* Check disk usage
* Monitor CPU and RAM usage
* Reboot or shut down the system

### User Management

* Create new sudo users
* Lock user accounts
* Unlock user accounts
* View active users
* Check sudo group members
* Detect UID 0 accounts

### SSH Security

* Disable root SSH login
* Change SSH port

### Firewall & Protection

* Enable UFW firewall
* Install and configure Fail2Ban
* Install ClamAV antivirus
* Secure shared memory

### Security Auditing

* Check open ports
* View running services
* Review failed login attempts
* Scan for world-writable files
* Run a basic security audit
* View command logs

### Utilities

* Generate secure random passwords
* Backup important system configuration files
* Check internet connectivity
* Display kernel version

---

## Requirements

* Python 3.8+
* Linux operating system
* Root privileges
* APT package manager

Supported distributions include:

* Ubuntu
* Debian
* Linux Mint
* Kali Linux
* Other Debian-based distributions

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/linux-hardening-tool.git
cd linux-hardening-tool
```

Make the script executable:

```bash
chmod +x hardening_tool.py
```

Run the tool as root:

```bash
sudo python3 hardening_tool.py
```

---

## Usage

Start the program:

```bash
sudo python3 hardening_tool.py
```

Select an option from the menu and follow the prompts.

Example:

```text
1 - Update system
2 - Enable firewall
3 - Disable root SSH login
...
31 - Exit
```

---

## Log File

All executed commands are logged to:

```text
/var/log/linux_hardening_tool.log
```

Logs can be viewed directly from the application menu or manually:

```bash
cat /var/log/linux_hardening_tool.log
```

---

## Backup Location

Configuration backups are stored in:

```text
/root/security_backups
```

Backed up files include:

```text
/etc/passwd
/etc/group
/etc/shadow
/etc/ssh/sshd_config
```

---

## Security Notice

This tool modifies system configuration files and services.

Always:

* Review changes before applying them
* Test on a non-production system first
* Create backups before making major changes
* Ensure you have an alternative login method before modifying SSH settings

The authors are not responsible for system damage, data loss, or service interruptions resulting from the use of this software.

---

## Project Structure

```text
linux-hardening-tool/
│
├── hardening_tool.py
├── README.md
└── LICENSE
```

---

## Future Improvements

* Automatic security report generation
* Lynis integration
* Malware scanning reports
* Email notifications
* Scheduled security audits
* Configuration restore feature
* Export results to PDF

---

## License

This project is released under the MIT License.

You are free to use, modify, and distribute this software for personal, educational, and commercial purposes.
