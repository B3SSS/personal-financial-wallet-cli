# personal-financial-wallet-cli
## Пэт-проект "Разработка консольного приложения "Личный финансовый кошелек"" (Linux)
### Порядок действий:
#### 1. Клонировать репозиторий к себе (через HTTPS или Github Desktop)
command: git clone https://github.com/B3SSS/personal-financial-wallet-cli.git
#### 2. Дальше порядок зависит от вашей операционной системы
Linux:
1. Создать виртуальное окружение: python3 -m venv .venv, где
   - python3 - язык программирования;
   - .venv - название виртуальной среды.
2. Активировать виртуальную среду: source /.venv/bin/activate.bat;
3. Скачать все зависимости из файла **requirements.txt**: pip3 install -r requirements.txt;
4. Перейти в папку **/src** и запустить файл **main.py** командой: python3 main.py.

Windows (требует наличия WSL, в данном примере рассматривается Docker Desktop):
1. Запустить Docker Desktop;
2. Собрать образ из Dockerfile, лежащего в корневой папке проекта: docker build -t personal-wallet . , где
   - -t personal-wallet - название образа;
   - . - текущая директория.
3. Создать контейнер в интерактивном режиме: docker run -it --name personal-wallet-container personal-wallet bash, где
   - run - команда запуска контейнера;
   - -it - интерактивный режим;
   - --name personal-wallet-container - название контейнера;
   - personal-wallet - созданный ранее образ;
   - bash - запуск командной оболочки bash.
4. В результате третьего действия вы окажитесь внутри контейнера, где необходимо выполнить команду для запуска приложения: cd app && python3 main.py.

#### В итоге откроется главная страница приложения:
![image](https://github.com/B3SSS/personal-financial-wallet-cli/assets/113550281/35aad474-71f2-443a-8d42-3f778cc219ab)

