![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=ASYNC+MINECRAFT+CHAT)


Это проект асинхронного чата для игры майнкрафт. 
С помошью скрипта `show_chat.py` вы можете смотреть переписку в чате у себя в консоли и записывать ее в файл.
С помошью скрипта `write_to_chat.py` вы можете написать сообщение в чат, передав его в виде параметра 
    при запуске.

## Работа скрипта:

### Запуск чата из консоли
```sh
python3 show_chat.py  # запуск без доп параметров
```
```sh
# запуск с доп. параметрами (необязательные)
python3 show_chat.py -f log.txt -c minechat.dvmn.org -p 5000
```

### show_chat.py можно запускать с доп. необязательными параметрами через консоль
* `'-f', '--FILE'` - Укажите название файла где будет записываться история переписки чата.
* `'-c', '--HOST'` - Укажите название хоста для подключения к секретному чату.
* `'-p', '--PORT'` - Укажите название порта для подключения к секретному чату.

### show_chat.py конфигурация через .env файл, создайте его радом со скриптом
```sh
FILE=logs_history      # Укажите название файла где будет записываться история переписки чата.
HOST=minechat.dvmn.org # Укажите название хоста для подключения к секретному чату.
PORT=5000              # Укажите название порта для подключения к секретному чату.
```
---
### Написание сообщения в чат
```sh
python3 write_to_chat.py 'Всем привет!'  # запуск без доп параметров
```
```sh
# запуск с доп. параметрами (необязательные)
python3 write_to_chat.py 'Всем привет!' -u Max -c minechat.dvmn.org -p 5050
```

### write_to_chat.py нужно запускать с обязательным позиционным параметром в виде теста сообщения, также можно добавить доп. параметры через консоль

* `'-t', '--TOKEN'` - Укажите токен для доступа в чат от вашего имени в файле `token.txt` или сгенерируйте новый токен просто запустив скрипт
* `'-u', '--NAME'` - Укажите имя которое будет использовано для общения в чате при генерации токена.
* `'-c', '--HOST'` - Укажите название хоста для подключения к секретному чату.
* `'-p', '--PORT_TO_WRITE'` - Укажите название порта для подключения к секретному чату.

### write_to_chat.py конфигурация через `.env` файл, создайте его радом со скриптом
```sh
NAME=Sergey      # Укажите имя которое будет использоваться в чате при генерации токена.
HOST=minechat.dvmn.org # Укажите название хоста для подключения к секретному чату.
PORT=5000              # Укажите название порта для подключения к секретному чату.
```

### write_to_chat.py конфигурация токена через `token.txt` файл, создайте его радом со скриптом
```sh
TOKEN=1s5sf5dds4d6s56s464   # Укажите токен для авторизации в чате под вашим ником.
```

## Установка

Используйте данную инструкцию по установке этого скрипта

1. Установить

```python
git clone https://github.com/Maxim-Pekov/async_minecraft_chat.git
```

2. Установите зависимости командой ниже:
```python
poetry install
```
 
3. Активируйте виртуальное окружение 
```python
poetry shell
```

## About me

[<img align="left" alt="maxim-pekov | LinkedIn" width="30px" src="https://img.icons8.com/color/48/000000/linkedin-circled--v3.png" />https://www.linkedin.com/in/maxim-pekov/](https://www.linkedin.com/in/maxim-pekov/)
</br>

[<img align="left" alt="maxim-pekov" width="28px" src="https://upload.wikimedia.org/wikipedia/commons/5/5c/Telegram_Messenger.png" />https://t.me/MaxPekov/](https://t.me/MaxPekov/)
</br>

[//]: # (Карточка профиля: )
![](https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=Maxim-Pekov&theme=solarized_dark)

[//]: # (Статистика языков в коммитах:)

[//]: # (Статистика языков в репозиториях:)
![](https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=Maxim-Pekov&theme=solarized_dark)
![](https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=Maxim-Pekov&theme=solarized_dark)


[//]: # (Статистика профиля:)

[//]: # (Данные по коммитам за сутки:)
![](https://github-profile-summary-cards.vercel.app/api/cards/stats?username=Maxim-Pekov&theme=solarized_dark)
![](https://github-profile-summary-cards.vercel.app/api/cards/productive-time?username=Maxim-Pekov&theme=solarized_dark)

[//]: # ([![trophy]&#40;https://github-profile-trophy.vercel.app/?username=Maxim-Pekov&#41;]&#40;https://github.com/ryo-ma/github-profile-trophy&#41;)

