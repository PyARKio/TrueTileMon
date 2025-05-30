@echo off
TITLE Preparation of the environment
COLOR 0a

REM The required version of the interpreter is searched
echo Setup.bat - The required version of the interpreter is searched...
PATH | find "\Python\Python38\" > NUL
IF %ERRORLEVEL% EQU 1 (
    echo Setup.bat - The required version of the interpreter was not found
    echo Setup.bat - Run ./Setup/Download_Python_Interpreter.bat
    CALL ./Setup/Download_Python_Interpreter.bat
    TITLE Preparation of the environment)


PATH | find "\Git\" > NUL
IF %ERRORLEVEL% EQU 1 (
    echo Setup.bat - The required version of the interpreter was not found
    )

REM Deploying environment
echo Setup.bat - Deploying environment...
python ./Setup/Setup.py
COLOR 0a
pause
