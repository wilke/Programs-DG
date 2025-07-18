FROM python:3.9-slim

# Metadata and provenance information
LABEL maintainer="Andreas Wilke and Claude"
LABEL org.opencontainers.image.title="Bioinformatics Programs Suite"
LABEL org.opencontainers.image.description="Complete bioinformatics toolkit for SARS-CoV-2 sequence analysis and viral surveillance"
LABEL org.opencontainers.image.version="1.2.0"
LABEL org.opencontainers.image.created="2025-07-16"
LABEL org.opencontainers.image.authors="Original code by various authors, Dockerfile by Andreas Wilke and Claude"
LABEL org.opencontainers.image.url="https://github.com/wilke/bioinformatics-programs"
LABEL org.opencontainers.image.vendor="Bioinformatics Programs Project"
LABEL org.opencontainers.image.licenses="GPL-3.0"
LABEL org.opencontainers.image.base.name="python:3.9-slim"

# Build arguments for provenance
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION=1.2.0

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
    # Additional bioinformatics tools dependencies
    curl \
    wget \
    unzip \
    screen \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Copy Cryptic Screening scripts to PATH instead of installing via setup.py
RUN if [ -d Cryptic_Screening ]; then \
        cp Cryptic_Screening/*.py /usr/local/bin/ && \
        chmod +x /usr/local/bin/NTSeqScreenMP.py /usr/local/bin/PMScreenMP.py /usr/local/bin/WinnowScreens.py; \
    fi

# Install cryptic-screen CLI
RUN if [ -f cryptic-screen ]; then \
        cp cryptic-screen /usr/local/bin/ && \
        chmod +x /usr/local/bin/cryptic-screen; \
    fi && \
    if [ -d lib/cryptic_screening ]; then \
        cp -r lib /usr/local/lib/python3.9/site-packages/; \
    fi

# Make all Python scripts executable
RUN find . -name "*.py" -type f -exec chmod +x {} \; && \
    find . -name "*.sh" -type f -exec chmod +x {} \;

# Create directories for common workflows
RUN mkdir -p /work /data /results && \
    chmod 755 /work /data /results

# Create a non-root user
RUN useradd -m -u 1000 biouser && \
    chown -R biouser:biouser /work /data /results /app

USER biouser

# Set working directory for user
WORKDIR /work

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/app:$PATH"

# Default command - show available tools
CMD ["python", "-c", "import os; print('Bioinformatics Programs Suite v1.2.0\\n'); \
print('NEW: cryptic-screen CLI is now available!\\n'); \
print('Try: cryptic-screen --help\\n'); \
print('Available Python scripts:'); \
[print(f'  - {f}') for f in sorted(os.listdir('/app')) if f.endswith('.py')]; \
print('\\nAvailable workflows:'); \
[print(f'  - {f}') for f in sorted(os.listdir('/app')) if f.endswith('.sh')]; \
print('\\nCryptic Screening tools:'); \
print('  - cryptic-screen (NEW CLI interface)'); \
print('  - NTSeqScreenMP.py, PMScreenMP.py, WinnowScreens.py (legacy)'); \
print('\\nAll scripts are in PATH and can be executed directly.')"]