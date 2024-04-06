FROM python:3.8-alpine
RUN apk update && apk add bash && apk add --no-cache mariadb-dev && pip install --upgrade mysql-connector-python && pip install Flask flask-mysql
#&& pip install --upgrade pip
WORKDIR /app
COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
#CMD ["python", "app.py"] 