Тестовое задание для компании Kerka

# Бот для приёма платежей на QIWI-кошелёк.

## Настройка:
* Переименовать файл `editme.env` в `.env`
* Заполнить поля: `API_TOKEN` и `QIWI_PRIV_KEY` и по-желанию отредактировать настройки базы данных в файле `.env`
### Settings.py
* Установить `DEBUG=True` если хотите использовать sqlite вместо postgres
* Добавить админов (их телеграм id) в поле `ADMINS` файлы `settings.py`
* Настроить параметры `WEBHOOK*` если хотите использовать вебхук

## Запуск
* Собрать и запустить докер `docker-compose up --build -d`

Либо
* Отдельно запустить postgres, установить зависимости из файла `requirements.py` и запустить файл `main.py`
