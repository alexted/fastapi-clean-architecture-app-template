# Pull official base image
FROM python:{{ cookiecutter.app_lang_version }}-slim

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy project files
COPY my-example .

RUN pip install -U poetry && poetry install

# Make entrypoint.sh executable
RUN chmod +x ./entrypoint.sh

# Publish network port
EXPOSE 5000

# Execute script to start the application web server
ENTRYPOINT ["./entrypoint.sh"]

