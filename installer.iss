; Inno Setup Script para Legend Online Launcher v2.4

#define MyAppName "Legend Online Launcher"
#define MyAppVersion "2.4"
#define MyAppPublisher "Bacon Knight Studio"
#define MyAppExeName "LegendOnlineLauncher_v2.4.exe"

[Setup]
AppId={{BACON-KNIGHT-LEGEND-ONLINE-LAUNCHER-V24}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\LegendOnlineLauncher
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=c:\Users\mariano\Documents\Launcher\dist
OutputBaseFilename=Setup_LegendOnlineLauncher_v2.4
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
Source: "c:\Users\mariano\Documents\Launcher\dist\LegendOnlineLauncher_v2.4\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
