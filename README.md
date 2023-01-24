# Developing an API with FastAPI, SQLAlchemy, PostgresSQL

Menu -> Submenu -> Dish

## Want to use this project?

Build the images and run the containers:

```sh
$ docker-compose up -d --build
```
```sh
$ docker-compose down
```
```sh
$ docker-compose --file docker-compose.test.yml up -d --build
```
```sh
$ docker-compose --file docker-compose.test.yml down
```
```sh
$ docker-compose exec test_web pytest .
```


Test out the following routes:

1. [http://localhost:8000/docs](http://localhost:8000/docs)

