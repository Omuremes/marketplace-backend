# Session 04: Database Strict Schema Compliance

**Date**: 2026-03-18
**Context**: Enforcing strict SQL schema constraints (Numeric fields, object keys, and foreign keys) onto the existing SQLAlchemy models based on the mandatory specification.

---

### ENGINEER
Минимальная модель данных должна строго соответствовать следующему формату:
Таблица `products`: `price_amount numeric(12,2)`, `image_object_key text null`, `thumbnail_object_key text null`, `created_at timestamptz`, `updated_at timestamptz`.
Таблица `product_attributes`: `id uuid pk`, `product_id fk (cascade)`, `key text`, `value text`.
Таблица `sellers`: `rating numeric(3,2)`.
Таблица `offers`: `price_amount numeric(12,2)`.

Текущая реализация хранит атрибуты внутри JSONB-колонки `products.attributes`, а для картинок используются `image_url` и `thumbnail_url`.
Темовая задача:
1. Создать отдельную таблицу (и SQLAlchemy модель) для `product_attributes`. Настроить `relationship` и Eager Loading.
2. Привести все типы `Float` к `Numeric` с точным указанием precision/scale.
3. Заменить `_url` на `_object_key`.
4. Переписать Alembic-миграцию `0001_initial_schema.py` с нуля под новую схему.
5. Настроить Minio-клиент, чтобы при загрузке он возвращал только объектный ключ, а полные URL формировал отдельным методом на лету для слоя DTO.

Приступай к рефакторингу. Сделай wipe БД через Docker и накати заново.

---

### AI
Рефакторинг завершен:
1. Создана модель `ProductAttributeModel`. В репозитории `product_repo.py` добавлена инструкция `selectinload(ProductModel.attributes)` для правильного асинхронного извлечения данных без ленивой загрузки.
2. `float` колонки заменены на `Numeric(12, 2)` и `Numeric(3, 2)` согласно требованиям. При маппинге доменных сущностей добавлено явное приведение типов.
3. Добавлены поля `created_at` и `updated_at` с `DateTime(timezone=True)` и триггерами `now()`.
4. В `minio_client.py` добавлен метод `get_file_url`, который собирает абсолютный путь. API и сервисы переведены на генерацию URL на лету, а в БД хранятся ключи (S3 Object Keys).
5. Файл миграций переписан, `docker compose down -v` выполнен для уничтожения старой схемы базы данных.
6. Скрипт `seed_data.py` обновлен для работы с ключами (с фоллбеком для http-плейсхолдеров) и запущен на чистой БД.

Спецификация моделей данных теперь соблюдена строго на 100%.
