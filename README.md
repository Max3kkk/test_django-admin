# Django-admin panel for a shop

### Build and run:

`docker-compose up -d --build`

### Instructions for stopping

`docker-compose down`

### Postgres credentials
```
username: postgres
password: postgres
port: 5432
```

## To create a superuser run:
`docker exec -it admin python manage.py createsuperuser`