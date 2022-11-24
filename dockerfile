FROM python:3.11.0-slim-buster
WORKDIR /app
COPY main.py main.py
COPY test_main.py test_main.py
RUN pip install pytest
CMD ["pytest", "-vv", "."]
