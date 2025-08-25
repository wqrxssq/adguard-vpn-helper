# Telegramm bot helper for AdGuard VPN

## Описание сервиса:

`TBA`

## Работа с сервисом

1) Установите виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate
```

2) Установите зависимости:

```bash
pip install -r requirements.txt
```

3) Получите `token` для бота телеграмма у `@BotFather` и установите в окружении:

```bash
export TOKEN=<your token>
```

4) Запустите сервер:

```bash
python3 -m src.app
```

## Запуск в докерконтейнере

Перед запуском убедитесь что у вас установлен `Docker` или `Docker Desktop`.

1) Сборка контейнера:

```bash
docker build -t adguard-helper .
```

2) Запуск контейнера: (С пробросом токена для бота)

```bash
docker run -d \
  -p 8000:8000 \
  -e TOKEN=<your_secret_token> \
  adguard-helper
```

## Запуск тестов

1) Установите виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate
```

2) Установите зависимости:

```bash
pip install -r requirements.txt
```

3) Запустите тесты:

```bash
python3 -m pytest -q
```

## Ручной просмотр бд

Войти в бд можно с помощью утилиты `sqlite3`:

```bash
sqlite3 data.db
```

Посмотреть схему таблицы `accounts`:

```bash
.schema accounts
```

Посмотреть все поля из таблицы:

```bash
SELECT * FROM accounts;
```

Примерный вид:

`1102311129|one@mail.ru|2025-08-10|2025-09-09|0`

`1102311129|two@mail.ru|2025-08-06|2025-09-05|0`