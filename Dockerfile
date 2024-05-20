FROM python:3.8-slim-buster


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# To access SQL SERVER below applications are required
RUN apt-get update \
 && apt-get install unixodbc -y \
 && apt-get install unixodbc-dev -y \
 && apt-get install freetds-dev -y \
 && apt-get install freetds-bin -y \
 && apt-get install tdsodbc -y \
 && apt-get install --reinstall build-essential -y

 # populate "ocbcinst.ini for FreeTDS"
RUN echo "[FreeTDS]\n\
Description = FreeTDS unixODBC Driver\n\
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini


# optional: kerberos library for debian-slim distributions
RUN apt-get install -y --no-install-recommends gcc libc-dev python3-dev openjdk-11-jre-headless libreoffice ghostscript curl

RUN pip install --upgrade pip
RUN pip install torch==1.11.0+cpu torchvision==0.12.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

WORKDIR /app


COPY ./requirements.txt /app/
RUN pip install -r /app/requirements.txt

RUN apt-get install poppler-utils
RUN apt-get install -y tesseract-ocr

RUN apt-get install -y wget


COPY . /app
WORKDIR /app
ENTRYPOINT [ "python" ]

EXPOSE 5000

CMD ["app.py" ]
