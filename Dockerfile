FROM python:3.8.5-alpine3.12

COPY . /workspace

WORKDIR /workspace

RUN pip install -r requirements.txt

CMD ["python", "AnsibleDI/manage.py", "runserver"]