FROM python:3.11

WORKDIR /app

COPY requirements.txt .
COPY vendor/dist ./vendor/dist

RUN python3 -m venv /opt/venv
#RUN /opt/venv/bin/pip install --disable-pip-version-check --no-cache-dir --no-deps --require-hashes -r requirements.txt
#RUN /opt/venv/bin/pip install --no-index --find-links vendor/wheels --only-binary=:all: --require-hashes -r requirements.txt
RUN /opt/venv/bin/pip install --no-index --find-links=vendor/dist -r requirements.txt
ENV PATH="/opt/venv/bin:$PATH"

COPY gpt-2/ ./gpt-2
COPY econstormodel/ ./gpt-2/models/econstormodel/

WORKDIR /app/gpt-2

CMD [ "python", "-u", "./src/new_server.py", "0", "artificialeconomist-mongo", "27017", "artificialeconomist-tensorflow", "8008" ]

