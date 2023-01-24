# set base image python:3.8-slim-buster
FROM python:3.8-slim-buster

# set working directory as app
WORKDIR /api_app

# copy requirements.txt file from local (source) to file structure of container (destination) 
COPY /app/requirements.txt requirements.txt

# Install the requirements specified in file using RUN
RUN pip3 install -r requirements.txt

# copy all items in current local directory (source) to current container directory (destination)
COPY . /api_app/

#Expose the container's port 5001 so that our API client route the request to the container.
EXPOSE 5001

# command to run when image is executed inside a container
CMD [ "python3", "main.py" ]
