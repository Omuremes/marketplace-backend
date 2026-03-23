# Session 01: Architecture Definition & Scaffold

**Date**: 2026-03-18
**Context**: Defining the strict Clean Architecture boundaries and delegating the initial boilerplate generation to AI.

---

### ENGINEER
Сгенерируй базовый каркас бэкенда для прототипа маркетплейса. 
Стек: FastAPI, SQLAlchemy 2.0 (async), asyncpg.

Архитектурные требования:
- Строгое следование Clean Architecture. 
- Слои: `domain`, `application` (DTOs, Services, UoW), `persistence` (Repositories, DB Mappers), `infrastructure`, `api`.
- Domain слой не должен иметь никаких зависимостей от FastAPI или ORM.
- База данных должна быть полностью скрыта за паттерном Unit of Work. Репозитории должны возвращать исключительно Domain-сущности (не ORM модели).

Вот желаемая структура:
[структура директорий]

Сгенерируй `scaffold.py` для создания этой структуры и подготовь конфигурацию `pyproject.toml` с poetry.

---

### AI
Я подготовил скрипт генерации `scaffold.py` и `pyproject.toml`. 
Структура директорий успешно создана. Были добавлены базовые зависимости (`fastapi`, `sqlalchemy`, `asyncpg`, `alembic`, `pydantic-settings`).

*Генерация файлов...*

Теперь я перейду к реализации доменных моделей: `Product`, `Seller`, `Offer` и Value Object `Money`.

---

### ENGINEER
Отлично. Реализуй модели ORM в слое Infrastructure и напиши мапперы для конвертации. Убедись, что репозитории абстрагируют доступ к БД.

---

### AI
Реализовано. Добавлен `DomainMapper`. Абстрактные репозитории и `UnitOfWork` добавлены в слой Application, а их конкретные SQLAlchemy-имплементации — в слой Persistence. Это позволит сервисам работать с БД транзакционно, не зная деталей реализации.
