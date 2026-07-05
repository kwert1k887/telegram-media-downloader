@echo off
chcp 65001 > nul
echo ================================================
echo  Telegram Media Downloader - Запуск
echo ================================================
echo.

REM Проверка Python
python --version > nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден!
    echo Установите Python 3.7+ с https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python установлен
echo.

REM Создание папок
if not exist "logs" mkdir logs
if not exist "sessions" mkdir sessions
if not exist "downloads" mkdir downloads

echo [OK] Папки созданы
echo.

REM Запуск программы
echo Запуск программы...
echo.
python main.py

pause
