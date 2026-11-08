FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend ./backend
RUN useradd --create-home portal && mkdir /data && chown portal:portal /data
USER portal
ENV DATABASE_URL=sqlite:////data/portal.db
EXPOSE 8000
CMD ["sh", "-c", "python -m backend.init_db && exec uvicorn backend.main:app --host 0.0.0.0 --port 8000"]
