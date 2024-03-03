FROM python

WORKDIR /app

# copy apps deps
COPY  ./requeriments.txt /tmp/requeriments.txt

# copy scripts
COPY . .

# install deps
RUN pip install --no-cache-dir -r /tmp/requeriments.txt

CMD [ "python", "main.py"]