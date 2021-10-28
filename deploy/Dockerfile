FROM python:3.9.7-alpine3.14

RUN sed -i 's/https/http/' /etc/apk/repositories
RUN apk add --no-cache --virtual .persistent-deps curl

RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --upgrade pip
WORKDIR /python_web_learn

COPY requirements.txt /python_web_learn/requirements.txt
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org -r requirements.txt

COPY . /python_web_learn/

CMD [ "python", "/python_web_learn/manage.py", "runserver" ]