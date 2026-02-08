# User Guide - Working with Your Personal Workspace

This guide explains how to work with your personal space in the AlphaGenome JupyterHub platform.

## 📂 Understanding Your Workspace

### Personal Space (Private - Only You)

Each user has a **completely private** workspace:

```
~/work/
├── notebooks/       # Your copied and modified tutorials
├── results/         # Your analysis results
├── data/            # Your uploaded data files
├── figures/         # Your saved plots and visualizations
└── exports/         # Your exported CSV/Excel files
```

**Key Points:**
- 🔒 **Private**: No other users can see or access your `~/work/` directory
- ✍️ **Writable**: You can create, modify, and delete files here
- 💾 **Persistent**: Your work is saved even after you logout

### Shared Resources (Read-Only - Everyone)

All users share access to these resources:

```
/shared/
├── notebooks/       # Tutorial notebooks (read-only)
├── data/            # Reference and example data (read-only)
└── tools/           # Helper library (read-only)
```

**Key Points:**
- 👥 **Shared**: All users can see these files
- 🔒 **Read-only**: No one (including you) can modify these files
- 📚 **Reference**: These are templates and learning materials

---

## 🚀 How to Use This Platform

### Scenario 1: Learning and Exploration (Read-Only)

**Best for**: First-time users, learning the basics

1. Navigate to `/shared/notebooks/` in the file browser
2. Open any tutorial (e.g., `01_quickstart.ipynb`)
3. Run cells to learn (Shift+Enter or click "Run")
4. Results are saved to `~/work/results/`

**Pros:**
- ✅ Always have the original template
- ✅ Can't accidentally break anything
- ✅ Always up-to-date with latest version

**Cons:**
- ❌ Cannot modify the notebook
- ❌ Cannot save your own code changes

### Scenario 2: Experimentation and Customization (Copy & Modify)

**Best for**: Custom analyses, experimentation

1. Navigate to `/shared/notebooks/`
2. Find the notebook you want to use
3. **Right-click** → **Copy**
4. Navigate to `~/work/notebooks/`
5. **Paste** (Ctrl+V)
6. Open the copied notebook and modify as you like

**Pros:**
- ✅ Can modify and experiment freely
- ✅ Keep your own version
- ✅ Original template remains unchanged

**Example:**
```
/shared/notebooks/01_quickstart.ipynb  →  Copy
~/work/notebooks/01_quickstart.ipynb    →  Modify and experiment
```

### Scenario 3: Creating Your Own Analysis

**Best for**: Production analysis, custom workflows

1. Copy `05_custom_analysis.ipynb` to your workspace
2. Rename it (e.g., `my_chr22_analysis.ipynb`)
3. Modify for your specific needs
4. Save results regularly

---

## 📝 Step-by-Step: Copying a Notebook

### Method 1: Using JupyterLab UI (Recommended)

1. **Open the File Browser** (left sidebar)
2. **Navigate to** `/shared/notebooks/`
3. **Right-click** on the notebook you want
4. **Select "Copy"**
5. **Navigate to** `~/work/notebooks/`
6. **Right-click in empty space**
7. **Select "Paste"**

### Method 2: Using Code (Automatic)

Run this in a notebook cell:

```python
# Copy a notebook programmatically
import shutil
from pathlib import Path

src = Path('/shared/notebooks/01_quickstart.ipynb')
dst = Path.home() / 'work' / 'notebooks' / 'my_quickstart.ipynb'

shutil.copy(src, dst)
print(f"✅ Copied to {dst}")
```

---

## 💾 Saving Your Work

### Where Are My Results?

By default, results are saved to:

```
~/work/results/
├── quickstart_20250208_143022/
├── variant_analysis_20250208_150145/
└── batch_analysis_20250208_160230/
```

Each analysis creates a **timestamped directory** to keep results organized.

### Manual Saving

```python
from pathlib import Path

# Save to a specific location
output_dir = Path.home() / 'work' / 'results' / 'my_analysis'
output_dir.mkdir(parents=True, exist_ok=True)

# Save your files here
```

---

## 🔍 Finding Your Files

### In JupyterLab

1. Open **File Browser** (left sidebar)
2. Click the **folder icon** for `~/work/`
3. Navigate through subdirectories

### File Locations

| What | Where |
|------|-------|
| Your notebooks | `~/work/notebooks/` |
| Analysis results | `~/work/results/` |
| Uploaded data | `~/work/data/` |
| Saved figures | `~/work/figures/` |
| Exports (CSV/Excel) | `~/work/exports/` |
| Tutorial templates | `/shared/notebooks/` (read-only) |

---

## 📤 Sharing Results with Team

Since each user's `~/work/` is private, share results by:

### Method 1: Export to CSV/Excel

```python
# Export results
from alphagenome_tools import export_to_csv, export_to_excel
import pandas as pd

# Your results
results_df = pd.DataFrame(...)

# Export to shared location (if configured)
export_to_csv(results_df, '~/work/exports/my_results.csv')
```

Then share the file via:
- Email
- Shared network drive
- Internal messaging
- Git repository

### Method 2: Generate Report

```python
# Convert notebook to HTML
!jupyter nbconvert --to html my_analysis.ipynb

# Share the HTML file
```

### Method 3: Use Shared Teamwork Directory (Optional)

If admin configured `/shared/teamwork/`:

```python
# Save to shared location
shared_dir = Path('/shared/teamwork')
results.to_csv(shared_dir / 'team_results.csv')
```

**Note**: All users can see and modify files here!

---

## 🏗️ Best Practices

### Organizing Your Work

```
~/work/
├── notebooks/
│   ├── 01_quickstart_copy.ipynb        # Copies of tutorials
│   ├── chr22_analysis.ipynb            # Your custom analyses
│   └── batch_processing_v1.ipynb
├── results/
│   ├── chr22_region1/                  # Organize by project
│   ├── chr22_region2/
│   └── batch_analysis_20250208/
├── data/
│   ├── my_variants.csv                 # Your input data
│   ├── custom_regions.bed
│   └── project_data/
├── figures/
│   ├── figure1.png
│   └── publication_figure.pdf
└── exports/
    ├── summary_20250208.xlsx
    └── results.csv
```

### File Naming Tips

- ✅ Use descriptive names: `chr22_variant_analysis.ipynb`
- ✅ Add dates: `results_20250208.csv`
- ✅ Use versions: `analysis_v1.ipynb`, `analysis_v2.ipynb`
- ❌ Avoid: `test.ipynb`, `analysis1.ipynb`, `final_final.ipynb`

### Regular Cleanup

```python
# Clean up old results (older than 90 days)
import shutil
from pathlib import Path
from datetime import datetime, timedelta

results_dir = Path.home() / 'work' / 'results'
cutoff = datetime.now() - timedelta(days=90)

for item in results_dir.iterdir():
    if item.is_dir():
        # Parse date from directory name
        # Delete if older than cutoff
        pass
```

---

## 🔄 Workflow Examples

### Example 1: Quick Variant Analysis

```bash
# 1. Copy tutorial
cp /shared/notebooks/02_variant_analysis.ipynb ~/work/notebooks/

# 2. Open and modify with your variant
# (in JupyterLab)

# 3. Run and check results in ~/work/results/
```

### Example 2: Batch Processing

```bash
# 1. Upload your CSV
# Use JupyterLab upload button to upload to ~/work/data/

# 2. Open batch analysis notebook
# /shared/notebooks/03_batch_analysis.ipynb

# 3. Modify to load your data
# data_file = '~/work/data/my_variants.csv'

# 4. Run and export results
```

### Example 3: Reproducible Analysis

```bash
# 1. Copy template
cp /shared/notebooks/05_custom_analysis.ipynb ~/work/notebooks/my_project.ipynb

# 2. Modify for your project
# - Add metadata
# - Configure parameters
# - Document your analysis

# 3. Save all results with clear names
# 4. Export for sharing
```

---

## ❓ Common Questions

### Q: Can I see other users' files?
**A**: No. Each user's `~/work/` is completely private and isolated.

### Q: Where should I save my work?
**A**: Always save to `~/work/`. Subdirectories help organize:
- `~/work/notebooks/` - Your analysis notebooks
- `~/work/results/` - Analysis outputs
- `~/work/data/` - Your input data

### Q: Do I need to copy every notebook?
**A**: No. Only copy if you want to modify it. For learning, you can run directly from `/shared/notebooks/`.

### Q: How do I share my results?
**A**: Export to CSV/Excel and share the file, or use `/shared/teamwork/` if configured.

### Q: What happens when I logout?
**A**: Your work is saved. Everything in `~/work/` persists between sessions.

### Q: Can I accidentally delete the templates?
**A**: No. `/shared/notebooks/` is read-only. You can't modify or delete templates.

### Q: How much space do I have?
**A**: Limited by the server's disk space. Check with:
```python
import shutil
disk = shutil.disk_usage(str(Path.home()))
print(f"Available: {disk.free / (1024**3):.2f} GB")
```

---

## 🎯 Summary

| Task | How |
|------|-----|
| **Learn** | Run from `/shared/notebooks/` (read-only) |
| **Experiment** | Copy to `~/work/notebooks/` first |
| **Analyze** | Use `05_custom_analysis.ipynb` template |
| **Save** | Results go to `~/work/results/` |
| **Share** | Export to CSV/Excel or use `/shared/teamwork/` |

---

**Need more help?** Check `QUICKSTART.md` or `README.md`
