# Telegramm bot helper for AdGuard VPN

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
python3 src/app.py
```