; ─────────────────────────────────────────────────────────────
; Period Manager — Inno Setup installer script.
;
; Build the app first (from the project folder):
;     python build_exe.py
; That creates dist\PeriodManager\ — this script packages that
; folder into PeriodManager_Setup.exe (Windows installer).
;
; To build with Inno Setup: open this file in the Inno Setup
; Compiler (or run: iscc installer.iss) after build_exe.py has
; produced dist\PeriodManager\.
; ─────────────────────────────────────────────────────────────
#define MyAppName "Period Manager"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Muhammad Talha"
#define MyAppExeName "PeriodManager.exe"
#define MyAppFolder "PeriodManager"
; Fixed GUID for this product — keep it exactly as-is between
; versions, so an update installs over the old copy instead of
; being treated as a different app. Only change it if you ever
; want Windows to treat a future release as a separate program.
#define MyAppId "{{6E4C6E6B-9E0C-4E58-9F1B-6D2E9E9E0A11}"

[Setup]
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\{#MyAppFolder}
DefaultGroupName={#MyAppFolder}

OutputDir=Output
OutputBaseFilename={#MyAppFolder}_Setup

Compression=lzma2
SolidCompression=yes

WizardStyle=modern

PrivilegesRequired=admin

ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

DisableProgramGroupPage=yes

;SetupIconFile=logo.ico

UninstallDisplayIcon={app}\{#MyAppExeName}

[Tasks]
Name: desktopicon; Description: "Create Desktop Shortcut"; GroupDescription: "Additional Icons:";

[Files]
Source: "dist\{#MyAppFolder}\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\{#MyAppFolder}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppFolder}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppFolder}"; Flags: nowait postinstall skipifsilent
