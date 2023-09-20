# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /flaskapp
WORKDIR /myapp

# Copy flaskapp directory contents into the container at /flaskapp
COPY myapp /myapp

# Install needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 9000 available to the world outside this container
EXPOSE 9000

CMD ["main.py"]
# Run main.py when the container launches
ENTRYPOINT ["python3"]
