FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --disable-pip-version-check --no-cache-dir --no-deps --require-hashes -r requirements.txt

# Ensure the virtual environment is activated for future commands
ENV PATH="/opt/venv/bin:$PATH"

COPY gpt-2/ /app/gpt-2
WORKDIR /app/gpt-2

COPY new_server.py ./src/
COPY econstormodel/ ./models/econstormodel/

CMD [ "python", "-u", "./src/new_server.py", "0", "artificialeconomist-mongo", "27017", "artificialeconomist-tensorflow", "8008" ]

