FROM python:3.11

WORKDIR /app

# Note these are *my* requirements
COPY requirements.txt .
RUN pip3 install --disable-pip-version-check --no-cache-dir --no-deps --require-hashes -r requirements.txt

COPY gpt-2/ /app/gpt-2
WORKDIR /app/gpt-2

COPY new_server.py ./src/
COPY econstormodel/ ./models/econstormodel/

CMD [ "python3", "-u", "./src/new_server.py", "0", "artificialeconomist-mongo", "27017", "artificialeconomist-tensorflow", "8008" ]
