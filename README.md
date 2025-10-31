# Custom Authentication & Authorization System

Система аутентификации и авторизации на Django REST Framework с собственной реализацией управления доступом на основе ролей (RBAC).

## 🚀 Особенности

- **Кастомная аутентификация** - собственная реализация на основе сессионных токенов
- **RBAC (Role-Based Access Control)** - гибкая система управления правами доступа
- **Мягкое удаление пользователей** - деактивация аккаунта вместо физического удаления
- **REST API** - полный набор эндпоинтов для управления системой
- **PostgreSQL** - надежное хранение данных
- **DRF** - современный API фреймворк

## 🛠 Технологии

- Python 3.9+
- Django 4.2.7
- Django REST Framework 3.14.0
- PostgreSQL 13+
- psycopg2-binary 2.9.7

## 📦 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd auth_system
```

### 2. Создание виртуального окружения
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка окружения
```bash
cp .env.example .env
# Отредактируйте .env файл под вашу конфигурацию
```

### 5. Настройка базы данных
Убедитесь, что PostgreSQL запущен и создайте базу данных `auth_system`.

### 6. Миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Создание тестовых данных
```bash
python manage.py create_test_data
```

### 8. Запуск сервера
```bash
python manage.py runserver
```

Сервер будет доступен по адресу: `http://localhost:8000`

## 🔐 Тестовые пользователи

После выполнения `create_test_data` создаются:

- **Администратор**: `admin@example.com` / `admin123`
- **Обычный пользователь**: `user@example.com` / `user123`

## 📡 API Endpoints

### Аутентификация
- `POST /api/auth/register/` - Регистрация нового пользователя
- `POST /api/auth/login/` - Вход в систему
- `POST /api/auth/logout/` - Выход из системы
- `GET /api/auth/profile/` - Получение профиля
- `PUT /api/auth/profile/` - Обновление профиля
- `DELETE /api/auth/delete_account/` - Удаление аккаунта

### Бизнес-логика
- `GET /api/projects/` - Список проектов
- `POST /api/projects/` - Создание проекта
- `GET /api/tasks/` - Список задач
- `POST /api/tasks/` - Создание задачи

### Администрирование (только для суперпользователей)
- `GET /api/admin/roles/` - Список ролей
- `POST /api/admin/roles/` - Создание роли
- `GET /api/admin/resources/` - Список ресурсов
- `GET /api/admin/permissions/` - Список разрешений

## 🗄 Структура базы данных

### Основные модели

#### User
- `email` - уникальный email пользователя
- `password_hash` - хэш пароля
- `first_name`, `last_name`, `patronymic` - личные данные
- `is_active` - активен ли пользователь
- `is_superuser` - является ли суперпользователем
- `created_at`, `updated_at`, `last_login` - временные метки

#### Role
- `name` - название роли
- `description` - описание роли

#### Resource
- `name` - название ресурса (эндпоинта)
- `method` - HTTP метод (GET, POST, PUT, DELETE, PATCH)
- Уникальность по комбинации `name` + `method`

#### Permission
- Связывает роли с ресурсами
- `can_access` - разрешен ли доступ

#### SessionToken
- `token` - уникальный токен сессии
- `user` - связь с пользователем
- `expires_at` - время истечения токена
- `is_active` - активен ли токен

### ER-model

<img width="976" height="746" alt="er" src="https://github.com/user-attachments/assets/cacbfcab-ec14-49d3-a470-353ec6a1b359" />


## 🔒 Система прав доступа

### Концепция
1. **Пользователи** могут иметь несколько **ролей**
2. **Роли** имеют **разрешения** на доступ к **ресурсам**
3. **Ресурсы** представляют эндпоинты API и HTTP методы

### Иерархия доступа
1. Суперпользователь (`is_superuser=True`) имеет доступ ко всем ресурсам
2. Пользователь получает доступ, если хотя бы одна из его ролей имеет разрешение на ресурс
3. Если у пользователя нет ролей с доступом к ресурсу - возвращается 403

### Примеры ролей
- **admin** - полный доступ ко всем ресурсам
- **user** - базовый доступ на чтение и создание

## 🧪 Тестирование с Postman

### 1. Регистрация пользователя
```http
POST http://localhost:8000/api/auth/register/
Content-Type: application/json

{
    "email": "newuser@example.com",
    "password": "password123",
    "password_repeat": "password123",
    "first_name": "New",
    "last_name": "User"
}
```

### 2. Вход в систему
```http
POST http://localhost:8000/api/auth/login/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "user123"
}
```

Сохраните полученный токен для последующих запросов.

### 3. Доступ к защищенным ресурсам
```http
GET http://localhost:8000/api/projects/
Authorization: Bearer <your_token>
```


## 🚨 Обработка ошибок

- **401 Unauthorized** - Неверный или отсутствующий токен аутентификации
- **403 Forbidden** - У пользователя нет прав доступа к ресурсу
- **404 Not Found** - Ресурс не найден
- **400 Bad Request** - Неверные данные запроса

## 📄 Лицензия

Этот проект создан в учебных целях.
