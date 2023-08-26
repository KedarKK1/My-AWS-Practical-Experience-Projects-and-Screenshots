# use official python image as base image
FROM python:3.9-buster

# set the working directory in container 
WORKDIR /app

# copy the requirements.txt file in the working directory
COPY requirements.txt .

# install required py packages
RUN pip3 install --no-cache-dir -r requirements.txt

# copy application code to working directory
COPY . .

# set env. var. for flask app 
ENV FLASK_RUN_HOST=0.0.0.0

# expose port on which flask app will run
EXPOSE 5000

# start the flask app when the container is run
CMD ["flask", "run"]