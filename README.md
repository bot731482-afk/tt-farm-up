# TikTok Farm Pro - Advanced Automation Platform

Продвинутая платформа для автоматизации TikTok с поддержкой выбора тематики контента, интеллектуальной фильтрацией видео и улучшенной логикой бота.

## 🎯 Новые Возможности

### 1. **Выбор Тематики Видео**
- Фильтрация по хэштегам (#музыка, #танцы, #комедия и т.д.)
- Поиск по ключевым словам
- Выбор категорий контента
- Чёрный список тем (исключение нежелательного контента)

### 2. **Интеллектуальная Фильтрация**
- Анализ описания видео
- Проверка популярности контента
- Фильтрация по языку
- Анализ комментариев для определения тематики

### 3. **Улучшенная Логика Бота**
- Более реалистичное поведение пользователя
- Адаптивные задержки
- Умное чередование действий
- Защита от детектирования TikTok

### 4. **Расширенный UI**
- Управление тематиками
- Настройка фильтров контента
- Статистика по темам
- Логирование действий

## 🛠️ Структура Проекта

```
tt-farm-up/
├── app/
│   ├── api/
│   │   ├── main.py
│   │   └── routes/
│   │       ├── content_filtering.py
│   │       ├── themes.py
│   │       └── advanced_settings.py
│   ├── automation/
│   │   ├── services.py
│   │   ├── content_analyzer.py
│   │   ├── behavior_simulator.py
│   │   └── theme_filter.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── models/
│   │   └── __init__.py
│   ├── services/
│   │   ├── content_service.py
│   │   └── behavior_service.py
│   └── ui/
│       ├── main.py
│       └── pages/
│           ├── devices.py
│           ├── accounts.py
│           ├── proxies.py
│           ├── posts.py
│           ├── warm_schedules.py
│           ├── theme_manager.py
│           └── content_filters.py
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

## 📦 Установка

```bash
git clone https://github.com/bot731482-afk/tt-farm-up.git
cd tt-farm-up
pip install -r requirements.txt
```

## 🚀 Запуск

```bash
# Backend API
python -m app.api.main

# Frontend UI
python main.py
```

## 🔑 Ключевые Файлы

- `app/automation/theme_filter.py` - Фильтрация по тематике
- `app/automation/content_analyzer.py` - Анализ контента
- `app/automation/behavior_simulator.py` - Реалистичное поведение
- `app/ui/pages/theme_manager.py` - UI для управления темами
- `app/ui/pages/content_filters.py` - UI для фильтров

## ⚖️ Disclaimer

Этот инструмент предназначен только для образовательных целей. Использование может нарушать Terms of Service TikTok. Используйте на свой риск.
