# yamdb_final
![Workflow status](https://github.com/sharumario/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg) 

### YaMDb о проекте и авторах:
Проект является агрегатором отзывов о фильмах, книгах и музыке.

Список разработчиков:
- [Гусейнов Нажмудин](https://github.com/Casp1an "https://github.com/Casp1an.com")
- [Халус Кузьма](https://github.com/Domovoy-k "https://github.com/Domovoy-k")
- [Шайхнисламов Марат](https://github.com/Sharumario "https://github.com/Sharumario")

### Подготовка репозитория:

Клонируйте репозиторий:
git clone git@github.com:sharumario/yamdb_final.git
В репозитории на гитхаб добавьте ключи в Settings - Secrets - Actions

DOCKER_USERNAME - имя пользователя docker
DOCKER_PASSWORD - пароль docker
HOST - ip-адрес сервера
USER - имя пользователя для сервера
SSH_KEY - приватный ключ с компьютера, имеющего доступ к боевому серверу cat ~/.ssh/id_rsa
PASSPHRASE - пароль для сервера
DB_ENGINE=django.db.backends.postgresql - указываем, что работаем с postgresql
DB_NAME=postgres - имя базы данных
POSTGRES_USER - логин для подключения к базе данных
POSTGRES_PASSWORD - пароль для подключения к БД
DB_HOST=db - название сервиса (контейнера)
DB_PORT=5432 - порт для подключения к БД
TELEGRAM_TO - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота)

Измените имя пользователя DockerHub в docker-compose.yaml на ваше

### Подготовка сервера:

- Запустите сервер и зайдите на него ssh username@ip_address
- Установите обновления apt: sudo apt update; sudo apt upgrade -y
- Установите nginx sudo apt install nginx -y
- Остановите службу nginx sudo systemctl stop nginx
- Установите docker sudo apt install docker.io
- Установите docker-compose: Выполните команду, чтобы загрузить текущую стабильную версию     Docker Compose:
  sudo curl -SL https://github.com/docker/compose/releases/download/v2.6.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
  Примените к файлу права доступа:
  sudo chmod +x /usr/local/bin/docker-compose
  Проверьте установку (должна вернуться версия docker-compose):
  docker-compose --version
- Создайте на сервере два файла и скопируйте в них код из проекта на GitHub:
  docker-compose.yaml в home/#username#/
  nginx/default.conf в home/#username#/nginx/

### Развертывание приложения на боевом сервере:

Развёртывание происходит автоматически с помощью Actions workflow. В файле yamdb_workflow.yml описана автоматическая последовательность действий при push репозитория. За состоянием работы Actions workflow можно проследить во вкладке Actions в репозиторий GitHub.

Суперюзер создаётся внутри сервера, с помощью команды:

sudo docker-compose exec web python createsuperuser

### Полное описание проекта с примерами запросов:

http://178.154.222.78/redoc/
