@echo off

:LOOP
python sdl\sdl.py
FOR /F "delims=" %%i IN ('type system_logs\%log_filename% ^| findstr /C:"Finished Successfully"') DO SET LastLine=%%i
if "%LastLine%"=="Finished Successfully" (
    echo Script terminated by user.
    set /p choice="Are you sure you want to stop logging data? (Yes/No): " default=[No]
    if /I "%choice%"=="Yes" goto :END
) else (
    echo Unexpected termination. Restarting...
)

goto LOOP

:END
echo Stopping...
