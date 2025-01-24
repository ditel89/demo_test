FROM python:3.11
RUN apt-get update

WORKDIR /app
COPY requirement.txt /app/requirement.txt
RUN pip install --upgrade pip
RUN pip install -r requirement.txt
COPY Subinfluxdb.py /app/Subinfluxdb.py
CMD [ "python3", "Subinfluxdb.py" ]