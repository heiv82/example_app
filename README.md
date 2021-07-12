#Web application

## About the project
The goal of the project is to create and run a web application virtualized with Docker.


## Usage:
Make sure you have already installed both Docker and Docker Compose. 

**Start application**

Start the application by running:
```
    docker-compose up
```
from  within your project directory in the terminal. 

**Connect application directly**

You can also access the container directly using:
```
docker exec -it <container id or name> bash
```
**Run the service in the background**

If you want to run services in the background, you can pass the
```-d``` flag to ```docker-compose up```, use:
```
docker-compose up -d
```

**Stop application**

Stop the application, either by running
```
docker-compose down 
```
from withing your project directory in the second terminal, or by hitting ```CTRL+C```
in the original terminal where you started the app.

