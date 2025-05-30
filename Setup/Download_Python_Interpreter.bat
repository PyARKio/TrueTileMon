@echo off
TITLE Download Python Interpreter
::COLOR 0a

REM Download python interpreter
echo Download_Python_Interpreter.bat - The current processor architecture is being determined...
IF %PROCESSOR_ARCHITECTURE% == AMD64 (
    echo Download_Python_Interpreter.bat - Current processor architecture is - x64
    echo Download_Python_Interpreter.bat - The interpreter python-3.8.10-amd64.exe is loading...
    curl "https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe" --output "python-3.8.10-amd64.exe"
    set path_to=python-3.8.10-amd64.exe)

IF %PROCESSOR_ARCHITECTURE% == x86 (
    echo Download_Python_Interpreter.bat - Current processor architecture is - x86
    echo Download_Python_Interpreter.bat - The interpreter python-3.8.10-x86.exe is loading...
    curl "https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe" --output "python-3.8.10-x86.exe"
    set path_to=python-3.8.10-x86.exe)

echo Download_Python_Interpreter.bat - The python installer %path_to% is running...
CALL %path_to%