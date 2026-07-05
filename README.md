# Telegram Media Downloader

Скачивание медиафайлов (фото, видео, кружки, документы, аудио) из Telegram-каналов и чатов на диск.

## Возможности

- Скачивание всех типов медиа: фото, видео, кружки, документы, аудио, стикеры, GIF
- Организация файлов по папкам источников
- Сохранение подписей к медиа в отдельные файлы
- Whitelist-фильтр по ключевым словам
- Мониторинг новых сообщений в реальном времени
- Утилита `list_chats.py` для просмотра доступных каналов

## Установка

```bash
pip install -r requirements.txt
cp config.yaml.example config.yaml
```

Получите `api_id` и `api_hash` на https://my.telegram.org

## Запуск

```bash
python main.py
```

Просмотр доступных каналов:

```bash
python list_chats.py
```

## Куда скачиваются файлы

```
downloads/
└── Название_канала/
    ├── photo_123_20250204_153000.jpg
    ├── video_124_20250204_153010.mp4
    ├── video_note_125_20250204_153020.mp4
    └── photo_123_20250204_153000_caption.txt
```

## Типы медиа

| Тип | Расширение |
|---|---|
| Фото | `.jpg` |
| Видео / Кружки | `.mp4` |
| Документы | оригинальное |
| Аудио | `.mp3` |
| Голосовые | `.ogg` |
| Стикеры | `.webp` |
| GIF | `.gif` |

## Структура

```
├── main.py                            # Точка входа
├── list_chats.py                      # Список каналов/чатов
├── config.yaml.example                # Пример конфигурации
├── requirements.txt
├── start.bat                          # Запуск (Windows)
├── start.sh                           # Запуск (Mac/Linux)
└── telegram_channel_duplicator/
    ├── client.py                      # Telegram-клиент
    ├── config_controller.py           # Загрузка конфига
    ├── duplicator_download.py         # Координатор скачивания
    ├── media_downloader.py            # Скачивание медиа
    ├── message_preparer.py            # Фильтрация
    └── source_channel.py              # Модель источника
```
