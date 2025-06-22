# ExamFlow Backend API

---

## 📦 Стек технологий

- Python 3.13.5
- Django 5.2.3
- Django REST Framework
- Simple JWT
- DRF-YASG
- SQLite
- Pillow
- Postman

---

## 📂 Структура приложения

- **users** — управление пользователями, аутентификация.
- **exams** — создание экзаменов и вопросов.
- **streams** — работа с потоками и результатами студентов.
- **profiles** — справочник учителя.

---

## 🔑 Авторизация

Все методы защищены через JWT.

1. Получить токен:  
`POST /api/v1/token/`

2. Получить refresh токен:  
`POST /api/v1/token/refresh/`

---

## 📖 Документация API (Swagger UI)

Доступна по адресу:  
`http://localhost:8000/swagger/`

---

## 🚀 Основные эндпоинты

### Пользователи:

- `GET /api/v1/users/profile/`
- `PUT /api/v1/users/profile/`

### Экзамены:

- `POST /api/v1/exams/` — создать экзамен вручную
- `POST /api/v1/exams/import/ai/` — импорт через AI

### Потоки:

- `POST /api/v1/streams/` — создать поток
- `POST /api/v1/streams/submit-exam/` — отправить результат

### Справочник учителя:

- `GET /api/v1/profiles/manuals/`

---

## 🐳 Запуск проекта

# Установка зависимостей
pip install -r requirements.txt

# Миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Запуск сервера
python manage.py runserver
