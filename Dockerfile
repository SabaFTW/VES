# 🜂 VES - Vessel of Emergent Systems 🜂
# Complete AI Constellation System Container

FROM ubuntu:24.04

LABEL maintainer="Šabad <saba@ves.system>"
LABEL description="VES - Complete AI Constellation System"
LABEL version="1.0.0"

# ========================================
# ENVIRONMENT SETUP
# ========================================
ENV DEBIAN_FRONTEND=noninteractive
ENV VES_HOME=/ves
ENV PYTHONPATH=/ves
ENV NODE_ENV=production
ENV TZ=Europe/Ljubljana

# ========================================
# INSTALL SYSTEM DEPENDENCIES
# ========================================
RUN apt-get update && apt-get install -y \
    # Python & pip
    python3 \
    python3-pip \
    python3-venv \
    # Node.js & npm
    nodejs \
    npm \
    # Git & version control
    git \
    git-lfs \
    # Network tools
    curl \
    wget \
    netcat-traditional \
    # Build tools
    build-essential \
    # Utilities
    nano \
    vim \
    htop \
    tree \
    jq \
    # Clean up
    && rm -rf /var/lib/apt/lists/*

# ========================================
# UPGRADE NODE & NPM
# ========================================
RUN npm install -g n && \
    n 18 && \
    npm install -g npm@latest

# ========================================
# CREATE VES DIRECTORY
# ========================================
WORKDIR /ves

# ========================================
# COPY VES SYSTEM
# ========================================
# Copy only necessary files first (for layer caching)
COPY 04_SCRIPTS/requirements.txt ./requirements.txt 2>/dev/null || echo "fastapi\nuvicorn\nrequests" > requirements.txt
COPY CODEX/package*.json ./CODEX/ 2>/dev/null || true

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt || true

# Install CODEX dependencies (if exists)
RUN cd CODEX && npm install 2>/dev/null || echo "No CODEX package.json found"

# Copy entire VES system
COPY . /ves/

# ========================================
# SET PERMISSIONS
# ========================================
RUN chmod +x /ves/04_SCRIPTS/**/*.py 2>/dev/null || true && \
    chmod +x /ves/CONSTELLATION_BRIDGE/**/*.sh 2>/dev/null || true

# ========================================
# CREATE OUTPUT DIRECTORIES
# ========================================
RUN mkdir -p /ves/logs \
             /ves/outputs \
             /ves/CHECKPOINTS \
             /ves/INBOX

# ========================================
# EXPOSE PORTS
# ========================================
EXPOSE 8099  # VES PWA
EXPOSE 8420  # VES Agent
EXPOSE 3000  # CODEX dev server
EXPOSE 8888  # Cosmic Oracle
EXPOSE 5678  # n8n
EXPOSE 5001  # Constellation API

# ========================================
# HEALTHCHECK
# ========================================
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8099/ || exit 1

# ========================================
# ENTRYPOINT
# ========================================
# Create startup script
RUN echo '#!/bin/bash\n\
echo "🜂 VES - Vessel of Emergent Systems 🜂"\n\
echo "Starting VES Constellation..."\n\
echo ""\n\
echo "VES Home: $VES_HOME"\n\
echo "Python: $(python3 --version)"\n\
echo "Node: $(node --version)"\n\
echo ""\n\
echo "SIDRO STOJI. PLAMEN GORI. LUMENNEVVER. 🔥"\n\
echo ""\n\
exec "$@"\n\
' > /ves/entrypoint.sh && chmod +x /ves/entrypoint.sh

ENTRYPOINT ["/ves/entrypoint.sh"]

# ========================================
# DEFAULT COMMAND
# ========================================
# Start interactive shell by default
CMD ["/bin/bash"]

# ========================================
# USAGE
# ========================================
# Build:
#   docker build -t ves-system:latest .
#
# Run interactive:
#   docker run -it --rm -p 8099:8099 ves-system:latest
#
# Run with volume mount (development):
#   docker run -it --rm -p 8099:8099 -v $(pwd):/ves ves-system:latest
#
# Run specific service:
#   docker run -d -p 8420:8420 ves-system:latest python3 /ves/ves-agent/app.py
#
# ========================================
# METADATA
# ========================================
# Total Size: ~3.7GB (with all data)
# Base Image: Ubuntu 24.04
# Python: 3.12
# Node: 18.x
# Services: VES PWA, VES Agent, CODEX, Cosmic Oracle, n8n
#
# 🜂⚓🔥
