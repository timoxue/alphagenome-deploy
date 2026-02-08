# AlphaGenome JupyterHub Deployment

A complete deployment solution for running AlphaGenome (Google DeepMind's genomic prediction model) in a corporate research environment using JupyterHub.

## Overview

This project provides a Docker-based JupyterHub deployment pre-configured with:
- AlphaGenome client library and API integration
- Example notebooks for common analysis workflows
- Custom Python tools for batch processing and visualization
- Multi-user support for research teams
- Production-ready deployment configuration

## Features

- **🚀 Quick Start**: Pre-built Docker images with all dependencies
- **👥 Multi-User**: JupyterHub authentication for 2-5 users (scalable)
- **📚 Example Notebooks**: 5 comprehensive tutorials covering:
  - Quick start guide
  - Variant effect analysis
  - Batch processing
  - Advanced visualization
  - Custom analysis template
- **🛠️ Custom Tools**: Helper library for batch processing, data export, and visualization
- **🔒 Secure**: API key management via environment variables
- **📦 Easy Deployment**: Docker Compose for simple setup

## Project Structure

```
alphagenome-deploy/
├── docker/
│   ├── Dockerfile              # JupyterHub image definition
│   └── docker-compose.yml      # Service orchestration
├── notebooks/                  # Example notebooks (5 tutorials)
│   ├── 01_quickstart.ipynb
│   ├── 02_variant_analysis.ipynb
│   ├── 03_batch_analysis.ipynb
│   ├── 04_visualization.ipynb
│   └── 05_custom_analysis.ipynb
├── alphagenome_tools/         # Custom helper library
│   ├── __init__.py
│   ├── helpers.py             # Batch processing utilities
│   └── visualization.py       # Visualization helpers
├── config/
│   └── jupyterhub_config.py   # JupyterHub configuration
├── data/
│   ├── reference/             # Reference genome data
│   └── examples/              # Example datasets
├── .env.example               # API key template
├── .gitignore
└── README.md
```

## Quick Start

### Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- AlphaGenome API key (get from https://alphagenome.google/)
- At least 8GB RAM available for Docker

### 1. Clone or Download

```bash
git clone <repository-url>
cd alphagenome-deploy
```

### 2. Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
# On Windows: notepad .env
# On Mac/Linux: nano .env
```

Edit `.env`:
```
ALPHAGENOME_API_KEY=your_actual_api_key_here
```

### 3. Start the Service

```bash
# Build and start
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 4. Access JupyterHub

- Open your browser and go to: http://localhost:8000
- Login with your system username/password
- Start exploring the example notebooks in `/shared/notebooks/`

## Usage

### First Time: Quick Start Tutorial

1. Open `01_quickstart.ipynb` from `/shared/notebooks/`
2. Run the cells sequentially
3. Learn how to:
   - Connect to AlphaGenome API
   - Define genomic intervals
   - Run sequence predictions
   - Visualize results

### Analyze Genetic Variants

Use `02_variant_analysis.ipynb` to:
- Define variants (SNPs, insertions, deletions)
- Compare reference vs alternate alleles
- Calculate effect scores
- Generate comparison visualizations

### Batch Processing

Use `03_batch_analysis.ipynb` to:
- Load multiple variants from CSV
- Run batch predictions with progress tracking
- Monitor API quota
- Export aggregated results

### Advanced Visualization

Use `04_visualization.ipynb` to:
- Create publication-quality figures
- Build multi-panel visualizations
- Apply custom styling and annotations
- Export to PNG/PDF/SVG

### Custom Analysis

Copy `05_custom_analysis.ipynb` to your workspace (`~/work/`) to:
- Start your own analysis
- Use the provided template structure
- Build on the helper functions

## Custom Tools

The `alphagenome_tools` package provides:

### `helpers.py`
- `batch_predict_variants()` - Batch variant predictions
- `batch_predict_sequences()` - Batch sequence predictions
- `load_variants_from_csv()` - Load variants from CSV
- `load_intervals_from_csv()` - Load intervals from CSV
- `save_results()` - Save results in multiple formats
- `export_to_csv()` / `export_to_excel()` - Data export
- `monitor_api_quota()` - Track API usage

### `visualization.py`
- `quick_plot()` - Quick preview plots
- `plot_variant_comparison()` - Side-by-side variant comparison
- `plot_batch_summary()` - Batch result summaries
- `plot_expression_heatmap()` - Gene expression heatmaps
- `plot_tracks_overlaid()` - Overlaid genomic tracks
- `create_multi_panel_figure()` - Multi-panel publication figures

## Deployment to Production Server

### Local Development (Windows 11)

1. Build and test locally:
   ```bash
   docker-compose up --build
   ```

2. Test all notebooks and verify functionality

3. Export Docker image:
   ```bash
   docker save alphagenome-jupyterhub:latest > alphagenome-jupyterhub.tar
   ```

### Server Deployment (Linux)

1. Transfer files to server:
   ```bash
   scp alphagenome-jupyterhub.tar user@server:/opt/
   scp -r .env config/ user@server:/opt/alphagenome-deploy/
   ```

2. On the server:
   ```bash
   # Install Docker
   sudo apt-get update
   sudo apt-get install -y docker.io docker-compose
   sudo systemctl start docker

   # Load image
   docker load < /opt/alphagenome-jupyterhub.tar

   # Start service
   cd /opt/alphagenome-deploy
   docker-compose up -d
   ```

3. Configure firewall:
   ```bash
   sudo ufw allow 8000/tcp
   ```

4. Access at: `http://server-ip:8000`

## Configuration

### JupyterHub

Edit `config/jupyterhub_config.py`:
- Authentication method (PAM, LDAP, OAuth)
- User permissions and admin users
- Resource limits (CPU, memory)
- Spawner settings

### Docker Resources

Edit `docker-compose.yml`:
- CPU and memory limits
- Port mappings
- Volume mounts
- Network settings

### API Quota

AlphaGenome free tier limits:
- Suitable for small to medium analyses
- ~1M predictions (check current limits)
- Monitor usage with: `monitor_api_quota()`

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs -f

# Rebuild image
docker-compose build --no-cache
docker-compose up -d
```

### API key not working
- Verify `.env` file exists and contains valid key
- Check API key hasn't expired
- Ensure `ALPHAGENOME_API_KEY` is set correctly

### Out of memory
- Increase memory limit in `docker-compose.yml`
- Reduce number of concurrent users
- Process smaller batches

### Can't access from network
- Check firewall settings
- Verify port 8000 is open
- Ensure JupyterHub is listening on `0.0.0.0`

## Maintenance

### Backup User Data

```bash
# Backup user volumes
docker run --rm \
  -v alphagenome-deploy_jupyterhub-user-data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/user-data-$(date +%Y%m%d).tar.gz /data
```

### Update AlphaGenome

```bash
# Pull latest changes
git pull

# Rebuild image
docker-compose build --no-cache

# Restart service
docker-compose up -d
```

### Monitor Resources

```bash
# Check container stats
docker stats

# View logs
docker-compose logs -f jupyterhub
```

## Security Considerations

- **Never commit `.env`** to version control (it contains API keys)
- Use strong passwords for user accounts
- Restrict network access (firewall, internal network only)
- Regularly update Docker images for security patches
- Consider HTTPS for production deployments
- Monitor API usage for unusual activity

## Contributing

To add new features or fix issues:

1. Test changes locally first
2. Update relevant documentation
3. Ensure all notebooks still work
4. Submit pull request with description

## License

This deployment configuration is provided as-is for internal corporate use.

AlphaGenome API is subject to Google's Terms of Use:
- Free for non-commercial use
- Commercial licensing available
- See: https://github.com/google-deepmind/alphagenome

## Support

For issues related to:
- **This deployment**: Check the troubleshooting section or contact your IT team
- **AlphaGenome API**: https://github.com/google-deepmind/alphagenome/issues
- **JupyterHub**: https://discourse.jupyter.org/

## Acknowledgments

- AlphaGenome by Google DeepMind
- JupyterHub by Project Jupyter
- Docker by Docker Inc.

---

**Version**: 1.0.0
**Last Updated**: 2025-02-08
**Maintained by**: Your Research IT Team
