GitHub README.md
markdown
# CensysDomainFinder 🔍

**Advanced Domain Discovery Tool using Censys Certificate Transparency**

> ⚠️ **NOTE**: This tool requires Censys API credentials. Get free API keys at [search.censys.io](https://search.censys.io)

## Features

- **🔍 Multiple Search Methods**: Domain, organization, and SSL hash searches
- **📊 Interactive Menu**: User-friendly interface with guided options
- **💾 Export Results**: Multiple formats (TXT, JSON, CSV)
- **🚀 Bulk Searching**: Comprehensive domain discovery
- **⚡ Rate Limit Handling**: Automatic retry with backoff
- **📝 Logging**: Detailed operation logs for debugging

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/your-username/censys-domain-finder.git
cd censys-domain-finder

# Install dependencies
pip install censys requests
2. API Setup
bash
# Set your Censys API credentials (get from https://search.censys.io/account/api)

# Linux/Mac
export CENSYS_API_ID="your_api_id_here"
export CENSYS_API_SECRET="your_api_secret_here"

# Windows (PowerShell)
$env:CENSYS_API_ID="your_api_id_here"
$env:CENSYS_API_SECRET="your_api_secret_here"
3. Usage
Interactive Mode (Recommended)
bash
python censys_domain_finder.py
Command Line Mode
bash
# Domain search
python censys_domain_finder.py example.com

# Organization search  
python censys_domain_finder.py --org "Company Name"

# SSL hash search
python censys_domain_finder.py --ssl-hash "abc123..."

# With export
python censys_domain_finder.py example.com --export results.txt --format json
Complete Usage Guide
Step 1: Launch the Tool
bash
python censys_domain_finder.py
You'll see the main menu:

text
╔═══════════════════════════════════════════════╗
║           CensysDomainFinder v2.0             ║
║           Advanced Domain Discovery           ║
║                                               ║
║         Get API Keys: search.censys.io        ║
╚═══════════════════════════════════════════════╝

Main Menu:
1. 🔍 Domain Search (Certificate Transparency)
2. 🏢 Organization Search
3. 🔐 SSL Hash Search
4. 📊 View Previous Results
5. 💾 Export Results
6. ⚙️ API Configuration
0. 🚪 Exit

Select option [0-6]:
Step 2: Domain Search (Option 1)
2.1 Choose Search Depth
text
🔍 Domain Search Options:
1. Quick Search (100 results)
2. Comprehensive Search (500 results)  
3. Custom Search
4. Back to Main Menu

Select option [1-4]: 1
2.2 Enter Domain
text
Enter domain to search (e.g., example.com): target-company.com
2.3 View Results
text
🚀 Starting search for: target-company.com
This may take a few moments...
✅ Found 47 unique domains from certificates

============================================================
📊 Domains related to target-company.com
============================================================
Total Domains Found: 47
------------------------------------------------------------
  1. target-company.com
  2. api.target-company.com
  3. app.target-company.com
  4. auth.target-company.com
  5. blog.target-company.com
  ...
============================================================
Step 3: Organization Search (Option 2)
Use this to find all domains belonging to a specific company:

text
Enter organization name: Google LLC

🔍 Searching for organization: Google LLC
✅ Found 152 domains for organization: Google LLC
Step 4: SSL Hash Search (Option 3)
Find domains using a specific SSL certificate hash:

text
Enter SSL certificate hash: a1b2c3d4e5f6...

🔍 Searching for SSL hash: a1b2c3d4e5f6...
✅ Found 3 domains for SSL hash
Step 5: Export Results (Option 5)
text
💾 Export Options:
1. Export as Text File
2. Export as JSON  
3. Export as CSV
4. Back to Main Menu

Select format [1-4]: 2

Enter filename (optional, .json): target-company_domains.json
💾 Results exported to: target-company_domains.json
Advanced Features
Custom Search Options
Quick Search: 100 results (fast)

Comprehensive: 500 results (thorough)

Custom: Set your own limit (100-1000)

Export Formats
TXT: Simple domain list

JSON: Structured data with metadata

CSV: Spreadsheet-friendly format

Search Methods
Certificate Transparency: Find domains through SSL certificates

Organization Search: Discover all domains owned by a company

SSL Hash Lookup: Find domains using certificate fingerprints

API Setup Instructions
Getting Censys API Credentials
Visit Censys Search

Create a free account or login

Go to Account API

Generate new API credentials

Set environment variables:

bash
# Permanent setup (add to ~/.bashrc or ~/.zshrc)
export CENSYS_API_ID="your_api_id_here"
export CENSYS_API_SECRET="your_api_secret_here"

# Temporary setup (current session only)
export CENSYS_API_ID="your_api_id"
export CENSYS_API_SECRET="your_api_secret"
Testing API Connection
Use Option 6 in the menu to test your API configuration:

text
⚙️ Current API Configuration:
API ID: ✅ Set
API Secret: ✅ Set

Options:
1. Test API Connection
2. View API Setup Instructions
3. Back to Main Menu

Select option [1-3]: 1
✅ API connection successful!
Command Line Reference
bash
# Basic domain search
python censys_domain_finder.py example.com

# Organization search
python censys_domain_finder.py --org "Facebook"

# SSL hash search  
python censys_domain_finder.py --ssl-hash "sha256:abc123"

# With custom limits and export
python censys_domain_finder.py example.com --max-results 500 --export domains.json --format json

# Help
python censys_domain_finder.py --help
Troubleshooting
Common Issues
Error: Censys API authentication failed
Solution: Verify your API credentials and environment variables

Error: Rate limit exceeded
Solution: Tool automatically waits and retries. Free tier has limited requests.

Error: No domains found
Solution: Try different search terms or organization names

Error: ModuleNotFoundError: No module named 'censys'
Solution: Run pip install censys

Rate Limits
Free tier: 250 requests/month

Wait 60 seconds between bulk searches

Use comprehensive searches sparingly

Legal & Ethical Usage
✅ Authorized Activities:
Security research and reconnaissance

Bug bounty hunting (within scope)

Penetration testing (with permission)

Educational purposes

❌ Prohibited Activities:
Scanning without authorization

Malicious activities

Violating terms of service

Harassment or illegal surveillance

Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Create a Pull Request

License
MIT License - See LICENSE file for details.

Support
For issues:

Check API credentials are set correctly

Verify internet connection

Check rate limits aren't exceeded

Review the log file: censys_domain_finder.log

Remember: Always use this tool ethically and with proper authorization. Respect rate limits and terms of service.
