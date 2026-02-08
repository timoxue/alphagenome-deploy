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
    python3-pip \
    && rm -rf /var/lib/apt/lists/* || true

# Create system users for JupyterHub
# These users will be able to login
# We create them without home dirs first, then create proper structure
RUN for user in admin user1 user2 user3 user4 user5; do \
      useradd -s /bin/bash $user && \
      mkdir -p /home/$user && \
      mkdir -p /home/$user/work/notebooks && \
      mkdir -p /home/$user/work/results && \
      mkdir -p /home/$user/work/data && \
      mkdir -p /home/$user/work/figures && \
      mkdir -p /home/$user/work/exports && \
      chown -R $user:$user /home/$user; \
    done

# Install Python packages globally (will be available to all users)
RUN pip3 install --no-cache-dir \
    alphagenome \
    jupyterlab \
    matplotlib \
    seaborn \
    pandas \
    biopython \
    tqdm \
    openpyxl \
    xlsxwriter

# Copy custom tools library - create proper package structure
RUN mkdir -p /opt/alphagenome_packages
COPY alphagenome_tools /opt/alphagenome_packages/alphagenome_tools

# Make tools available via environment variable (will be set in jupyterhub_config.py)
ENV PYTHONPATH="/opt/alphagenome_packages:$PYTHONPATH"

# Copy example notebooks
COPY notebooks /shared/notebooks

# Create data directories structure
RUN mkdir -p /shared/data/reference /shared/data/examples /shared/teamwork

# Set proper permissions
RUN chmod -R a+rx /shared

# Expose JupyterHub port
EXPOSE 8000

# Start JupyterHub
CMD ["jupyterhub", "--config", "/etc/jupyterhub/jupyterhub_config.py"]
