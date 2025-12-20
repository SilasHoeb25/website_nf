#BUILD THE IMAGE:                   docker build -t <image_name>
#START A CONTAINER FROM IMAGE:      docker run -d --<container_name> -p8000:8000 <image_name>
#START WITH VOLUME FOR DEV:         docker run -d --name <docker_container> -v .:/app -p 8000:8000 <image_name>
#CLEAR DOCKER:                      docker system prune
#EXECUTE COMMAND IN A CONTAINER:    docker exec -it <container_name> <command>

#python base image
FROM python:3.12-slim-bookworm

#Prevent Python from creating pycache in container
ENV PYTHONDONTWRITEBYTECODE=1
#Enable Python output buffering 
ENV PYTHONBUFFERED=1

#Workingdirectory in the container
WORKDIR /app

#Copy app dependencies into container
COPY requirements.txt .

#install and upgrade pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

 #Copy the whole directory into container
COPY . .

EXPOSE 8000

# commands to start server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]