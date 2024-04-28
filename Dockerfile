
FROM python:3.8-slim-buster
 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
 
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc-dev python3-dev openjdk-11-jre-headless libreoffice ghostscript curl \
    && apt-get install -y poppler-utils tesseract-ocr wget
 
RUN pip install --upgrade pip
 
WORKDIR /app
 
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt
 
COPY . /app
 
ENTRYPOINT ["python"]
 
CMD ["app.py"]
 
EXPOSE 5000
 