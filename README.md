# Image Processing Service
[![Build Status](https://cloud.drone.io/api/badges/ukrvassabi/svc-img-processing/status.svg)](https://cloud.drone.io/ukrvassabi/svc-img-processing)

## General information
Image Processing Service allows you to upload images and download zoomed and cropped images after that.  

### Technologies and frameworks
- [Python 3.7.1](https://www.python.org/downloads/release/python-371/)
- [AIOHTTP 3.5.0](https://docs.aiohttp.org/en/stable/)
- [aiosqlite 0.8.0](https://github.com/jreese/aiosqlite)
- [Pillow 5.3.0](https://pillow.readthedocs.io/en/5.3.x/)
- [Docker](https://www.docker.com/)
- [docker-compose 1.22](https://docs.docker.com/compose/)

### Running project
It can be done in two ways: with Gunicorn and Docker

#### Gunicorn
1. Create new virtual environment with python 3.7: `make env`.
1. Run gunicorn application: `make run-gunicorn`.
1. Open swagger specification: [http://localhost:8022/api/v1/doc](http://localhost:8022/api/v1/doc)
1. Upload and download files.
1. Examples how to use service with `curl`:
```
    Upload:
    curl -F 'img=@/Users/ykryvun/Documents/3.jpg' 'http://localhost:8022/api/v1/upload'
    Upload response:
    {"id":"ad76d9e0-7c40-4e21-ba93-eb0c33689e2a"}
    Download:
    curl -X GET 'http://localhost:8022/api/v1/download/ad76d9e0-7c40-4e21-ba93-eb0c33689e2a?zoom=1&left=0&top=0&right=200&bottom=200'
```


#### Docker
1. Build docker image: `make docker-build`.
1. Run docker image with help of `docker-compose`: `make docker-run`.
1. Open swagger specification: [http://localhost:8082/api/v1/doc](http://localhost:8082/api/v1/doc)
1. Upload and download files.
1. Examples how to use service with `curl`:
```
    Upload:
    curl -F 'img=@/Users/ykryvun/Documents/3.jpg' http://localhost:8082/api/v1/upload
    Upload response:
    {"id":"ad76d9e0-7c40-4e21-ba93-eb0c33689e2a"}
    Download:
    curl -X GET 'http://localhost:8082/api/v1/download/ad76d9e0-7c40-4e21-ba93-eb0c33689e2a?zoom=1&left=0&top=0&right=200&bottom=200'
```


### Development
1. Create new virtual environment with python 3.7: `make env`.
1. Run server: `make run`.
1. Swagger UI: [http://localhost:8881/api/v1/doc](http://localhost:8881/api/v1/doc).
1. Run `make` to check the full list of commands.
1. Run tests: `make test`.

### CI/CD
Service uses [Drone.io](https://cloud.drone.io/ukrvassabi/svc-img-processing).