# Quick Start Guide - AlphaGenome JupyterHub

This guide will get you up and running with AlphaGenome in 10 minutes.

## Step 1: Prepare Your Environment

### Check Docker Installation

```bash
docker --version
docker-compose --version
```

If not installed:
- **Windows**: Download Docker Desktop from https://www.docker.com/products/docker-desktop
- **Mac**: Download Docker Desktop for Mac
- **Linux**: Install via package manager

### Get Your AlphaGenome API Key

1. Visit: https://alphagenome.google/
2. Sign in with your Google account
3. Request an API key (free for non-commercial use)
4. Copy your API key

## Step 2: Set Up the Project

### 2.1 Get the Code

```bash
# Clone or download the project
cd alphagenome-deploy
```

### 2.2 Configure API Key

```bash
# Copy the template
cp .env.example .env

# Edit .env file
# On Windows:
notepad .env

# On Mac/Linux:
nano .env
```

Add your API key:
```
ALPHAGENOME_API_KEY=your_actual_api_key_here
```

**IMPORTANT**: Never share or commit your `.env` file!

## Step 3: Start JupyterHub

```bash
# Build and start (first run takes 5-10 minutes)
docker-compose up --build
```

You'll see build progress. Wait until you see:
```
jupyterhub-1  | 200 GET /hub/api/...
```

JupyterHub is now running!

## Step 4: Access JupyterHub

1. Open your browser
2. Go to: http://localhost:8000
3. Login with your system username and password

## Step 5: Run Your First Analysis

### Open Quick Start Notebook

1. In JupyterLab, navigate to `/shared/notebooks/`
2. Open `01_quickstart.ipynb`
3. Run the cells one by one (Shift+Enter or click "Run")

### What You'll Do

✓ Connect to AlphaGenome API
✓ Define a genomic region
✓ Run sequence prediction
✓ Visualize results
✓ Save to your workspace

## Step 6: Explore More Notebooks

### Variant Analysis
**File**: `02_variant_analysis.ipynb`
- Analyze genetic variants
- Compare reference vs alternate alleles
- Calculate effect scores

### Batch Processing
**File**: `03_batch_analysis.ipynb`
- Process multiple variants at once
- Load from CSV files
- Export aggregated results

### Advanced Visualization
**File**: `04_visualization.ipynb`
- Create publication-quality figures
- Multi-panel visualizations
- Custom styling

### Custom Analysis
**File**: `05_custom_analysis.ipynb`
- Template for your own analyses
- Copy to your workspace
- Modify as needed

## Common Tasks

### Save Your Work

All work is automatically saved in:
- `~/work/` - Your personal workspace
- `~/work/results/` - Analysis results

### Upload Your Own Data

1. In JupyterLab, click the "Upload Files" button (↑ icon)
2. Select your CSV/VCF/BED files
3. Files appear in your file browser

### Stop JupyterHub

```bash
# Press Ctrl+C in the terminal
# Or run in another terminal:
docker-compose down
```

### Restart JupyterHub

```bash
docker-compose up -d
```

## Tips for Success

### Start Small
- Begin with the quick start notebook
- Test with small datasets first
- Check your API quota regularly

### Monitor API Usage

```python
from alphagenome_tools import monitor_api_quota
print(monitor_api_quota())
```

### Save Frequently
- Results are saved in `~/work/results/`
- Use descriptive filenames
- Export to CSV/Excel for sharing

### Get Help

1. Check the **README.md** for detailed documentation
2. Review example notebooks
3. Check AlphaGenome docs: https://github.com/google-deepmind/alphagenome
4. Ask your team for help

## Next Steps

1. ✅ Complete the quick start tutorial
2. ✅ Try the variant analysis notebook
3. ✅ Experiment with batch processing
4. ✅ Create your own analysis from the template

## Troubleshooting

### "Connection Refused" Error
- Ensure Docker is running
- Check that `docker-compose up` completed successfully
- Try accessing http://localhost:8000 again

### "API Key Not Found" Error
- Verify `.env` file exists in project root
- Check that `ALPHAGENOME_API_KEY` is set correctly
- No extra spaces or quotes around the key

### Out of Memory
- Close unused browser tabs
- Reduce the number of simultaneous users
- Increase Docker memory limit in Docker Desktop settings

### Container Won't Start
```bash
# Check logs
docker-compose logs

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## What's Where?

| Location | Contents |
|----------|----------|
| `/shared/notebooks/` | Example tutorials (read-only) |
| `/shared/data/` | Reference and example data (read-only) |
| `/shared/tools/` | Helper library (read-only) |
| `~/work/` | Your personal workspace (read-write) |
| `~/work/results/` | Your analysis results (read-write) |

## Keyboard Shortcuts in JupyterLab

- `Shift+Enter` - Run cell and move to next
- `Ctrl+Enter` - Run cell and stay
- `A` - Insert cell above (in command mode)
- `B` - Insert cell below (in command mode)
- `DD` - Delete cell (in command mode)
- `M` - Change to Markdown cell
- `Y` - Change to code cell

## Resources

- **Full Documentation**: See README.md
- **AlphaGenome API**: https://github.com/google-deepmind/alphagenome
- **JupyterLab**: https://jupyterlab.readthedocs.io/
- **Python**: https://docs.python.org/3/

---

**Ready to analyze!** 🚀

You now have everything you need to start using AlphaGenome. If you need more detailed information, refer to the main README.md file.

Happy analyzing! 🧬
