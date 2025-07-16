FROM python:3.9-slim

# Metadata and provenance information
LABEL maintainer="Andreas Wilke and Claude"
LABEL org.opencontainers.image.title="Cryptic Screening"
LABEL org.opencontainers.image.description="Files used to screen SRA samples for cryptic signals"
LABEL org.opencontainers.image.version="1.1.0"
LABEL org.opencontainers.image.created="2025-07-09"
LABEL org.opencontainers.image.authors="Original code by degregory, Dockerfile by Andreas Wilke and Claude"
LABEL org.opencontainers.image.url="https://github.com/cryptic-screening/cryptic-screening"
LABEL org.opencontainers.image.documentation="https://github.com/cryptic-screening/cryptic-screening/blob/main/readme.md"
LABEL org.opencontainers.image.source="https://github.com/cryptic-screening/cryptic-screening"
LABEL org.opencontainers.image.vendor="Cryptic Screening Project"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.base.name="python:3.9-slim"
LABEL org.opencontainers.image.base.digest="sha256:c2a0feb07dedbf91498883c2f8e1e5201e95c91d413e21c3bea780c8aad8e6a7"

# Build arguments for provenance
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION=1.1.0

# Additional metadata using build args
LABEL org.opencontainers.image.revision=${VCS_REF}
LABEL org.opencontainers.image.created=${BUILD_DATE}
LABEL org.opencontainers.image.version=${VERSION}

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    libbz2-dev \
    liblzma-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    zlib1g-dev \
    screen \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy main project requirements and install Python dependencies
COPY ../requirements.txt ./main-requirements.txt
COPY requirements.txt ./cryptic-requirements.txt
RUN pip install --no-cache-dir -r main-requirements.txt && \
    pip install --no-cache-dir -r cryptic-requirements.txt

# Copy all application files
COPY . .
COPY ../ ./main-project/

# Install the application and make Python scripts executable
RUN pip install -e . && \
    find ./main-project -name "*.py" -type f -exec chmod +x {} \; && \
    find . -name "*.py" -type f -exec chmod +x {} \;

# Create a non-root user and writable work directory
RUN useradd -m -u 1000 screening && \
    mkdir -p /work && \
    chown screening:screening /work

USER screening

# Set writable work directory
WORKDIR /work

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Add Python scripts to PATH
ENV PATH="/app/main-project:$PATH"

# Default command
CMD ["python", "-c", "print('Cryptic Screening tools available: NTSeqScreenMP.py, PMScreenMP.py, WinnowScreens.py')\\nMain project Python scripts are executable and in PATH']"]