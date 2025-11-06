#!/usr/bin/env python3
"""
PyScanMaster - Advanced Port Scanner
Author: Security Research
Version: 2.0
Features: Multi-threading, Service Detection, Banner Grabbing, Export Results
"""

import socket
import threading
import time
import argparse
import sys
from datetime import datetime
import json
import csv
import subprocess
import os
from ipaddress import ip_network, ip_address

class PyScanMaster:
    def __init__(self):
        self.open_ports = []
        self.scan_results = []
        self.common_ports = {
            'web': [80, 443, 8080, 8443],
            'file': [21, 22, 23, 69],
            'email': [25, 110, 143, 993, 995],
            'database': [1433, 1521, 3306, 5432, 27017],
            'remote': [22, 23, 3389, 5900],
            'all_common': [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
        }
        self.scan_stats = {
            'start_time': None,
            'end_time': None,
            'hosts_scanned': 0,
            'ports_found': 0
        }

    def display_banner(self):
        banner = """
╔═══════════════════════════════════════════════╗
║              PyScanMaster v2.0                ║
║           Advanced Port Scanner               ║
║         For Authorized Testing Only          ║
╚═══════════════════════════════════════════════╝
        """
        print(banner)

    def validate_target(self, target):
        """Validate target IP or domain"""
        try:
            # Check if it's an IP address
            ip_address(target)
            return True
        except:
            # Check if it's a domain
            try:
                socket.gethostbyname(target)
                return True
            except socket.gaierror:
                return False

    def validate_port_range(self, port_range):
        """Validate port range format"""
        try:
            if '-' in port_range:
                start, end = map(int, port_range.split('-'))
                return 1 <= start <= 65535 and 1 <= end <= 65535 and start <= end
            else:
                port = int(port_range)
                return 1 <= port <= 65535
        except:
            return False

    def scan_port(self, target, port, timeout=1, banner_grab=False):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            
            if result == 0:
                service_name = "Unknown"
                banner = ""
                
                if banner_grab:
                    try:
                        sock.settimeout(2)
                        # Try to receive banner
                        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                        # Get service name
                        service_name = socket.getservbyport(port, 'tcp')
                    except:
                        service_name = self.get_service_name(port)
                        banner = "No banner"
                
                result_data = {
                    'port': port,
                    'state': 'open',
                    'service': service_name,
                    'banner': banner
                }
                
                self.open_ports.append(port)
                self.scan_results.append(result_data)
                
                print(f"[+] Port {port}/tcp open - {service_name}")
                if banner and banner != "No banner":
                    print(f"    Banner: {banner[:100]}...")
                
            sock.close()
        except Exception as e:
            pass

    def get_service_name(self, port):
        """Get service name for common ports"""
        service_map = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
            80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS', 993: 'IMAPS',
            995: 'POP3S', 1433: 'MSSQL', 1521: 'Oracle', 3306: 'MySQL',
            3389: 'RDP', 5432: 'PostgreSQL', 5900: 'VNC', 27017: 'MongoDB'
        }
        return service_map.get(port, 'Unknown')

    def thread_scan(self, target, ports, timeout, banner_grab, max_threads=100):
        """Multi-threaded port scanning"""
        threads = []
        
        for port in ports:
            while threading.active_count() > max_threads:
                time.sleep(0.1)
            
            thread = threading.Thread(
                target=self.scan_port, 
                args=(target, port, timeout, banner_grab)
            )
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def ping_sweep(self, network):
        """Perform ping sweep to find active hosts"""
        active_hosts = []
        print(f"[*] Performing ping sweep on {network}")
        
        try:
            # Create list of IPs in the network
            network_obj = ip_network(network, strict=False)
            ips = [str(ip) for ip in network_obj.hosts()]
            
            def ping_host(ip):
                try:
                    if os.name == 'nt':  # Windows
                        param = '-n'
                    else:  # Linux/Mac
                        param = '-c'
                    
                    result = subprocess.run(
                        ['ping', param, '1', '-W', '1000', ip],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    
                    if result.returncode == 0:
                        active_hosts.append(ip)
                        print(f"[+] Host active: {ip}")
                except:
                    pass
            
            # Multi-threaded ping
            threads = []
            for ip in ips[:254]:  # Limit to first 254 hosts
                thread = threading.Thread(target=ping_host, args=(ip,))
                thread.daemon = True
                thread.start()
                threads.append(thread)
            
            for thread in threads:
                thread.join()
                
        except Exception as e:
            print(f"[-] Ping sweep error: {e}")
        
        return active_hosts

    def export_results(self, format_type, filename=None):
        """Export scan results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scan_results_{timestamp}.{format_type}"
        
        try:
            if format_type == 'json':
                with open(filename, 'w') as f:
                    json.dump({
                        'scan_time': self.scan_stats['start_time'].isoformat(),
                        'target': getattr(self, 'current_target', 'Unknown'),
                        'results': self.scan_results
                    }, f, indent=2)
            
            elif format_type == 'csv':
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Port', 'State', 'Service', 'Banner'])
                    for result in self.scan_results:
                        writer.writerow([
                            result['port'],
                            result['state'],
                            result['service'],
                            result['banner'][:100]  # Limit banner length
                        ])
            
            elif format_type == 'txt':
                with open(filename, 'w') as f:
                    f.write(f"Scan Results - {self.scan_stats['start_time']}\n")
                    f.write(f"Target: {getattr(self, 'current_target', 'Unknown')}\n")
                    f.write("="*50 + "\n")
                    for result in self.scan_results:
                        f.write(f"Port {result['port']}/tcp - {result['service']}\n")
                        if result['banner']:
                            f.write(f"Banner: {result['banner']}\n")
                        f.write("-" * 30 + "\n")
            
            print(f"[+] Results exported to: {filename}")
            return True
            
        except Exception as e:
            print(f"[-] Export failed: {e}")
            return False

    def main_menu(self):
        """Main interactive menu"""
        while True:
            self.display_banner()
            print("Main Menu:")
            print("1. Single Target Scan")
            print("2. Network Range Scan")
            print("3. Quick Common Ports Scan")
            print("4. Custom Port Range Scan")
            print("5. View Previous Results")
            print("6. Export Results")
            print("0. Exit")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                self.single_target_scan()
            elif choice == "2":
                self.network_scan()
            elif choice == "3":
                self.quick_scan()
            elif choice == "4":
                self.custom_scan()
            elif choice == "5":
                self.view_results()
            elif choice == "6":
                self.export_menu()
            elif choice == "0":
                print("[*] Thank you for using PyScanMaster!")
                break
            else:
                print("[-] Invalid option")
            
            input("\nPress Enter to continue...")

    def single_target_scan(self):
        """Scan a single target"""
        print("\n=== Single Target Scan ===")
        target = input("Enter target IP or domain: ").strip()
        
        if not self.validate_target(target):
            print("[-] Invalid target. Please enter a valid IP or domain.")
            return
        
        print("\nPort Selection:")
        print("1. Common Ports (Top 100)")
        print("2. Web Services (80, 443, 8080, 8443)")
        print("3. All Common Services (Top 1000)")
        print("4. Custom Range")
        
        port_choice = input("Select port range: ").strip()
        
        if port_choice == "1":
            ports = self.common_ports['all_common']
        elif port_choice == "2":
            ports = self.common_ports['web']
        elif port_choice == "3":
            ports = range(1, 1001)
        elif port_choice == "4":
            port_range = input("Enter port range (e.g., 1-1000): ").strip()
            if not self.validate_port_range(port_range):
                print("[-] Invalid port range")
                return
            start, end = map(int, port_range.split('-'))
            ports = range(start, end + 1)
        else:
            print("[-] Invalid selection")
            return
        
        timeout = float(input("Enter timeout in seconds (default 1): ") or "1")
        banner_grab = input("Enable banner grabbing? (y/n): ").lower() == 'y'
        threads = int(input("Number of threads (default 100): ") or "100")
        
        self.run_scan(target, ports, timeout, banner_grab, threads)

    def network_scan(self):
        """Scan a network range"""
        print("\n=== Network Range Scan ===")
        network = input("Enter network (e.g., 192.168.1.0/24): ").strip()
        
        try:
            active_hosts = self.ping_sweep(network)
            if not active_hosts:
                print("[-] No active hosts found")
                return
            
            print(f"\n[*] Found {len(active_hosts)} active hosts")
            
            # Scan common ports on active hosts
            ports = self.common_ports['all_common']
            
            for host in active_hosts:
                print(f"\n[*] Scanning {host}...")
                self.run_scan(host, ports, timeout=1, banner_grab=False, threads=50, brief=True)
                
        except Exception as e:
            print(f"[-] Network scan error: {e}")

    def quick_scan(self):
        """Quick scan common ports"""
        print("\n=== Quick Common Ports Scan ===")
        target = input("Enter target IP or domain: ").strip()
        
        if not self.validate_target(target):
            print("[-] Invalid target")
            return
        
        self.run_scan(target, self.common_ports['all_common'], timeout=0.5, banner_grab=True, threads=100)

    def custom_scan(self):
        """Fully customizable scan"""
        print("\n=== Custom Scan ===")
        target = input("Enter target IP or domain: ").strip()
        
        if not self.validate_target(target):
            print("[-] Invalid target")
            return
        
        port_range = input("Enter port range (e.g., 1-1000): ").strip()
        if not self.validate_port_range(port_range):
            print("[-] Invalid port range")
            return
        
        start, end = map(int, port_range.split('-'))
        ports = range(start, end + 1)
        
        timeout = float(input("Enter timeout (default 1): ") or "1")
        banner_grab = input("Enable banner grabbing? (y/n): ").lower() == 'y'
        threads = int(input("Number of threads (default 100): ") or "100")
        
        self.run_scan(target, ports, timeout, banner_grab, threads)

    def run_scan(self, target, ports, timeout=1, banner_grab=False, threads=100, brief=False):
        """Execute the port scan"""
        self.open_ports = []
        self.scan_results = []
        self.current_target = target
        self.scan_stats['start_time'] = datetime.now()
        self.scan_stats['hosts_scanned'] = 1
        
        total_ports = len(ports)
        print(f"\n[*] Starting scan of {target}")
        print(f"[*] Scanning {total_ports} ports with {threads} threads")
        print(f"[*] Start time: {self.scan_stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
        
        start_time = time.time()
        
        # Run the scan
        self.thread_scan(target, ports, timeout, banner_grab, threads)
        
        # Calculate scan duration
        scan_duration = time.time() - start_time
        self.scan_stats['end_time'] = datetime.now()
        self.scan_stats['ports_found'] = len(self.open_ports)
        
        # Display results
        print("\n" + "=" * 50)
        print("SCAN COMPLETED")
        print("=" * 50)
        print(f"Target: {target}")
        print(f"Open ports: {len(self.open_ports)}/{total_ports}")
        print(f"Scan duration: {scan_duration:.2f} seconds")
        
        if not brief:
            if self.open_ports:
                print("\nOpen Ports:")
                for result in self.scan_results:
                    print(f"  {result['port']}/tcp - {result['service']}")
                    if result['banner'] and result['banner'] != "No banner":
                        print(f"    Banner: {result['banner'][:100]}...")
            else:
                print("\nNo open ports found.")

    def view_results(self):
        """View previous scan results"""
        if not self.scan_results:
            print("\nNo scan results available. Run a scan first.")
            return
        
        print(f"\n=== Scan Results for {self.current_target} ===")
        print(f"Scan time: {self.scan_stats['start_time']}")
        print(f"Ports found: {len(self.open_ports)}")
        print("-" * 50)
        
        for result in self.scan_results:
            print(f"Port {result['port']}/tcp - {result['service']}")
            if result['banner'] and result['banner'] != "No banner":
                print(f"  Banner: {result['banner']}")

    def export_menu(self):
        """Export results menu"""
        if not self.scan_results:
            print("\nNo results to export. Run a scan first.")
            return
        
        print("\n=== Export Results ===")
        print("1. Export as JSON")
        print("2. Export as CSV")
        print("3. Export as Text")
        
        choice = input("Select format: ").strip()
        filename = input("Enter filename (optional): ").strip()
        
        if choice == "1":
            self.export_results('json', filename)
        elif choice == "2":
            self.export_results('csv', filename)
        elif choice == "3":
            self.export_results('txt', filename)
        else:
            print("[-] Invalid format")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='PyScanMaster - Advanced Port Scanner')
    parser.add_argument('target', nargs='?', help='Target IP or domain')
    parser.add_argument('-p', '--ports', default='1-1000', help='Port range (e.g., 1-1000)')
    parser.add_argument('-t', '--threads', type=int, default=100, help='Number of threads')
    parser.add_argument('-T', '--timeout', type=float, default=1, help='Timeout in seconds')
    parser.add_argument('-b', '--banner', action='store_true', help='Enable banner grabbing')
    parser.add_argument('-q', '--quick', action='store_true', help='Quick scan common ports')
    
    args = parser.parse_args()
    
    scanner = PyScanMaster()
    
    if args.target:
        # Command line mode
        if args.quick:
            ports = scanner.common_ports['all_common']
        else:
            if not scanner.validate_port_range(args.ports):
                print("[-] Invalid port range")
                return
            start, end = map(int, args.ports.split('-'))
            ports = range(start, end + 1)
        
        scanner.run_scan(args.target, ports, args.timeout, args.banner, args.threads)
    else:
        # Interactive mode
        scanner.main_menu()

if __name__ == "__main__":
    main()