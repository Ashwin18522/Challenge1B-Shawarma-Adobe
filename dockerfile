FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app
COPY requirements.txt .
COPY en_core_web_sm-3.6.0-py3-none-any.whl .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install ./en_core_web_sm-3.6.0-py3-none-any.whl

COPY ./src ./src
COPY ./models ./models
COPY main.py .

CMD ["python", "main.py"]
