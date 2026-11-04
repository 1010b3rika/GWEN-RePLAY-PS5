#ifndef PackageDir
  #error PackageDir must identify the verified runtime folder
#endif
#ifndef DistDir
  #error DistDir must identify the release output folder
#endif
[Setup]
AppId={{AD52D0DE-F8C4-4E6D-8AD9-4CB8401DCB81}
AppName=GWEN ▶ RePLAY™ PS5
AppVersion=0.9.0
AppPublisher=1010B3rika
AppPublisherURL=https://github.com/Tenten1824/GWEN-RePLAY-PS5
AppSupportURL=https://github.com/Tenten1824/GWEN-RePLAY-PS5/issues
AppCopyright=Copyright (C) 2026 1010B3rika
DefaultDirName={localappdata}\Programs\GWEN RePLAY PS5
DefaultGroupName=GWEN ▶ RePLAY™ PS5
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
OutputDir={#DistDir}
OutputBaseFilename=GWEN-RePLAY-PS5-Setup
SetupIconFile={#PackageDir}\assets\gwen.ico
UninstallDisplayIcon={app}\GWEN ▶ RePLAY™ PS5.exe
LicenseFile={#PackageDir}\LICENSE
InfoBeforeFile={#PackageDir}\CREDITS.txt
WizardStyle=modern
Compression=lzma2/fast
SolidCompression=yes
[Tasks]
Name: desktopicon; Description: "Create a desktop shortcut"; Flags: unchecked
[Files]
Source: "{#PackageDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
[Icons]
Name: "{group}\GWEN ▶ RePLAY™ PS5"; Filename: "{app}\GWEN ▶ RePLAY™ PS5.exe"
Name: "{autodesktop}\GWEN ▶ RePLAY™ PS5"; Filename: "{app}\GWEN ▶ RePLAY™ PS5.exe"; Tasks: desktopicon
[Run]
Filename: "{app}\GWEN ▶ RePLAY™ PS5.exe"; Description: "Open GWEN ▶ RePLAY™ PS5"; Flags: nowait postinstall skipifsilent

