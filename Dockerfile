FROM python:3.12

WORKDIR /app
COPY . . 

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv pip install --system -r pyproject.toml


ENV PORT=8080

CMD ["python", "app.py"]
