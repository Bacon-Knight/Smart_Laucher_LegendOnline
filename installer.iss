; Inno Setup Script para BK Launcher LO v2.4.2

#define MyAppName "BK Launcher LO"
#define MyAppVersion "2.4.2"
#define MyAppPublisher "Bacon Knight Studio"
#define MyAppExeName "BKLauncherLO_v2.4.2.exe"

[Setup]
AppId={{BACON-KNIGHT-BK-LAUNCHER-LO-V242}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\BKLauncherLO
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=c:\Users\mariano\Documents\Launcher\dist
OutputBaseFilename=Setup_BKLauncherLO_v2.4.2
SetupIconFile=c:\Users\mariano\Documents\Launcher\bacon_knight.ico
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "c:\Users\mariano\Documents\Launcher\dist\BKLauncherLO_v2.4.2\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
