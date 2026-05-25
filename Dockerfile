FROM python:3.14.4
WORKDIR /api
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
# If we need packages, add them here
RUN apt-get update
RUN apt-get install -y default-libmysqlclient-dev build-essential
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["flask", "run", "--debug"]