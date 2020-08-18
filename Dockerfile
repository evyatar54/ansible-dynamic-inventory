FROM python:3.8.5-slim

COPY . /workspace

WORKDIR /workspace

RUN pip install -r requirements.txt

CMD ["python", "AnsibleDI/manage.py", "runserver"]