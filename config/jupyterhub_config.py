"""
JupyterHub configuration for AlphaGenome deployment
"""

import os
import sys

# =============================================================================
# Basic Configuration
# =============================================================================

# JupyterHub base URL
c.JupyterHub.base_url = '/'

# Bind to all network interfaces (allows external access)
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000

# Set the proxy to use a subpath if needed
c.JupyterHub.bind_url = 'http://0.0.0.0:8000'

# =============================================================================
# Authentication
# =============================================================================

# Use PAM authentication (Linux system users)
# This is suitable for small teams on internal servers
c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'

# Alternative: Simple local authentication (uncomment to use)
# c.JupyterHub.authenticator_class = 'jupyterhub.auth.SimpleLocalAuthenticator'

# Set admin users (comma-separated list)
# These users can admin the JupyterHub server
c.JupyterHub.admin_users = {
    'admin',
    'jovyan',
}

# =============================================================================
# Spawner Configuration
# =============================================================================

# Use DockerSpawner for containerized user environments
c.JupyterHub.spawner_class = 'jupyterhub.spawner.LocalProcessSpawner'

# Set default URL for user servers (opens JupyterLab by default)
c.Spawner.default_url = '/lab'

# Set the working directory for user notebooks
c.Spawner.notebook_dir = '~/work'

# Environment variables to pass to user notebooks
c.Spawner.environment = {
    'ALPHAGENOME_API_KEY': os.environ.get('ALPHAGENOME_API_KEY', ''),
    'SHARED_DATA_PATH': '/shared/data',
    'SHARED_TOOLS_PATH': '/shared/tools',
}

# Resource limits for each user container
c.Spawner.mem_limit = '2G'
c.Spawner.cpu_limit = 1.0

# Automatically start user servers when they log in
c.Spawner.start_timeout = 300

# Allow users to create named servers (optional)
c.Spawner.allow_named_servers = True

# =============================================================================
# Services
# =============================================================================

# You can add services here if needed
# c.JupyterHub.services = [
#     {
#         'name': 'cull-idle',
#         'admin': True,
#         'command': [sys.executable, '-m', 'jupyterhub_idle_culler',
#                    '--timeout=3600'],
#     }
# ]

# =============================================================================
# Security
# =============================================================================

# Generate a secure cookie secret (auto-generated on first run)
# For production, set this explicitly in environment variable
c.JupyterHub.cookie_secret_file = '/srv/jupyterhub/jupyterhub_cookie_secret'

# Allow self-signed certificates for internal deployments
c.JupyterHub.ssl_enabled = False

# =============================================================================
# Logging
# =============================================================================

# Log level
c.JupyterHub.log_level = 'INFO'

# Log to file
c.JupyterHub.extra_log_file = '/var/log/jupyterhub.log'

# =============================================================================
# Custom Configuration
# =============================================================================

# Add custom logo (optional)
# c.JupyterHub.logo_file = '/shared/logo.png'

# Custom template variables (optional)
c.JupyterHub.template_vars = {
    'prefix': 'AlphaGenome',
    'organization': 'Company R&D',
}

# =============================================================================
# Performance tuning
# =============================================================================

# Clean up servers after logout (optional)
c.JupyterHub.cleanup_servers = False

# Cleanup proxy on exit
c.JupyterHub.cleanup_proxy = True

# Maximum number of servers per user
c.Spawner.active_server_limit = 5
