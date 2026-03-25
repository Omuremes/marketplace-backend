# Marketplace Backend

Backend часть маркетплейса на базе FastAPI.

## Технологии
- **FastAPI**: Современный асинхронный веб-фреймворк.
- **SQLAlchemy 2.0 + alembic**: Работа с БД и миграциями.
- **Pillow**: Обработка изображений (создание миниатюр).
- **MinIO**: S3-совместимое хранилище.
- **Pytest**: Тестирование.

## Особенности реализации
- **Audit Logs**: Все CRUD операции в админке логируются в таблицу `product_audit_logs`.
- **Presigned URLs**: Публичный доступ к бакету закрыт. Ссылки на изображения генерируются "на лету" с ограниченным временем жизни.
- **FSD-like Structure**: Логика разделена на слои (api, application, domain, infrastructure).

## Тестирование
Запуск тестов через Docker:
```bash
docker compose exec backend poetry run pytest
```
Или локально (нужна установленная poetry):
```bash
poetry install --with dev
pytest
```
