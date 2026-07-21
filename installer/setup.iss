#define MyAppName "ObserveX Agent"
#define MyAppVersion "1.0"
#define MyAppPublisher "ObserveX"

[Setup]

AppId={{5eb20438-9b8e-466c-a19d-f865113dc893}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf32}\ObserveXAgent
DefaultGroupName=ObserveX Agent

OutputDir=.
OutputBaseFilename=ObserveX_Setup

Compression=lzma
SolidCompression=yes

PrivilegesRequired=admin
WizardStyle=modern


[Languages]

Name: "english"; MessagesFile: "compiler:Default.isl"


[Tasks]

Name: desktopicon; Description: "Create Desktop Shortcut"


[Dirs]

Name: "{app}\logs"



; ============================================================
; FILES
; ============================================================

[Files]


; Main Agent

Source: "..\main\*"; DestDir: "{app}\main"; Flags: recursesubdirs createallsubdirs


; Windows Service

Source: "..\service\*"; DestDir: "{app}\service"; Flags: recursesubdirs createallsubdirs


; Storage

Source: "..\storage\*"; DestDir: "{app}\storage"; Flags: recursesubdirs createallsubdirs



; Launchers

Source: "..\launcher.exe"; DestDir: "{app}"


Source: "..\extension_loader.exe"; DestDir: "{app}"


Source: "..\registration.exe"; DestDir: "{app}"



; Extensions

Source: "..\extensions\*"; DestDir: "{app}\extensions"; Flags: recursesubdirs createallsubdirs





; ============================================================
; REGISTRY
; ============================================================

[Registry]


; Chrome

Root: HKLM; Subkey: "Software\Google\Chrome\NativeMessagingHosts\com.observex.host"; ValueType: string; ValueName: ""; ValueData: "{app}\extensions\native_host\native_host.json"; Flags: uninsdeletekey


Root: HKLM; Subkey: "Software\WOW6432Node\Google\Chrome\NativeMessagingHosts\com.observex.host"; ValueType: string; ValueName: ""; ValueData: "{app}\extensions\native_host\native_host.json"; Flags: uninsdeletekey

; Edge

Root: HKLM; Subkey: "Software\Microsoft\Edge\NativeMessagingHosts\com.observex.host"; ValueType: string; ValueName: ""; ValueData: "{app}\extensions\native_host\native_host_edge.json"; Flags: uninsdeletekey





; ============================================================
; CREATE NATIVE HOST MANIFEST
; ============================================================

[Code]


procedure WriteManifest(FileName: String);

var
  HostPath: String;
  S: String;

begin


  HostPath :=
    ExpandConstant('{app}\extensions\native_host\host.exe');


  ; 

  StringChangeEx(
    HostPath,
    '\',
    '\\',
    True
  );


  S :=
'{'+#13#10+
'  "name":"com.observex.host",'+#13#10+
'  "description":"ObserveX Native Host",'+#13#10+
'  "path":"'+HostPath+'",'+#13#10+
'  "type":"stdio",'+#13#10+
'  "allowed_origins":['+
'"chrome-extension://ojneolimjkjhajnklkobfpaedldahgmk/"'+
']'+#13#10+
'}';



  SaveStringToFile(
    FileName,
    S,
    False
  );


end;





procedure CurStepChanged(
  CurStep: TSetupStep
);

begin


 if CurStep = ssPostInstall then

 begin


   WriteManifest(
     ExpandConstant(
       '{app}\extensions\native_host\native_host.json'
     )
   );



   WriteManifest(
     ExpandConstant(
       '{app}\extensions\native_host\native_host_edge.json'
     )
   );


 end;


end;








[Icons]


Name: "{group}\ObserveX Agent"; Filename: "{app}\launcher.exe"



Name: "{autodesktop}\ObserveX Agent"; Filename: "{app}\launcher.exe"; Tasks: desktopicon







; ============================================================
; INSTALL ACTIONS
; ============================================================

[Run]


Filename: "{app}\registration.exe"; Flags: runhidden waituntilterminated

Filename: "{app}\extension_loader.exe"; Flags: runhidden waituntilterminated



; Install service

Filename: "{app}\service\service.exe"; Parameters: "install"; Flags: runhidden waituntilterminated



; Auto start service

Filename: "sc.exe"; Parameters: "config ObserveXAgent start= auto"; Flags: runhidden waituntilterminated



; Start service

Filename: "{app}\service\service.exe"; Parameters:"start"; Flags: runhidden waituntilterminated







; ============================================================
; UNINSTALL
; ============================================================

[UninstallRun]


Filename: "{app}\service\service.exe"; Parameters: "stop"; Flags: runhidden waituntilterminated



Filename: "{app}\service\service.exe"; Parameters: "remove"; Flags: runhidden waituntilterminated






[UninstallDelete]


Type: filesandordirs; Name: "{app}\logs"