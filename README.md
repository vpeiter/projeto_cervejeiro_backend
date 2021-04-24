# Backend of PI course's project at UFSC

These instructions are meant for project colleagues not familiar with Docker.

For those running on Windows, please install Docker for Windows and Git for Windows,
and run the commands listed here in Git Bash terminal (MINGW64).

## To build and run

This project is built and runs using docker compose, which allows a single command to be used for this purpose:
```
docker-compose -f docker-compose.yml up -d --build
```

## To connect to the database using psql
To connect to the database using psql run:
```
docker exec -it backend_postgres_db_1 psql -U postgres cervejeiro
```


## To kill services and remove containers
To connect to the database using psql run:
```
docker-compose kill
docker-compose rm
```

## Database persistance
The database saves content on a named docker volume. To list volumes use:
```
docker volume ls
```
To delete all data stored use:
```
docker volume rm <volume_name>
```
