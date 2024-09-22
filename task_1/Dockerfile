FROM python:3.10-slim

WORKDIR /task_1

COPY requirements.txt /task_1/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /task_1/

CMD ["python", "main.py"]
