# YaMDb API

REST API для сервиса **YaMDb**, позволяющего пользователям публиковать отзывы на произведения, оценивать их и оставлять комментарии.

## Возможности

- регистрация пользователей с подтверждением по e-mail;
- аутентификация по JWT-токену;
- управление пользователями и ролями;
- просмотр, создание, редактирование и удаление:
  - произведений;
  - категорий;
  - жанров;
  - отзывов;
  - комментариев;
- автоматический расчёт рейтинга произведений;
- импорт данных из CSV-файлов.

## Технологии

- Python 3
- Django
- Django REST Framework
- Simple JWT
- SQLite
- django-filter

## Роли пользователей

- **Аноним** — просмотр произведений, отзывов и комментариев.
- **Пользователь** — создание и редактирование своих отзывов и комментариев.
- **Модератор** — управление любыми отзывами и комментариями.
- **Администратор** — полный доступ к проекту и управление пользователями.

## Запуск проекта

Клонируйте репозиторий:

```bash
git clone https://github.com/InnaSof/api-yamdb
cd api_yamdb
```

Создайте виртуальное окружение и активируйте его:

```bash
python -m venv venv
```

Linux/macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Примените миграции:

```bash
python manage.py migrate
```

При необходимости создайте суперпользователя:

```bash
python manage.py createsuperuser
```

Запустите сервер:

```bash
python manage.py runserver
```

Проект будет доступен по адресу:

```
http://127.0.0.1:8000/
```

Документация API:

```
http://127.0.0.1:8000/redoc/
```

## Импорт тестовых данных

Для заполнения базы данных используется CSV из директории:

```
static/data/
```

После создания моделей выполните команду импорта:

```bash
python manage.py import_csv
```

## Основные эндпоинты

| Метод | Эндпоинт | Назначение |
|-------|----------|------------|
| POST | `/api/v1/auth/signup/` | Регистрация пользователя |
| POST | `/api/v1/auth/token/` | Получение JWT-токена |
| GET, POST | `/api/v1/categories/` | Категории |
| GET, POST | `/api/v1/genres/` | Жанры |
| GET, POST | `/api/v1/titles/` | Произведения |
| GET, POST | `/api/v1/titles/{title_id}/reviews/` | Отзывы |
| GET, POST | `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` | Комментарии |
| GET, PATCH | `/api/v1/users/me/` | Профиль текущего пользователя |

Полное описание всех эндпоинтов доступно в ReDoc.

## Авторы

Проект выполнен в рамках командной разработки на курсе **Яндекс Практикум**.

| Роль | GitHub |
|------|--------|
| Team Lead | [InnaSof](https://github.com/InnaSof) |
| Backend Developer | [Torb7](https://github.com/Torb7) |
| Backend Developer | [Viktor-Popov19](https://github.com/Viktor-Popov19) |