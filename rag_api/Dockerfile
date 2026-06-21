FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY rag_api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY assets/local_pdf_rag_index.json /app/assets/local_pdf_rag_index.json
COPY rag_api /app/rag_api

WORKDIR /app/rag_api
ENV RAG_INDEX_PATH=/app/assets/local_pdf_rag_index.json

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
