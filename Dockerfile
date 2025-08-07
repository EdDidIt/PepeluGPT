# Multi-stage build for PepeluGPT
FROM python:3.11-slim as builder

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Poetry configuration and install dependencies
COPY pyproject.toml poetry.lock* ./
RUN pip install --no-cache-dir --user poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Production stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    # For PDF processing
    libmupdf-dev \
    # For document parsing
    libxml2-dev \
    libxslt1-dev \
    # For Excel files
    libpng-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash pepelu

WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /root/.local /home/pepelu/.local

# Copy application code
COPY --chown=pepelu:pepelu . .

# Create necessary directories with proper permissions
RUN mkdir -p cyber_vector_db cyber_documents config logs \
    && chown -R pepelu:pepelu /app

# Switch to non-root user
USER pepelu

# Add local bin to PATH
ENV PATH=/home/pepelu/.local/bin:$PATH

# Expose port for API interface
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import core.engine; print('Health check passed')" || exit 1

# Default command
CMD ["python", "main.py", "--config", "config/default.yaml"]
