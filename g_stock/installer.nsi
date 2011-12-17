Name "Suivi de stock GSTOCK"

;SetCompress off

; installer file name
OutFile "Install-gstock.exe"

; default destination dir
InstallDir "C:\Gstock"

; request application privilege
; user should be ok. one can still right-click to install as admin
RequestExecutionLevel user

Page directory
Page instfiles

Section ""

  ; destination folder
  SetOutPath $INSTDIR

  ; List of files/folders to copy
  File /r dist\*.*
  File /r *.dll
  File /r *.manifest
  File /r images
  File /r locale
  File /r utils

  ; start menu entry
  CreateDirectory "$SMPROGRAMS\GSTOCK"
  CreateShortCut "$SMPROGRAMS\GSTOCK\Suivi gstock.lnk" "$INSTDIR\gstock.exe" "" "$INSTDIR\gstock.exe" 0
  createShortCut "$SMPROGRAMS\GSTOCK\Uninstall Suivi gstock.lnk" "$INSTDIR\uninstaller.exe"


  ; uninstaller
  writeUninstaller $INSTDIR\uninstaller.exe

SectionEnd

section "Uninstall"

# Always delete uninstaller first
delete $INSTDIR\uninstaller.exe

RMDir /r $SMPROGRAMS\GSTOCK

# now delete installed file
delete $INSTDIR\*.exe
delete $INSTDIR\*.dll
delete $INSTDIR\*.manifest
delete $INSTDIR\*.exe
delete $INSTDIR\*.lib
delete $INSTDIR\*.zip
RMDir /r $INSTDIR\images
;~ RMDir /r $INSTDIR\locale

sectionEnd

