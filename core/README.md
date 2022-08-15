# Django Boilerplate

## Running the project

### Django

```bash
python manage.py runserver
```

### Celery worker

```bash
celery -A backend worker -l info
```

### Celery beat

```bash
celery -A backend beat -l info
```

### Celery flower

```bash
celery -A backend flower -l info --persistent=True
```

Visit the dashboard at <http://localhost:5555>
