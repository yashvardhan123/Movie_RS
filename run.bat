@echo off

REM "C:\Users\hp\AppData\Local\Programs\Python\Python38-32\python.exe"
cd "C:\Users\hp\Desktop\Movie Project\myvenv\Scripts"
start activate.bat
timeout /t 2 /nobreak
start http://localhost:5000/
REM SET /P _inputname= go to localhost(y/n)?:
REM IF "%_inputname%"=="y" GOTO :yes
REM ECHO exitting.....
REM GOTO :end
REM :yes
REM start http://localhost:5000/
REM :end
