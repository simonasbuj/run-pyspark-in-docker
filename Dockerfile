FROM bitnami/spark:3.3.4

WORKDIR /app
COPY . /app
COPY /host_input/jars/* /opt/bitnami/spark/jars/

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/logs

CMD ["spark-submit", "--master", "local[2]", "main.py"]
