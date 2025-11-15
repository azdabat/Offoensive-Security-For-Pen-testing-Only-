GitHub README.md
markdown
# PyScanMaster 🔍

**Advanced Python Port Scanner for Security Professionals**

> ⚠️ **WARNING**: This tool is for authorized security testing and educational purposes only. Use only on systems you own or have explicit permission to scan.

## Features

- 🚀 **Multi-threaded Scanning**: Fast concurrent port scanning
- 🎯 **Multiple Scan Types**: Single target, network range, custom scans
- 🔍 **Service Detection**: Automatic service identification
- 🏷️ **Banner Grabbing**: Retrieve service banners for fingerprinting
- 📊 **Export Results**: JSON, CSV, and text format exports
- 🌐 **Network Discovery**: Ping sweep for active host discovery
- ⚡ **Quick Scans**: Pre-defined common port lists
- 🛡️ **Safe Scanning**: Configurable timeouts and thread limits

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/pyscanmaster.git
cd pyscanmaster

# No external dependencies required!
# Uses only Python standard library
Quick Start
Interactive Mode
bash
python3 pyscanmaster.py
Command Line Mode
bash
# Quick common ports scan
python3 pyscanmaster.py 192.168.1.1 --quick

# Custom port range scan
python3 pyscanmaster.py example.com -p 80-443 -t 200 -T 2

# Full scan with banner grabbing
python3 pyscanmaster.py 10.0.0.1 -p 1-1000 -b -t 150
Usage Guide
Step 1: Launch the Tool
bash
python3 pyscanmaster.py
You'll see the main menu:

text
╔═══════════════════════════════════════════════╗
║              PyScanMaster v2.0                ║
║           Advanced Port Scanner               ║
║         For Authorized Testing Only          ║
╚═══════════════════════════════════════════════╝

Main Menu:
1. Single Target Scan
2. Network Range Scan
3. Quick Common Ports Scan
4. Custom Port Range Scan
5. View Previous Results
6. Export Results
0. Exit
Step 2: Choose Scan Type
Option 1: Single Target Scan
Purpose: Comprehensive scan of a single host

Best for: Detailed analysis of specific targets

Features: Full port range, service detection, banner grabbing

Option 2: Network Range Scan
Purpose: Discover active hosts and scan common ports

Best for: Network reconnaissance

Example: 192.168.1.0/24

Option 3: Quick Common Ports Scan
Purpose: Fast scan of most common services

Best for: Initial reconnaissance

Ports: 21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080

Option 4: Custom Port Range Scan
Purpose: Full control over scan parameters

Best for: Targeted scanning of specific services

Step 3: Configure Scan Parameters
Common Port Lists:
Web Services: 80, 443, 8080, 8443

File Services: 21, 22, 23, 69

Email Services: 25, 110, 143, 993, 995

Database Services: 1433, 1521, 3306, 5432, 27017

Remote Access: 22, 23, 3389, 5900

Recommended Settings:
Threads: 50-200 (higher = faster, but more detectable)

Timeout: 1-3 seconds (higher = more accurate, but slower)

Banner Grabbing: Enable for service identification

Step 4: Review Results
Sample output:

text
[*] Starting scan of 192.168.1.1
[*] Scanning 100 ports with 100 threads
[*] Start time: 2024-01-15 14:30:25
--------------------------------------------------
[+] Port 22/tcp open - SSH
    Banner: SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3
[+] Port 80/tcp open - HTTP
    Banner: HTTP/1.1 200 OK...
[+] Port 443/tcp open - HTTPS

==================================================
SCAN COMPLETED
==================================================
Target: 192.168.1.1
Open ports: 3/100
Scan duration: 12.45 seconds
Step 5: Export Results
Supported formats:

JSON: For programmatic analysis

CSV: For spreadsheets and data processing

TXT: For human-readable reports

Command Line Reference
bash
# Basic usage
python3 pyscanmaster.py [TARGET] [OPTIONS]

# Options:
#   -p, --ports      Port range (default: 1-1000)
#   -t, --threads    Number of threads (default: 100)
#   -T, --timeout    Timeout in seconds (default: 1)
#   -b, --banner     Enable banner grabbing
#   -q, --quick      Quick scan common ports

# Examples:
python3 pyscanmaster.py 192.168.1.1 -q
python3 pyscanmaster.py scanme.nmap.org -p 1-500 -t 200 -b
python3 pyscanmaster.py 10.0.0.0/24 --quick
Advanced Features
Network Discovery
bash
# Perform ping sweep to find active hosts
python3 pyscanmaster.py
# Select: 2 (Network Range Scan)
# Enter: 192.168.1.0/24
Custom Port Lists
Create your own port lists by modifying the common_ports dictionary in the code.

Export Automation
bash
# Scan and auto-export to JSON
python3 pyscanmaster.py target.com -p 1-1000 -b
# Then use Export menu to save results
Ethical Usage Guidelines
✅ Authorized Activities:
Scanning your own systems

Penetration testing with written permission

Educational and research purposes

Security assessment of authorized networks

❌ Prohibited Activities:
Scanning systems without explicit permission

Network disruption or denial of service

Illegal or malicious activities

Violating terms of service

Troubleshooting
Common Issues:
Issue: socket.timeout errors
Solution: Increase timeout value with -T option

Issue: Slow scanning speed
Solution: Increase threads with -t option (use responsibly)

Issue: No open ports found
Solution: Verify target is reachable, check firewall settings

Issue: Permission errors
Solution: On Linux, may need sudo for certain scan types

Performance Tips:
Adjust Thread Count: More threads = faster scans, but more network noise

Optimize Timeout: Lower timeouts = faster, but may miss filtered ports

Use Quick Scans: For initial reconnaissance before comprehensive scanning

Network Conditions: Consider bandwidth and latency for large scans

Detection & Prevention
How to Detect Port Scanning:
Multiple connection attempts to different ports

Unusual traffic patterns from single source

Security tool alerts for reconnaissance activity

How to Protect Against Scanning:
Implement firewall rules

Use intrusion detection systems (IDS)

Monitor network traffic patterns

Regular security assessments

Legal Disclaimer
This tool is provided for educational and authorized security testing purposes only. Users are solely responsible for ensuring their compliance with all applicable laws and regulations. The authors assume no liability for misuse of this software.

Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Create a Pull Request

Support
For issues and questions:

Check the troubleshooting section above

Review closed GitHub issues

Ensure you have proper authorization for scanning

Remember: Always obtain proper authorization before scanning. Respect privacy and follow ethical guidelines.
