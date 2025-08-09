FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-fonts-recommended \
    texlive-latex-extra \
    wget \
    xfonts-75dpi \
    xfonts-base \
    fontconfig \
    libxrender1 \
    libxtst6 \
    libxext6 \
    libfontconfig1 \
    libfreetype6 \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/Your1000Resume

COPY Your1000Resume/ /app/Your1000Resume/

RUN pip install --no-cache-dir -r requirements.txt

# Add a non-root user
RUN useradd -m appuser
# Create and assign permissions to uploads and resumes folders
RUN mkdir -p /app/Your1000Resume/uploads /app/Your1000Resume/resumes \
    && chown -R appuser:appuser /app/Your1000Resume

USER appuser

EXPOSE 5000

ENV PYTHONPATH=/app

CMD ["python", "app.py"]