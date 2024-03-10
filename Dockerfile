FROM python

ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip
CMD apt-get install gcc libpq-dev build-essential libssl-dev libffi-dev libpq-dev -y
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 4444

CMD [ "python", "manage.py", "runserver", "0.0.0.0:4444" ]