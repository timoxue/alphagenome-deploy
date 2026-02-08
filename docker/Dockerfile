# AlphaGenome JupyterHub Docker Image
# Based on official JupyterHub image with AlphaGenome client and tools

FROM jupyterhub/jupyterhub:4.1.5

# Metadata
LABEL maintainer="your-email@company.com"
LABEL description="JupyterHub with AlphaGenome for genomics research"

# Switch to root to install system dependencies
USER root

# Install system packages
RUN apt-get update && apt-get install -y \
    git \
    vim \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Switch back to jovyan user for Python packages
USER jovyan

# Install Python packages
RUN pip install --no-cache-dir \
    alphagenome \
    matplotlib \
    seaborn \
    pandas \
    biopython \
    tqdm \
    openpyxl \
    xlsxwriter \
    ipywidgets && \
    jupyter labextension install @jupyter-widgets/jupyterlab-manager

# Copy custom tools library
COPY alphagenome_tools /opt/alphagenome_tools

# Install the tools package (make it importable)
RUN cd /opt/alphagenome_tools && \
    pip install -e . || \
    (echo "import sys; sys.path.insert(0, '/opt/alphagenome_tools')" >> \
    /opt/conda/lib/python3.*/*/site-packages/usercustomize.py 2>/dev/null || \
    mkdir -p /opt/conda/lib/python3.11/site-packages && \
    echo "import sys; sys.path.insert(0, '/opt/alphagenome_tools')" >> \
    /opt/conda/lib/python3.11/site-packages/usercustomize.py)

# Copy example notebooks
COPY notebooks /shared/notebooks

# Create data directories structure
RUN mkdir -p /shared/data/reference /shared/data/examples /shared/teamwork

# Set working directory
WORKDIR /home/jovyan/work

# Expose JupyterHub port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/hub/api/ || exit 1

# Start JupyterHub
CMD ["jupyterhub", "-C", "/etc/jupyterhub/jupyterhub_config.py"]
