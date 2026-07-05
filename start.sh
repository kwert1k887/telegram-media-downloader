#!/bin/bash

echo "================================================"
echo " Telegram Media Downloader - Запуск"
echo "================================================"
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "[ОШИБКА] Python3 не найден!"
    echo "Установите Python 3.7+ с https://www.python.org/downloads/"
    exit 1
fi

echo "[OK] Python установлен"
echo ""

# Создание папок
mkdir -p logs
mkdir -p sessions
mkdir -p downloads

echo "[OK] Папки созданы"
echo ""

# Запуск программы
echo "Запуск программы..."
echo ""
python3 main.py
