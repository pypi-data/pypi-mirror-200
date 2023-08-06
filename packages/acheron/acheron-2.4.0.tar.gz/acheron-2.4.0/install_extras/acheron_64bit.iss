[Setup]
AppName = Acheron
AppID = Suprock Tech Acheron
AppVersion = {#VERSION}
AppVerName = Acheron {#VERSION}
AppPublisher = Suprock Tech
AppPublisherURL = https://suprocktech.com/
CloseApplications = force
DefaultDirName = {autopf}\Acheron
DefaultGroupName = Acheron
DisableProgramGroupPage = yes
Compression = lzma2
SolidCompression = yes
OutputBaseFilename = Acheron 64-bit Setup
WizardSmallImageFile = acheron.bmp
SetupIconFile = acheron.ico

; Windows 7 with Service Pack 1
MinVersion = 6.1sp1

; 64-bit
ArchitecturesInstallIn64BitMode = x64
ArchitecturesAllowed = x64

; This installation requires admin priviledges. This is needed to install
; drivers on windows vista and later.
PrivilegesRequired = admin

[InstallDelete]
; Remove library files from the last installation; this is the easiest way to allow deletions
Type: filesandordirs; Name: "{app}\botodata"
Type: filesandordirs; Name: "{app}\imageformats"
Type: filesandordirs; Name: "{app}\lib"
Type: filesandordirs; Name: "{app}\platforms"
Type: filesandordirs; Name: "{app}\styles"

; Remove the old style start menu group in favor of the new top level shortcut
Type: filesandordirs; Name: "{group}"

[Files]
Source: "*"; DestDir: "{app}"; Excludes: "\*.iss,\*.ico,\*.bmp,\Output,lib\hyperborea\7zip_*,lib\asphodel\lib*"; Flags: recursesubdirs ignoreversion
Source: "acheron.exe"; DestDir: "{app}"; DestName: "acheron-device.exe"; Flags: ignoreversion
Source: "acheron.exe"; DestDir: "{app}"; DestName: "acheron-calc.exe"; Flags: ignoreversion
Source: "lib\hyperborea\7zip_64bit\*"; DestDir: "{app}\lib\hyperborea\7zip_64bit"; Flags: ignoreversion
Source: "lib\asphodel\lib64\*.dll"; DestDir: "{app}\lib\asphodel\lib64"; Flags: ignoreversion

[Run]
Filename: "{app}\acheron.exe"; Description: "Launch Acheron"; Flags: postinstall nowait

[Icons]
Name: "{commonprograms}\Acheron"; Filename: "{app}\acheron.exe";

[Code]
(* This deletes the installer if run with /DeleteInstaller=Yes *)
procedure CurStepChanged(CurStep: TSetupStep);
var
  strContent: String;
  intErrorCode: Integer;
  strSelf_Delete_BAT: String;
begin
  if CurStep=ssDone then
  begin
    if ExpandConstant('{param:DeleteInstaller|No}') = 'Yes' then
    begin
      strContent := ':try_delete' + #13 + #10 +
            'del "' + ExpandConstant('{srcexe}') + '"' + #13 + #10 +
            'if exist "' + ExpandConstant('{srcexe}') + '" goto try_delete' + #13 + #10 +
            'del %0';
  
      strSelf_Delete_BAT := ExtractFilePath(ExpandConstant('{tmp}')) + 'SelfDelete.bat';
      SaveStringToFile(strSelf_Delete_BAT, strContent, False);
      Exec(strSelf_Delete_BAT, '', '', SW_HIDE, ewNoWait, intErrorCode);
    end;
  end;
end;
