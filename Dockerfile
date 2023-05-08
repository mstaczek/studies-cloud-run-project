# Python image to use.
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# copy the requirements file used for dependencies
COPY requirements.txt .

RUN apt-get update -y
RUN apt-get install gcc g++ python3-dev -y
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY download_stable_diffusion.py download_stable_diffusion.py

# Download stable diffusion 1.5
RUN python download_stable_diffusion.py

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Run app.py when the container launches
ENTRYPOINT ["python", "app.py"]
