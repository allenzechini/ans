@echo off
set my_dir=C:\projects\Shared\src\graphlib
cd %my_dir%
for /d  /r "%my_dir%" %%a in (*) do if /i "%%~nxa"=="out" (
    echo Deleting files under %%~dpaout
    del /s /f /q %%~dpaout
    for /f %%f in ('dir /ad /b %%~dpaout') do (
        echo Removing my_dir %%~dpaout\%%f
        rd /s /q %%~dpaout\%%f
    )
)
