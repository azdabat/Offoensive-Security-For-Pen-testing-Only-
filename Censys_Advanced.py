#!/usr/bin/env python3
"""
CensysDomainFinder - Advanced Domain Discovery Tool
Author: Security Research
Version: 2.0
Description: Enhanced Censys domain discovery with multiple search techniques
"""

import sys
import json
import requests
import logging
import os
import argparse
import time
from typing import List, Set, Dict
import re
from pathlib import Path

try:
    from censys.search import CensysCertificates
    from censys.common.exceptions import CensysException, CensysAPIException
except ImportError:
    print("Error: Censys library not installed. Run: pip install censys")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('censys_domain_finder.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CensysDomainFinder:
    def __init__(self):
        self.domains_found = set()
        self.api_uid = None
        self.api_secret = None
        self.censys_client = None
        self.setup_api_credentials()
        
    def setup_api_credentials(self):
        """Setup Censys API credentials from environment or user input"""
        self.api_uid = os.environ.get("CENSYS_API_ID") or os.environ.get("CENSYS_UID") or os.environ.get("CENSYS_ID")
        self.api_secret = os.environ.get("CENSYS_API_SECRET") or os.environ.get("CENSYS_SECRET")
        
        if not self.api_uid or not self.api_secret:
            logger.warning("Censys API credentials not found in environment variables")
            logger.info("Please set CENSYS_API_ID and CENSYS_API_SECRET environment variables")
            logger.info("You can get them from: https://search.censys.io/account/api")
            return False
            
        try:
            self.censys_client = CensysCertificates(api_id=self.api_uid, api_secret=self.api_secret)
            # Test the connection
            self.censys_client.metadata()
            logger.info("✅ Censys API credentials validated successfully")
            return True
        except CensysException as e:
            logger.error(f"❌ Censys API authentication failed: {e}")
            return False
    
    def display_banner(self):
        """Display tool banner"""
        banner = """
╔═══════════════════════════════════════════════╗
║           CensysDomainFinder v2.0             ║
║           Advanced Domain Discovery           ║
║                                               ║
║         Get API Keys: search.censys.io        ║
╚═══════════════════════════════════════════════╝
        """
        print(banner)
    
    def validate_domain(self, domain: str) -> bool:
        """Validate domain format"""
        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$'
        return re.match(domain_pattern, domain) is not None
    
    def extract_base_domain(self, domain: str) -> str:
        """Extract base domain for subdomain matching"""
        parts = domain.split('.')
        if len(parts) >= 2:
            return '.'.join(parts[-2:])
        return domain
    
    def is_relevant_domain(self, candidate: str, target_domain: str) -> bool:
        """
        Check if candidate domain is relevant to target domain
        Returns True for:
        - Exact match
        - Subdomains of target
        - Domains sharing the same base domain
        """
        candidate = candidate.lower().strip()
        target = target_domain.lower().strip()
        
        # Exact match
        if candidate == target:
            return True
            
        # Subdomain of target
        if candidate.endswith('.' + target):
            return True
            
        # Same base domain (e.g., example.com and sub.example.com)
        base_target = self.extract_base_domain(target)
        base_candidate = self.extract_base_domain(candidate)
        
        return base_candidate == base_target
    
    def search_certificates_by_domain(self, domain: str, max_results: int = 100) -> Set[str]:
        """Search for domains using certificate transparency logs"""
        logger.info(f"🔍 Searching certificates for: {domain}")
        domains_found = set()
        
        try:
            # Search for certificates containing the domain
            query = f"parsed.names: {domain}"
            
            for page in self.censys_client.search(query, fields=["parsed.names"], max_records=max_results):
                for certificate in page:
                    if "parsed.names" in certificate:
                        for name in certificate["parsed.names"]:
                            if self.is_relevant_domain(name, domain):
                                domains_found.add(name)
                                logger.debug(f"Found domain: {name}")
            
            logger.info(f"✅ Found {len(domains_found)} unique domains from certificates")
            return domains_found
            
        except CensysAPIException as e:
            if "rate limit" in str(e).lower():
                logger.warning("⚠️ Rate limit hit, waiting 60 seconds...")
                time.sleep(60)
                return self.search_certificates_by_domain(domain, max_results)
            else:
                logger.error(f"❌ Censys API error: {e}")
                return set()
        except Exception as e:
            logger.error(f"❌ Unexpected error during certificate search: {e}")
            return set()
    
    def search_by_organization(self, org_name: str, max_results: int = 50) -> Set[str]:
        """Search for domains by organization name"""
        logger.info(f"🔍 Searching for organization: {org_name}")
        domains_found = set()
        
        try:
            query = f"parsed.subject.organization: \"{org_name}\""
            
            for page in self.censys_client.search(query, fields=["parsed.names"], max_records=max_results):
                for certificate in page:
                    if "parsed.names" in certificate:
                        for name in certificate["parsed.names"]:
                            # Filter out wildcard certificates and invalid domains
                            if '*' not in name and self.validate_domain(name):
                                domains_found.add(name)
            
            logger.info(f"✅ Found {len(domains_found)} domains for organization: {org_name}")
            return domains_found
            
        except Exception as e:
            logger.error(f"❌ Error searching by organization: {e}")
            return set()
    
    def search_by_ssl_hash(self, ssl_hash: str) -> Set[str]:
        """Search for domains by SSL certificate hash"""
        logger.info(f"🔍 Searching for SSL hash: {ssl_hash}")
        domains_found = set()
        
        try:
            certificate = self.censys_client.view(ssl_hash)
            if "parsed.names" in certificate:
                for name in certificate["parsed.names"]:
                    if self.validate_domain(name):
                        domains_found.add(name)
            
            logger.info(f"✅ Found {len(domains_found)} domains for SSL hash")
            return domains_found
            
        except Exception as e:
            logger.error(f"❌ Error searching by SSL hash: {e}")
            return set()
    
    def export_results(self, domains: Set[str], filename: str = None, format_type: str = "txt"):
        """Export results to file"""
        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"censys_domains_{timestamp}.{format_type}"
        
        try:
            domains_list = sorted(list(domains))
            
            if format_type == "txt":
                with open(filename, 'w', encoding='utf-8') as f:
                    for domain in domains_list:
                        f.write(domain + '\n')
            
            elif format_type == "json":
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump({"domains": domains_list, "count": len(domains_list)}, f, indent=2)
            
            elif format_type == "csv":
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("Domain\n")
                    for domain in domains_list:
                        f.write(f"{domain}\n")
            
            logger.info(f"💾 Results exported to: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error exporting results: {e}")
            return False
    
    def display_results(self, domains: Set[str], title: str = "Discovered Domains"):
        """Display results in a formatted way"""
        if not domains:
            print("❌ No domains found.")
            return
        
        domains_list = sorted(list(domains))
        
        print(f"\n{'='*60}")
        print(f"📊 {title}")
        print(f"{'='*60}")
        print(f"Total Domains Found: {len(domains_list)}")
        print(f"{'-'*60}")
        
        for i, domain in enumerate(domains_list, 1):
            print(f"{i:3d}. {domain}")
        
        print(f"{'='*60}")
    
    def interactive_menu(self):
        """Interactive menu system"""
        while True:
            self.display_banner()
            print("Main Menu:")
            print("1. 🔍 Domain Search (Certificate Transparency)")
            print("2. 🏢 Organization Search")
            print("3. 🔐 SSL Hash Search") 
            print("4. 📊 View Previous Results")
            print("5. 💾 Export Results")
            print("6. ⚙️ API Configuration")
            print("0. 🚪 Exit")
            
            choice = input("\nSelect option [0-6]: ").strip()
            
            if choice == "1":
                self.domain_search_menu()
            elif choice == "2":
                self.organization_search_menu()
            elif choice == "3":
                self.ssl_hash_search_menu()
            elif choice == "4":
                self.view_results_menu()
            elif choice == "5":
                self.export_menu()
            elif choice == "6":
                self.api_config_menu()
            elif choice == "0":
                print("👋 Thank you for using CensysDomainFinder!")
                break
            else:
                print("❌ Invalid option. Please try again.")
            
            input("\nPress Enter to continue...")
    
    def domain_search_menu(self):
        """Domain search submenu"""
        print("\n🔍 Domain Search Options:")
        print("1. Quick Search (100 results)")
        print("2. Comprehensive Search (500 results)")
        print("3. Custom Search")
        print("4. Back to Main Menu")
        
        choice = input("\nSelect option [1-4]: ").strip()
        
        if choice == "1":
            max_results = 100
        elif choice == "2":
            max_results = 500
        elif choice == "3":
            try:
                max_results = int(input("Enter max results [100-1000]: ") or "100")
                max_results = max(100, min(1000, max_results))
            except ValueError:
                print("❌ Invalid number. Using default 100 results.")
                max_results = 100
        elif choice == "4":
            return
        else:
            print("❌ Invalid option.")
            return
        
        domain = input("\nEnter domain to search (e.g., example.com): ").strip()
        if not domain:
            print("❌ No domain provided.")
            return
        
        if not self.validate_domain(domain):
            print("❌ Invalid domain format.")
            return
        
        if not self.censys_client:
            print("❌ Censys API not configured. Please check API credentials.")
            return
        
        print(f"\n🚀 Starting search for: {domain}")
        print("This may take a few moments...")
        
        domains = self.search_certificates_by_domain(domain, max_results)
        self.domains_found.update(domains)
        self.display_results(domains, f"Domains related to {domain}")
    
    def organization_search_menu(self):
        """Organization search submenu"""
        org_name = input("\nEnter organization name: ").strip()
        if not org_name:
            print("❌ No organization name provided.")
            return
        
        if not self.censys_client:
            print("❌ Censys API not configured.")
            return
        
        print(f"\n🔍 Searching for organization: {org_name}")
        domains = self.search_by_organization(org_name)
        self.domains_found.update(domains)
        self.display_results(domains, f"Domains for {org_name}")
    
    def ssl_hash_search_menu(self):
        """SSL hash search submenu"""
        ssl_hash = input("\nEnter SSL certificate hash: ").strip()
        if not ssl_hash:
            print("❌ No SSL hash provided.")
            return
        
        if not self.censys_client:
            print("❌ Censys API not configured.")
            return
        
        print(f"\n🔍 Searching for SSL hash: {ssl_hash}")
        domains = self.search_by_ssl_hash(ssl_hash)
        self.domains_found.update(domains)
        self.display_results(domains, f"Domains for SSL hash {ssl_hash}")
    
    def view_results_menu(self):
        """View previous results"""
        if not self.domains_found:
            print("❌ No results to display. Run a search first.")
            return
        
        self.display_results(self.domains_found, "All Discovered Domains")
    
    def export_menu(self):
        """Export results submenu"""
        if not self.domains_found:
            print("❌ No results to export. Run a search first.")
            return
        
        print("\n💾 Export Options:")
        print("1. Export as Text File")
        print("2. Export as JSON")
        print("3. Export as CSV")
        print("4. Back to Main Menu")
        
        choice = input("\nSelect format [1-4]: ").strip()
        
        if choice == "1":
            format_type = "txt"
        elif choice == "2":
            format_type = "json"
        elif choice == "3":
            format_type = "csv"
        elif choice == "4":
            return
        else:
            print("❌ Invalid option.")
            return
        
        filename = input(f"Enter filename (optional, .{format_type}): ").strip()
        self.export_results(self.domains_found, filename, format_type)
    
    def api_config_menu(self):
        """API configuration menu"""
        print(f"\n⚙️ Current API Configuration:")
        print(f"API ID: {'✅ Set' if self.api_uid else '❌ Not set'}")
        print(f"API Secret: {'✅ Set' if self.api_secret else '❌ Not set'}")
        
        print("\nOptions:")
        print("1. Test API Connection")
        print("2. View API Setup Instructions")
        print("3. Back to Main Menu")
        
        choice = input("\nSelect option [1-3]: ").strip()
        
        if choice == "1":
            if self.censys_client:
                try:
                    self.censys_client.metadata()
                    print("✅ API connection successful!")
                except Exception as e:
                    print(f"❌ API connection failed: {e}")
            else:
                print("❌ API not configured.")
        
        elif choice == "2":
            self.show_api_instructions()
        
        elif choice == "3":
            return
        
        else:
            print("❌ Invalid option.")
    
    def show_api_instructions(self):
        """Display API setup instructions"""
        print("""
📋 Censys API Setup Instructions:

1. Visit: https://search.censys.io/account/api
2. Create a free account or login
3. Generate API credentials
4. Set environment variables:

   Windows (Command Prompt):
   set CENSYS_API_ID=your_api_id_here
   set CENSYS_API_SECRET=your_api_secret_here

   Windows (PowerShell):
   $env:CENSYS_API_ID="your_api_id_here"
   $env:CENSYS_API_SECRET="your_api_secret_here"

   Linux/Mac:
   export CENSYS_API_ID=your_api_id_here
   export CENSYS_API_SECRET=your_api_secret_here

5. Restart your terminal and run the tool again

💡 Tip: For permanent setup, add these to your shell profile (.bashrc, .zshrc, etc.)
        """)

def main():
    """Main function with command line support"""
    parser = argparse.ArgumentParser(description='CensysDomainFinder - Advanced Domain Discovery')
    parser.add_argument('domain', nargs='?', help='Domain to search for')
    parser.add_argument('-o', '--org', help='Organization name to search for')
    parser.add_argument('-s', '--ssl-hash', help='SSL certificate hash to search for')
    parser.add_argument('-m', '--max-results', type=int, default=100, help='Maximum results (default: 100)')
    parser.add_argument('-e', '--export', help='Export results to file')
    parser.add_argument('--format', choices=['txt', 'json', 'csv'], default='txt', help='Export format')
    
    args = parser.parse_args()
    
    finder = CensysDomainFinder()
    
    if not finder.censys_client:
        print("❌ Censys API not configured. Please set CENSYS_API_ID and CENSYS_API_SECRET environment variables.")
        print("💡 Run with --help for setup instructions.")
        sys.exit(1)
    
    # Command line mode
    if args.domain:
        domains = finder.search_certificates_by_domain(args.domain, args.max_results)
        finder.display_results(domains, f"Domains related to {args.domain}")
        
        if args.export:
            finder.export_results(domains, args.export, args.format)
    
    elif args.org:
        domains = finder.search_by_organization(args.org, args.max_results)
        finder.display_results(domains, f"Domains for organization {args.org}")
        
        if args.export:
            finder.export_results(domains, args.export, args.format)
    
    elif args.ssl_hash:
        domains = finder.search_by_ssl_hash(args.ssl_hash)
        finder.display_results(domains, f"Domains for SSL hash {args.ssl_hash}")
        
        if args.export:
            finder.export_results(domains, args.export, args.format)
    
    else:
        # Interactive mode
        finder.interactive_menu()

if __name__ == "__main__":
    main()