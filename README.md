# SERVICE-EXERCISES

---

## Оглавление

1. [Назначение](#назначение)
2. [Функциональность](#функциональность)
3. [Технологии](#технологии)
4. [Конфигурация](#конфигурация)
5. [Локальная разработка](#локальная-разработка)
6. [Развертывание](#развертывание)
7. [Лицензия](#лицензия)

## Назначение

Микросервис управлежния упражнениями предназначен для реализации CRUD операций над обучающими упражнениями.

## Функциональность

- Листинг обучающих упражнений.
  - Пагинация
- Детальная информация по конкретному упражнению.
- Создание (добавление) в систему ILPS новых упражнений.
- Удаление неактуальных упражнений из системы.
- Редактирование уже существующих упражнений.

## Технологии

- Язык программирования: Python
- Фреймворк: FastAPI
- База данных: PostgreSQL + SQLAlchemy (asyncpg)
- Протоколы: HTTP

## Конфигурация

Микросервис настраивается с помощью переменных окружения в конфигурационном файле `.env`. По умолчанию `.env` не содержится в репозитории, данный файл необходимо создать самому:

```bash
touch .env
```

Если вы используете `VSCode`, не забудьте перезагрузить окно проекта, чтобы применить изменения в `.env` к вашему окружению.  
Или используйте следующую команду:

```bash
export $(cat .env)

```

Пример того, как можно заполнить файл `.env`, содержится в файле `.env.example`.

Ниже приведены таблицы, содержащие описание основных параметров, которые необходимо настроить для работы сервиса.

### Настройки общего характера

| **Переменная**       | **Значимость** | **Описание**                                       | **Тип данных** | **Стандартное значение**  |
|:--------------------:|:--------------:|:--------------------------------------------------:|:--------------:|:-------------------------:|
| EXERCISES_DEBUG_MODE     | Опционально    | Флаг запуска микросервиса в режиме отладки.        | BOOL           | True                      |
| EXERCISES_SERVICE_NAME   | Опционально    | Имя микросервиса. Рекомендуется вообще не трогать. | STRING         | ilps-service-texts        |

### Настройки базы данных

Перед тем как конфигурировать данные, по которым микросервис будет подключаться к экземпляру PGSQL, убедитесь, что PGSQL содержит
в себе **ранее созданного пользователя и базу данных (схему)**, согласно стандарным значениями переменных таблицы. Стандартные значения являются рекомендательными.

| **Переменная**                 | **Значимость** | **Описание**                     | **Тип данных** | **Стандартное значение** |
|:------------------------------:|:--------------:|:--------------------------------:|:--------------:|:------------------------:|
| EXERCISES_DB_POSTGRES_PASSWORD | Обязательно    | Пароль пользователя PGSQL.       | STRING         |                          |
| EXERCISES_DB_POSTGRES_HOST     | Обязательно    | Адрес хоста с развернутым PGSQL. | STRING         |                          |
| EXERCISES_DB_POSTGRES_USER     | Опционально    | Имя пользователя PGSQL.          | STRING         | service_auth             |
| EXERCISES_DB_POSTGRES_NAME     | Опционально    | Имя базы данных (схемы) PGSQL.   | STRING         | auth                     |
| EXERCISES_DB_POSTGRES_PORT     | Опционально    | Порт хоста с развернутым PGSQL.  | INTEGER        | 5432                     |

### Настройки Graylog

Сервис поддерживает отправку логов в Graylog, если эта функция включена при помощи специальной переменной среды.

| **Переменная**           | **Значимость** | **Описание**                                       | **Тип данных** | **Стандартное значение**  |
|:------------------------:|:--------------:|:--------------------------------------------------:|:--------------:|:-------------------------:|
| EXERCISES_GRAYLOG_ENABLE | Опционально    | Флаг отправки логов в Graylog.                     | BOOL           | False                     |
| EXERCISES_GRAYLOG_HOST   | Опционально    | Адрес развернутого Graylog. Может быть заглушкой.  | STRING         | localhost                 |
| EXERCISES_GRAYLOG_PORT   | Опционально    | Порт развернутого Graylog. Может быть заглушкой.   | STRING         | 12201                     |

## Локальная разработка

Для удобства локальной разработки микросервиса следуйте этим рекомендациям.

### Установка зависимостей

Перед началом работы убедитесь, что все зависимости установлены. Или установите, если предыдущее условие ложно.  
При разработке сервиса используется менеджер зависимостей `Poetry`.

```bash
pip install poetry
```

```bash
poetry install --no-root
```

Далее выберете виртуальную среду `Poetry` как основную для проекта.

### Переменные окружения

Создайте файл `.env` и сконфигурируйте переменные огружения, согласно главе [конфигурация](#конфигурация).  
В контексте локальной разработки необходимо задать только **обязательные** переменные среды. Опциональную переменную `EXERCISES_DEBUG_MODE` рекомендуется перевести в значение `True`.

### Подготовка базы данных

Вероятнее всего подготовленный экземпляр PGSQL содержит в себе пустую базу данных (схему), необходимую для работы сервиса. В таком случае необходимо применить миграции `Alembic`:

```bash

alembic upgrade head
```

`Alembic` самостоятельно создаст все нужные таблицы, применяя к ним последние изменения по ходу разработки.

### Запуск

Теперь все готово к запуску!

```bash
python start.py

```

## Развертывание

Для развертывания микросервиса в production-среде следуйте инструкциям, описанным в [этом](https://github.com/FEFU-ILPS/ILPS?tab=readme-ov-file#-развертывание-системы) репозитории.  
Сервис аутентификации в инфраструктуре ILPS будет развернут автоматически посредством `docker-compose`.

Процессы установки зависимостей и применения миграций автоматизированны при сборке Docker контейнера.

## Лицензия

Этот проект распространяется под лицензией **GNU General Public License v3.0 (GPL-3.0)**.
