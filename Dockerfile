FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app

CMD ["python", "gradio_app.py"]