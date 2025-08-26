# Telegram bot helper for AdGuard VPN

## Описание сервиса

Если вы как и я пользуетесь бесплатным AdGuardVPN, то сталкивались с тем, что он предоставляет лишь 3 Гб траффика в месяц. Легкое решение - создать множество аккаунтов, но появляется новая проблема:

- Ты посстоянно забываешь, на каком аккаунте ты был, а на каком нет
- Обновился ли уже траффик на аккаунте или нет

Поэтому эффективное решение проблемы:

**Тг-помощник в работе с AdGuard VPN**:

- add_mail, добавить новый аккаунт (нужен `email` и через сколько обновится траффик)
- info, получить список всех аккаунтов
- mark_used, пометить аккаунт, на котором закончился траффик (нужен `email`)
- delete_mail, удалить аккаунт (нужен `email`)
- find_free, найти первый аккаунт, что свободен на данный момент

Сервис сам раз в день запускает `refresh` и обновляет траффик у аккаунтов, у которых произошло обновление.

Если у вас пропадет интернет на машине, сервис перестанет отвечать, но при подключении будут обработаны все ответы.

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

## Хостинг и продакшн

Если вы хотите чтобы сервер работал постоянно и не на вашем ноутбуке, вам нужен удаленный сервер (например, YandexCloud).

### Первый запуск

1) Настройте ВМ(в моем случае через `ssh`), склонируйте репозиторий туда, перенесите (если есть), вашу БД
2) Установите Docker ([ссылка](https://docs.docker.com/engine/install/ubuntu/))
3) Чтобы БД не терялась и хранилось и на хосте:

    - Перейдите в папку проекта:

        ```bash
        cd /home/$USER/adguard-vpn-helper
        PROJECT_DIR=$(pwd)
        echo "Project dir: $PROJECT_DIR"
        ```

    - Создадим папку на хосте, где будут лежать данные

        ```bash
        HOST_DATA_DIR="/home/$USER/adguard-data"
        sudo mkdir -p "$HOST_DATA_DIR"
        sudo chown $USER:$USER "$HOST_DATA_DIR"
        chmod 700 "$HOST_DATA_DIR"
        ```

    - Скопируем существующий data.db в эту папку (если он уже в проекте)

        ```bash
        if [ -f "$PROJECT_DIR/data.db" ]; then
        cp "$PROJECT_DIR/data.db" "$HOST_DATA_DIR/data.db"
        echo "Copied existing data.db -> $HOST_DATA_DIR/data.db"
        else
        echo "В проекте нет data.db"
        sqlite3 "$HOST_DATA_DIR/data.db" "VACUUM;" >/dev/null 2>&1 || touch "$HOST_DATA_DIR/data.db"
        fi

        chmod 600 "$HOST_DATA_DIR/data.db"
        ```

    - Теперь актуальная БД хранится на хосте в `$HOST_DATA_DIR/data.db`

4) Соберем образ:

    ```bash
    docker build -t adguard-helper:latest .
    ```

5) Запуск контейнера:

    ```bash
    docker run -d \
    --name adguard-helper \
    -p 8000:8000 \
    -e TOKEN=<place your token here> \
    --restart unless-stopped \
    -v "$HOST_DATA_DIR/data.db":/adguard-vpn-helper/data.db \
    adguard-helper:latest
    ```

Проверьте, что контейнер запущен `docker ps`

Посмотреть логи можно так: `docker logs -f adguard-helper`

Остановить контейнер: `docker stop adguard-helper`

Запустить заново(если есть образ): `docker start adguard-helper`

### Установить обновление

1) Перейдите в репозиторий и выполните `git pull origin main`
2) Пересоберите образ

    ```bash
    docker build -t adguard-helper:latest .
    ```

3) Остановите старый контейнер:

    ```bash
    docker stop adguard-helper
    docker rm adguard-helper
    ```

4) Запустите новый контейнер:

    ```bash
    docker run -d \
    --name adguard-helper \
    -p 8000:8000 \
    -e TOKEN=<place your token here> \
    --restart unless-stopped \
    -v "$HOST_DATA_DIR/data.db":/adguard-vpn-helper/data.db \
    adguard-helper:latest
    ```

## TODO

- Покрыть тестами все сценарии (сейчас процент покрытия `40%`)
- Улучшить refresh, чтобы он запускался сразу после поднятия сервиса
- Добавить кнопки для выбора нужного аккаунта(для `delete, mark_used`)
- Добавить уточняюшие сообщения для упрощения `add_mail`
- Добавить валидацию почты
- Добавить уведомления если траффик у аккаунта обновился (`must-have feature`)
- Сделать БД асинхронной (вместо `asyncio.to_thread`)
