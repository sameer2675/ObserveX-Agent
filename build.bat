@echo off
setlocal enabledelayedexpansion

rem ============================================================
rem ObserveX Agent - build all executables with PyInstaller
rem Run this from the observex_agent project root (same folder
rem as main.py, service.py, registration.py, launcher.py).
rem ============================================================

goto :main

rem ------------------------------------------------------------
rem :movedir <src> <dst>
rem robocopy-based move with built-in retry: handles the brief
rem file lock that Windows Defender / OneDrive / indexers can
rem put on a freshly-written EXE right after PyInstaller closes it.
rem ------------------------------------------------------------
:movedir
robocopy "%~1" "%~2" /E /MOVE /R:5 /W:2 /NFL /NDL /NJH /NJS >nul
if errorlevel 8 exit /b 1
exit /b 0

rem ------------------------------------------------------------
rem :movefile <src> <dst>
rem ------------------------------------------------------------
:movefile
set _mf_tries=0
:movefile_retry
move /y "%~1" "%~2" >nul 2>&1
if exist "%~2" exit /b 0
set /a _mf_tries+=1
if %_mf_tries% geq 5 exit /b 1
timeout /t 2 /nobreak >nul
goto :movefile_retry

:main

set ROOT=%~dp0
cd /d "%ROOT%"

echo ==== Stopping any running agent/service so files aren't locked ====
net stop ObserveXAgent >nul 2>&1
taskkill /f /im main.exe >nul 2>&1
taskkill /f /im service.exe >nul 2>&1
taskkill /f /im launcher.exe >nul 2>&1
taskkill /f /im host.exe >nul 2>&1

echo ==== Installing/checking dependencies ====
pip install -r requirements.txt
pip install pyinstaller
if errorlevel 1 goto :error

echo ==== Cleaning previous builds ====
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q *.spec 2>nul
rmdir /s /q extensions\native_host\build 2>nul
rmdir /s /q extensions\native_host\dist 2>nul
rmdir /s /q installer\build 2>nul
rmdir /s /q installer\dist 2>nul
rmdir /s /q main 2>nul
if exist main (
    echo ERROR: could not remove old "main\" folder - a file inside it is likely locked ^(is ObserveXAgent service or main.exe still running?^)
    goto :error
)
rmdir /s /q service 2>nul
if exist service (
    echo ERROR: could not remove old "service\" folder - a file inside it is likely locked
    goto :error
)

rem ------------------------------------------------------------
rem main.exe (onedir) - the tracking agent itself
rem ------------------------------------------------------------
echo ==== Building main.exe ====
python -m PyInstaller --noconfirm --onedir --console --name main main.py
if errorlevel 1 goto :error
if not exist dist\main\main.exe (
    echo ERROR: PyInstaller reported success but dist\main\main.exe is missing
    goto :error
)
call :movedir dist\main main
if not exist main\main.exe (
    echo ERROR: move dist\main -^> main failed ^(main\main.exe not found after move^)
    goto :error
)

rem ------------------------------------------------------------
rem service.exe (onedir) - Windows Service wrapper that launches
rem main.exe inside the logged-on user's session
rem ------------------------------------------------------------
echo ==== Building service.exe ====
python -m PyInstaller --noconfirm --onedir --console --name service ^
    --hidden-import win32timezone ^
    --hidden-import win32event ^
    --hidden-import win32service ^
    --hidden-import win32serviceutil ^
    --hidden-import servicemanager ^
    --hidden-import win32ts ^
    --hidden-import win32profile ^
    --hidden-import win32security ^
    --hidden-import win32process ^
    --hidden-import win32con ^
    --hidden-import pywintypes ^
    service.py
if errorlevel 1 goto :error
if not exist dist\service\service.exe (
    echo ERROR: PyInstaller reported success but dist\service\service.exe is missing
    goto :error
)
call :movedir dist\service service
if not exist service\service.exe (
    echo ERROR: move dist\service -^> service failed ^(service\service.exe not found after move^)
    goto :error
)

rem ------------------------------------------------------------
rem registration.exe (onefile) - runs once at install to
rem register the device with the server
rem ------------------------------------------------------------
echo ==== Building registration.exe ====
python -m PyInstaller --noconfirm --onefile --console --name registration registration.py
if errorlevel 1 goto :error
call :movefile dist\registration.exe registration.exe
if not exist registration.exe (
    echo ERROR: move dist\registration.exe failed
    goto :error
)

rem ------------------------------------------------------------
rem extension_loader.exe (onefile, windowed) - small GUI to
rem walk the user through installing the browser extension
rem ------------------------------------------------------------
echo ==== Building extension_loader.exe ====
python -m PyInstaller --noconfirm --onefile --windowed --name extension_loader ^
    --hidden-import customtkinter ^
    extension_loader.py
if errorlevel 1 goto :error
call :movefile dist\extension_loader.exe extension_loader.exe
if not exist extension_loader.exe (
    echo ERROR: move dist\extension_loader.exe failed
    goto :error
)

rem ------------------------------------------------------------
rem launcher.exe (onefile) - shortcut target, launches the
rem service/agent if not already registered
rem ------------------------------------------------------------
echo ==== Building launcher.exe ====
python -m PyInstaller --noconfirm --onefile --console --name launcher launcher.py
if errorlevel 1 goto :error
call :movefile dist\launcher.exe launcher.exe
if not exist launcher.exe (
    echo ERROR: move dist\launcher.exe failed
    goto :error
)

rem ------------------------------------------------------------
rem host.exe (onefile) - native messaging host used by the
rem Chrome/Edge extension
rem ------------------------------------------------------------
echo ==== Building host.exe ====
pushd extensions\native_host
python -m PyInstaller --noconfirm --onefile --console --name host host.py
if errorlevel 1 (popd & goto :error)
call :movefile dist\host.exe host.exe
if not exist host.exe (
    echo ERROR: move dist\host.exe failed
    popd
    goto :error
)
popd

echo ==== Cleaning intermediate build folders ====
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q *.spec 2>nul
rmdir /s /q extensions\native_host\build 2>nul
rmdir /s /q extensions\native_host\dist 2>nul
del /q extensions\native_host\*.spec 2>nul

echo ==== Verifying build outputs ====
if not exist main\main.exe (echo ERROR: main\main.exe missing & goto :error)
if not exist service\service.exe (echo ERROR: service\service.exe missing & goto :error)
if not exist registration.exe (echo ERROR: registration.exe missing & goto :error)
if not exist extension_loader.exe (echo ERROR: extension_loader.exe missing & goto :error)
if not exist launcher.exe (echo ERROR: launcher.exe missing & goto :error)
if not exist extensions\native_host\host.exe (echo ERROR: extensions\native_host\host.exe missing & goto :error)

echo.
echo ==== BUILD COMPLETE - all outputs verified on disk ====
echo   main\main.exe
echo   service\service.exe
echo   registration.exe
echo   extension_loader.exe
echo   launcher.exe
echo   extensions\native_host\host.exe
echo.
echo Next: run installer\setup.iss with Inno Setup to build ObserveX_Setup.exe
goto :eof

:error
echo.
echo ==== BUILD FAILED ====
exit /b 1