"""
JupyterHub configuration for AlphaGenome deployment
Multi-user setup with simple authentication for 2-5 users
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
# Authentication - Simple Dictionary Authenticator
# =============================================================================

from jupyterhub.auth import Authenticator

# Create a simple password-based authentication
class DictionaryAuthenticator(Authenticator):
    """
    Simple dictionary-based authenticator for small teams.
    Users and passwords are defined below.
    """

    # Define users and passwords here
    # Format: 'username': 'password'
    users = {
        'admin': 'admin123',      # Administrator
        'user1': 'user123',       # Team member 1
        'user2': 'user123',       # Team member 2
        'user3': 'user123',       # Team member 3
        'user4': 'user123',       # Team member 4
        'user5': 'user123',       # Team member 5
    }

    async def authenticate(self, handler, data):
        """Authenticate user with username and password"""
        username = data['username']
        password = data['password']

        if username in self.users and self.users[username] == password:
            return username
        return None

# Use our custom authenticator
c.JupyterHub.authenticator_class = DictionaryAuthenticator

# Set admin users (these users can admin the JupyterHub server)
c.JupyterHub.admin_users = {
    'admin',
}

# =============================================================================
# Spawner Configuration
# =============================================================================

# Use LocalProcessSpawner (runs servers as local processes)
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
    'PYTHONPATH': '/opt/alphagenome_packages:/usr/lib/python3/dist-packages',
}

# Resource limits for each user container
c.Spawner.mem_limit = '2G'
c.Spawner.cpu_limit = 1.0

# Automatically start user servers when they log in
c.Spawner.start_timeout = 300

# =============================================================================
# User Server Configuration
# =============================================================================

# Set default working directory for all users
c.Spawner.notebook_dir = '~/work'

# Create user directories on first spawn
def make_userdir(spawner):
    """Create user home directory structure on first spawn"""
    import os
    import subprocess

    user = spawner.user.name
    home_dir = f'/home/{user}' if os.path.exists(f'/home/{user}') else f'/tmp/{user}'

    # Create work directory structure
    work_dir = os.path.join(home_dir, 'work')
    for subdir in ['notebooks', 'results', 'data', 'figures', 'exports']:
        os.makedirs(os.path.join(work_dir, subdir), exist_ok=True)

# Hook to create directories before spawn
c.Spawner.pre_spawn_hook = make_userdir

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

# =============================================================================
# User Management
# =============================================================================

# Admin users can manage the JupyterHub server
c.JupyterHub.admin_users = {
    'admin',
}

# Disable user self-registration (users must be in the dictionary)
# Only users defined in DictionaryAuthenticator.users can log in
