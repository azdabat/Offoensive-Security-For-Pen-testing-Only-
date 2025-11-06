#!/usr/bin/env python3
"""
CHRONOS-PAYLOAD: Advanced Delayed Execution Framework
Author: Red Team Research
Version: 2.1
License: MIT - For authorized testing only
"""

import os
import sys
import time
import random
import json
import base64
import hashlib
import platform
import subprocess
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import logging
from cryptography.fernet import Fernet
import getpass

class ChronosPayload:
    def __init__(self, config_dir=".chronos"):
        self.version = "2.1"
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "config.enc"
        self.log_file = self.config_dir / "activity.log"
        self.setup_logging()
        self.encryption_key = None
        self.cipher_suite = None
        self.vm_detected = self._detect_vm()
        self.setup_environment()
        
    def setup_logging(self):
        self.config_dir.mkdir(exist_ok=True)
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info(f"Chronos-Payload v{self.version} initialized")
        
    def setup_environment(self):
        key_file = self.config_dir / "key.dat"
        if key_file.exists():
            with open(key_file, 'rb') as f:
                self.encryption_key = f.read()
        else:
            self.encryption_key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(self.encryption_key)
        self.cipher_suite = Fernet(self.encryption_key)
    
    def _detect_vm(self):
        vm_indicators = 0
        vm_files = [
            "/proc/scsi/scsi",
            "/proc/ide/hda/model", 
            "C:\\Program Files\\VMware\\",
            "C:\\Program Files\\Oracle\\VirtualBox\\"
        ]
        
        for vm_file in vm_files:
            if Path(vm_file).exists():
                vm_indicators += 1
        return vm_indicators > 1
    
    def show_banner(self):
        banner = f"""
╔═══════════════════════════════════════════════╗
║            CHRONOS-PAYLOAD v{self.version}             ║
║         Advanced Delayed Execution           ║
║           For Authorized Testing Only        ║
╚═══════════════════════════════════════════════╝
        """
        print(banner)
        
    def main_menu(self):
        while True:
            self.show_banner()
            print(f"[*] System: {platform.system()} | VM: {self.vm_detected}")
            print("\n1. Deploy New Payload")
            print("2. Check Active Deployments") 
            print("3. Execute Payload Now (Test)")
            print("4. Cleanup Deployment")
            print("5. View Logs")
            print("0. Exit")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                self.deploy_menu()
            elif choice == "2":
                self.check_deployments()
            elif choice == "3":
                self.test_execution()
            elif choice == "4":
                self.cleanup_menu()
            elif choice == "5":
                self.view_logs()
            elif choice == "0":
                break
            else:
                print("[-] Invalid option")
            input("\nPress Enter to continue...")
    
    def deploy_menu(self):
        print("\nPayload Types:")
        print("1. Reconnaissance")
        print("2. Persistence")
        print("3. Lateral Movement")
        print("4. Custom Command")
        
        ptype_choice = input("\nSelect payload type (1-4): ").strip()
        payload_types = {"1": "recon", "2": "persistence", "3": "lateral", "4": "custom"}
        payload_type = payload_types.get(ptype_choice, "recon")
        
        print("\nActivation Delay:")
        print("1. Short (1-7 days)")
        print("2. Medium (1-4 weeks)") 
        print("3. Long (1-6 months)")
        print("4. Custom")
        
        delay_choice = input("Select delay (1-4): ").strip()
        if delay_choice == "4":
            delay_days = int(input("Enter days: "))
        else:
            delay_options = {"1": (1,7), "2": (7,28), "3": (30,180)}
            min_days, max_days = delay_options.get(delay_choice, (7,14))
            delay_days = random.randint(min_days, max_days)
        
        self.deploy_payload(payload_type=payload_type, delay_days=delay_days)

    def deploy_payload(self, payload_type, delay_days):
        print(f"\n[*] Deploying {payload_type} payload...")
        activation_time = datetime.now() + timedelta(days=delay_days)
        
        config = {
            'deployment_id': hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8],
            'payload_type': payload_type,
            'activation_time': activation_time.isoformat(),
            'deployment_time': datetime.now().isoformat(),
        }
        
        encrypted_config = self.encrypt_data(config)
        with open(self.config_file, 'w') as f:
            f.write(encrypted_config)
        
        print(f"[+] Payload deployed!")
        print(f"    ID: {config['deployment_id']}")
        print(f"    Activation: {activation_time.strftime('%Y-%m-%d %H:%M:%S')}")

    def encrypt_data(self, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        encrypted = self.cipher_suite.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()

    def decrypt_data(self, encrypted_data):
        try:
            encrypted = base64.b64decode(encrypted_data)
            decrypted = self.cipher_suite.decrypt(encrypted)
            return json.loads(decrypted.decode())
        except:
            return None

    def check_deployments(self):
        print("\n=== Active Deployments ===")
        if not self.config_file.exists():
            print("No active deployments")
            return
        
        with open(self.config_file, 'r') as f:
            encrypted_config = f.read()
        
        config = self.decrypt_data(encrypted_config)
        if config:
            activation_time = datetime.fromisoformat(config['activation_time'])
            time_remaining = activation_time - datetime.now()
            print(f"Deployment ID: {config['deployment_id']}")
            print(f"Activation: {activation_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Time Remaining: {time_remaining}")

    def test_execution(self):
        print("\n=== Test Execution ===")
        print("[*] This would execute the payload immediately for testing")
        # Add your test execution logic here

    def cleanup_menu(self):
        print("\n1. Remove deployment")
        print("2. Remove all artifacts")
        choice = input("Select option: ").strip()
        if choice == "1":
            self.remove_deployment()

    def remove_deployment(self):
        if self.config_file.exists():
            self.config_file.unlink()
            print("[+] Deployment removed")

    def view_logs(self):
        print("\n=== Logs ===")
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                print(f.read())

def main():
    tool = ChronosPayload()
    tool.main_menu()

if __name__ == "__main__":
    main()