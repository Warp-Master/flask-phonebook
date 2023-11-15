FROM python:3.11-alpine

WORKDIR app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "gunicorn", "--reload", "-b", "0.0.0.0:5000", "main:app" ]
