# MacでREDMINEを起動させる。

##  docker-compose.ymlファイルを作成する。

docker-compose.yml
```
version: '3.8'
services:
  redmine:
    container_name: redmine
    image: redmine
    restart: always
    ports:
      - 3000:3000
    volumes:
      - ./Redmine/plugins:/usr/src/redmine/plugins
      - ./Redmine/themes:/usr/src/redmine/public/themes
    environment:
      REDMINE_DB_MYSQL: redmine-db
      REDMINE_DB_PASSWORD: redmine
  redmine-db:
    image: mariadb
    container_name: redmine-db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: redmine
      MYSQL_DATABASE: redmine
    volumes:
      - ./db:/var/lib/mysql
    command: mysqld --character-set-server=utf8 --collation-server=utf8_unicode_ci

```
## DockerでRedmineを立ち上げる（docker-compose）

```bash
$ docker-compose up -d
```

## 参考
[MacでDockerコンテナ上にRedmineを構築する](https://qiita.com/TakSus/items/1f8bf5eab24548a7ed28)