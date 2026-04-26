# 🏭 ERP System (FastAPI)

> Учебный fullstack-проект: система учёта сотрудников и задач с аутентификацией и миграциями БД.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue?logo=postgresql)](https://postgresql.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

🔗 [Демо (если есть)](https://...) | 📄 [API Docs](https://.../docs)

---

## ✨ Фичи
- 🔐 Авторизация через JWT + refresh-токены
- 🗄 Миграции БД через Alembic
- 🔄 CRUD для сущностей User, Department, Task
- 🧪 Базовые тесты на Pytest (опционально, но сильно плюсует)

## 🛠 Стек
| Категория | Технологии |
|-----------|-----------|
| Backend | FastAPI, SQLAlchemy (async), Alembic, Pydantic |
| Database | PostgreSQL (через aiosqlite для демо) |
| Auth | JWT, password hashing (bcrypt) |
| DevOps | Poetry, .env, Dockerfile (опционально) |
| Testing | Pytest, httpx |

## 🚀 Как запустить локально
```bash
# 1. Клонировать
git clone https://github.com/danilov-dev/erp_fastapi.git
cd erp_fastapi

# 2. Установить зависимости
poetry install

# 3. Настроить .env (пример в .env.example)
cp .env.example .env

# 4. Применить миграции
alembic upgrade head

# 5. Запустить сервер
poetry run uvicorn app.main:app --reload

# 6. Открыть http://localhost:8000/docs
