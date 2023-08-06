FROM --platform=linux/amd64 python:3.9
WORKDIR /lndb-rest
COPY . /lndb-rest
RUN pip install --upgrade .
ENTRYPOINT python3 ./lndb_rest/main.py
