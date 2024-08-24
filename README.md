# py-fast-api

This repository contains a simple FastAPI application packaged as a Docker image.
Run the application locally, then navigate to /docs to use the Swagger for consuming the API.


# 1. Runnig the app locally

- create and activate the virtual environment
``` python -m venv venv ```

- install required packages
``` pip install --upgrade -r requirements.txt ```

- run the application on localhost:8080
``` uvicorn main:app --host 0.0.0.0 --port 8080 --reload ```

# 2. Build and run the app locally from docker image
 
- build the docker image 
``` docker build -t fast-api . ```

- running the docker image 
``` docker run -d -p 8080:80 fast-api ```

# 3. Add docker-compose file and run the application

- create the docker-compose.yaml script
```
services:
    app:
      build: .
      container_name: fast-api
      command: uvicorn main:app --host 0.0.0.0 --port 80 --reload
      ports: 
        - 8080:80
      volumes:
        - .:/app
```

- build the docker compose file
``` docker-compose up --build ```
