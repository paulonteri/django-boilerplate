# A well-written custom Dockerfile should respect this layering to make the most out of caching.
#   Whatever is on top of the Dockerfile should change the least, and on the bottom—the most.
FROM python:3.7-slim

# The environment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1
# This ensures that the Python interpreter doesn’t generate .pyc files
# which apart from being useless in our use-case, can also lead to few hard-to-find bugs.
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --upgrade pip

RUN pip install --no-cache-dir wheel

RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py collectstatic --verbosity 0 --noinput --clear

# The maximum concurrent requests are 'workers * threads'
# https://www.agiliq.com/blog/2017/11/how-performant-your-python-web-application/
# https://stackoverflow.com/a/41696500/10904662
# https://docs.gunicorn.org/en/stable/design.html#how-many-workers
# https://www.joelsleppy.com/blog/gunicorn-application-preloading/
# https://stackoverflow.com/a/60553901/10904662
# a smaller number helps allow us to create more cloud run instances
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 6 --preload backend.wsgi:application
