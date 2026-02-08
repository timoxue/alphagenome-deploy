# File System Structure - Visual Guide

This document shows the complete file system structure from a user's perspective.

## 🌳 Complete Directory Tree

```
alphagenome-jupyterhub/
│
├── 📁 /home/                          # User home directories
│   ├── 📁 user1/                      # User 1's private space
│   │   └── 📁 work/                   # User 1's workspace
│   │       ├── 📁 notebooks/          # 👤 PRIVATE: User 1's notebooks
│   │       ├── 📁 results/            # 👤 PRIVATE: User 1's results
│   │       ├── 📁 data/               # 👤 PRIVATE: User 1's data
│   │       ├── 📁 figures/            # 👤 PRIVATE: User 1's figures
│   │       └── 📁 exports/            # 👤 PRIVATE: User 1's exports
│   │
│   ├── 📁 user2/                      # User 2's private space
│   │   └── 📁 work/                   # User 2's workspace
│   │       ├── 📁 notebooks/          # 👤 PRIVATE: User 2's notebooks
│   │       ├── 📁 results/            # 👤 PRIVATE: User 2's results
│   │       └── ...                    # (same structure as user1)
│   │
│   ├── 📁 user3/                      # User 3's private space
│   │   └── 📁 work/                   # (same structure)
│   │
│   └── ...                            # More users
│
├── 📁 /shared/                        # 📚 SHARED: Read-only resources
│   ├── 📁 notebooks/                  # 👥 Tutorials (all users can read)
│   │   ├── 📄 00_welcome_and_setup.ipynb
│   │   ├── 📄 01_quickstart.ipynb
│   │   ├── 📄 02_variant_analysis.ipynb
│   │   ├── 📄 03_batch_analysis.ipynb
│   │   ├── 📄 04_visualization.ipynb
│   │   └── 📄 05_custom_analysis.ipynb
│   │
│   ├── 📁 data/                       # 👥 Reference data (read-only)
│   │   ├── 📁 reference/              # Reference genomes, annotations
│   │   └── 📁 examples/               # Example datasets
│   │
│   ├── 📁 tools/                      # 👥 Helper library (read-only)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 helpers.py
│   │   └── 📄 visualization.py
│   │
│   └── 📁 teamwork/                   # 👥 Optional shared workspace
│       └── 📁 shared_results/         # Everyone can read/write here
│
└── 📁 /etc/jupyterhub/                # ⚙️  System configuration
    └── 📄 jupyterhub_config.py
```

## 🔐 Privacy and Access Matrix

| Location | User 1 | User 2 | User 3 | Read/Write |
|----------|--------|--------|--------|------------|
| `~/work/` (User 1) | ✅ Full | ❌ None | ❌ None | Read+Write |
| `~/work/` (User 2) | ❌ None | ✅ Full | ❌ None | Read+Write |
| `~/work/` (User 3) | ❌ None | ❌ None | ✅ Full | Read+Write |
| `/shared/notebooks/` | ✅ Read | ✅ Read | ✅ Read | Read-Only |
| `/shared/data/` | ✅ Read | ✅ Read | ✅ Read | Read-Only |
| `/shared/tools/` | ✅ Read | ✅ Read | ✅ Read | Read-Only |
| `/shared/teamwork/` | ✅ Full | ✅ Full | ✅ Full | Read+Write |

## 🎯 User View - What You See

### As User 1 (user1)

When you login as **user1**, you see:

```
📁 /                                 # Root
├── 📁 home/
│   └── 📁 user1/                    # Your home (same as ~)
│       └── 📁 work/                 # Your workspace
│           ├── 📁 notebooks/        # 📝 Your notebooks
│           ├── 📁 results/          # 💾 Your results
│           ├── 📁 data/             # 📊 Your data
│           ├── 📁 figures/          # 📈 Your figures
│           └── 📁 exports/          # 📤 Your exports
│
└── 📁 shared/                       # Shared resources
    ├── 📁 notebooks/                # 👀 Read-only tutorials
    ├── 📁 data/                     # 👀 Read-only data
    └── 📁 tools/                    # 👀 Read-only tools
```

**You CANNOT see:**
- ❌ `/home/user2/` - Other users' directories don't exist in your view
- ❌ `/home/user3/` - Each user has an isolated view
- ✅ You only see `/home/user1/` (your own directory)

## 🔄 Typical Workflow

### Step 1: Start with Tutorials (Read-Only)

```
/shared/notebooks/01_quickstart.ipynb
    ↓
    (Read and run, cannot modify)
    ↓
Results saved to: ~/work/results/quickstart_20250208/
```

### Step 2: Copy and Customize

```
/shared/notebooks/02_variant_analysis.ipynb
    ↓ (Right-click → Copy)
~/work/notebooks/02_variant_analysis.ipynb
    ↓ (Modify, experiment, save)
~/work/results/variant_analysis_20250208/
```

### Step 3: Create Your Own Analysis

```
/shared/notebooks/05_custom_analysis.ipynb
    ↓ (Copy and rename)
~/work/notebooks/my_chr22_analysis.ipynb
    ↓ (Run your analysis)
~/work/results/my_chr22_analysis/
```

## 📊 File Ownership Examples

### Example 1: User Creates a File

**Action**: User 1 creates `~/work/data/my_variants.csv`

| Location | Owner | User 1 | User 2 | User 3 |
|----------|-------|--------|--------|--------|
| `~/work/data/my_variants.csv` | User 1 | ✅ See | ❌ Hidden | ❌ Hidden |

**Result**: Only User 1 can see this file

### Example 2: User Copies Template

**Action**: User 1 copies `/shared/notebooks/01_quickstart.ipynb`

| Location | Owner | Access | User 1 | User 2 | User 3 |
|----------|-------|--------|--------|--------|--------|
| `/shared/notebooks/01_quickstart.ipynb` | System | Read-Only | ✅ Read | ✅ Read | ✅ Read |
| `~/work/notebooks/01_quickstart.ipynb` | User 1 | Read+Write | ✅ Full | ❌ Hidden | ❌ Hidden |

**Result**: User 1 has their own modifiable copy

### Example 3: User Generates Results

**Action**: User 1 runs analysis, saves to `~/work/results/`

| Location | Owner | User 1 | User 2 | User 3 |
|----------|-------|--------|--------|--------|
| `~/work/results/analysis_20250208/` | User 1 | ✅ Full | ❌ Hidden | ❌ Hidden |

**Result**: Results are private to User 1

## 🎓 Quick Reference

### Where should I put...?

| What | Location | Who can see? |
|------|----------|-------------|
| My analysis notebook | `~/work/notebooks/` | Only me |
| My uploaded data | `~/work/data/` | Only me |
| Analysis results | `~/work/results/` | Only me |
| Shared team results | `/shared/teamwork/` | Everyone |
| Tutorial copy | `~/work/notebooks/` | Only me |
| Template reference | `/shared/notebooks/` | Everyone (read-only) |

### How do I...?

| Task | How |
|------|-----|
| **Read tutorial** | Open from `/shared/notebooks/` |
| **Modify tutorial** | Copy to `~/work/notebooks/` first |
| **Save my work** | Use `~/work/` directories |
| **Share with team** | Export to CSV or use `/shared/teamwork/` |
| **Upload data** | Use JupyterLab upload to `~/work/data/` |
| **Find my files** | Look in `~/work/` |

## 🎯 Summary

✅ **Each user has their own private `~/work/` directory**
✅ **`/shared/` is read-only for all users**
✅ **Users cannot see each other's `~/work/` directories**
✅ **Copy templates to `~/work/` to modify them**
✅ **Results are automatically saved to `~/work/results/`**

---

**Need more details?** See:
- `USER_GUIDE.md` - Detailed user guide
- `QUICKSTART.md` - Quick start tutorial
- `README.md` - Full documentation
