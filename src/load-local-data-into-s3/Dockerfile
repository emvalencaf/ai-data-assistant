FROM python

WORKDIR /app

# vol read-only
VOLUME [ "/dataset" ]

# copy apps deps
COPY  ./requeriments.txt /tmp/requeriments.txt

# copy scripts
COPY . .

# install deps
RUN pip install --no-cache-dir -r /tmp/requeriments.txt

# copy files in dattaset/raw dir to vol
COPY ./dataset/raw /dataset

CMD [ "python", "main.py"]