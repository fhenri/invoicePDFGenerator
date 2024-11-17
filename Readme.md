# Run locally

## setup virtual environment

```
$ python3 -m venv venv
$ source venv/bin/activate
venv $ python --version
Python 3.12.6
```

## install the dependencies

we need to install [wkhtmltopdf](https://wkhtmltopdf.org/), it comes as a system dependency
```
$ brew install wkhtmltopdf
```

and to install the python dependencies

```
venv $ pip install --no-cache-dir -r requirements.txt
```

## run with a sample

```
venv $ python invoice.py sample/payload.json
```

# Run with Docker

## building the Docker image

```
$ docker build . --tag 'invoice-generator'
[+] Building 3.0s (13/13) FINISHED                                   docker:desktop-linux
 => [internal] load build definition from Dockerfile                                 0.0s
 ...
```

```
$ docker image list
REPOSITORY                 TAG       IMAGE ID       CREATED              SIZE
invoice-generator          latest    xxxxxxxxxxxx   xxxxxxxx             330MB
```

## running the Docker image

Command `EXPOSE` in your Dockerfile lets you bind container's port to some port on the host machine but it doesn't do anything else. When running container, to bind ports specify `-p` option.

In our case, we expose port 5000. After building the image when we run the container, run docker with option `-p 5001:5001`. This binds container's port 5001 to our laptop/computers port 5001 and that portforwarding lets container to receive outside requests.

```
$ docker run -it -p 5001:5001 invoice-generator
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://172.17.0.2:5001
Press CTRL+C to quit
```

open a different terminal
```
curl http://127.0.0.1:5001/
Hey Invoice Generation App!
```

### using docker to develop

If you're running the container for development you need volumes for hot reloading and replacing the image's /app directory with the host's source code folder.

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" invoice-generator
```
