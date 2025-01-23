#FROM tensorflow/tensorflow:1.15.5-py3
#FROM python:3.6.9
#FROM python:3.7
FROM python:3.11
#RUN rm /etc/apt/sources.list.d/cuda.list /etc/apt/sources.list.d/nvidia-ml.list

#RUN apt-get update && apt-get install --no-install-recommends --yes \
#  git                                                               \
#  && apt-get clean                                                  \
#  && rm -rf /var/lib/apt/lists/*                                    \
#  && rm -rf /usr/share/doc/* /usr/share/man/*

#RUN apt-get clean                                                   \
#  && rm -rf /var/lib/apt/lists/*                                    \
#  && rm -rf /usr/share/doc/* /usr/share/man/*

WORKDIR /app

# Note these are *my* requirements
COPY requirements.txt .
RUN pip3 install --disable-pip-version-check --no-cache-dir -r requirements.txt

COPY gpt-2/ /app/gpt-2
#RUN git clone https://github.com/openai/gpt-2
WORKDIR /app/gpt-2
#RUN git checkout a74da5d
#RUN rm -rf .gitignore .gitattributes .git/

COPY new_server.py ./src/
COPY econstormodel/ ./models/econstormodel/

# Note these are *gpt2* requirements (WORKDIR changed)
#RUN pip3 install --disable-pip-version-check --no-cache-dir -r requirements.txt

CMD [ "python3", "-u", "./src/new_server.py", "0", "artificialeconomist-mongo", "27017", "artificialeconomist-tensorflow", "8008" ]
