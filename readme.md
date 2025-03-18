# FinancesDRF

## 📌 Описание проекта
**FinancesDRF** — это API на Django Rest Framework для управления финансами. 

### 🔥 Возможности:
- Регистрация и аутентификация через JWT
- Управление категориями трат
- CRUD-операции для транзакций
- Фильтрация и поиск

---

## 🚀 Установка и запуск

### 1️⃣ Клонирование репозитория
```sh
git clone https://github.com/yourusername/financesDRF.git
cd financesDRF
```

### 2️⃣ Создание и активация виртуального окружения
```sh
python -m venv venv
source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate  # Windows
```

### 3️⃣ Установка зависимостей
```sh
pip install -r requirements.txt
```

### 4️⃣ Применение миграций и создание суперпользователя
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5️⃣ Запуск сервера
```sh
python manage.py runserver
```
📌 **API доступен по адресу:** `http://127.0.0.1:8000/`

---

## 🔑 Аутентификация
### 📌 Получение JWT-токена
```sh
POST http://127.0.0.1:8000/api/token/
```
#### 🔹 JSON Body:
```json
{
  "username": "admin",
  "password": "yourpassword"
}
```
#### 🔹 Ответ:
```json
{
  "refresh": "your_refresh_token",
  "access": "your_access_token"
}
```
Используй `access_token` в **Postman** → вкладка `Authorization` → `Bearer Token`.

### 📌 Обновление токена
```sh
POST http://127.0.0.1:8000/api/token/refresh/
```
#### 🔹 JSON Body:
```json
{
  "refresh": "your_refresh_token"
}
```

---

## 📌 Основные API-эндпоинты

### 🔹 Получение категорий
```sh
GET http://127.0.0.1:8000/api/categories/
```
#### 🔹 Headers:
```json
Authorization: Bearer your_access_token
```
#### 🔹 Ответ:
```json
[
  { "id": 1, "name": "Еда", "user": 1 },
  { "id": 2, "name": "Транспорт", "user": 1 }
]
```

### 🔹 Создание категории
```sh
POST http://127.0.0.1:8000/api/categories/
```
#### 🔹 JSON Body:
```json
{
  "name": "Развлечения"
}
```

### 🔹 Удаление категории
```sh
DELETE http://127.0.0.1:8000/api/categories/1/
```

---

## 📌 Ошибки и их решение
| Ошибка | Причина | Решение |
|--------|---------|---------|
| `Authentication credentials were not provided.` | Не передан токен | Установи `Bearer Token` в Postman |
| `Cannot resolve keyword 'user' into field` | Поле `user` отсутствует в модели | Проверь `Category` и сделай миграции |
| `401 Unauthorized` | Истёк `access_token` | Обнови токен через `/api/token/refresh/` |

---

## 📌 Лицензия
Этот проект распространяется под лицензией **MIT**.