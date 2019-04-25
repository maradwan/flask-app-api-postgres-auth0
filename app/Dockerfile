FROM python:3.6
LABEL maintainer="Mohamed Radwan"

# Place app in container.
COPY . /opt/www
WORKDIR /opt/www

# Install dependencies.
RUN pip install -r requirements.txt

EXPOSE 5000
#CMD python runserver.py
CMD [ "uwsgi", "--ini", "app.ini" ]
