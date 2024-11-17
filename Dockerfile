FROM python:3.11-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y wget xfonts-75dpi fontconfig libjpeg62-turbo libx11-6 libxcb1 libxext6 libxrender1 xfonts-base
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb \
    && dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb \
    && apt --fix-broken install
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ .

EXPOSE 5001

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5001"]
