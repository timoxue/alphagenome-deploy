# 用户使用指南 - 个人工作空间使用说明

本指南详细说明如何在 AlphaGenome JupyterHub 平台上使用你的个人工作空间。

## 📂 理解你的工作空间

### 个人空间（私有 - 仅你可见）

每个用户都有**完全私有**的工作空间：

```
~/work/
├── notebooks/       # 你复制和修改的教程
├── results/         # 你的分析结果
├── data/            # 你上传的数据文件
├── figures/         # 你保存的图表和可视化
└── exports/         # 你导出的 CSV/Excel 文件
```

**关键要点**：
- 🔒 **私有**：其他用户无法查看或访问你的 `~/work/` 目录
- ✍️ **可写**：你可以创建、修改和删除文件
- 💾 **持久化**：即使你退出登录，你的工作也会被保存

### 共享资源（只读 - 所有人可见）

所有用户共享访问这些资源：

```
/shared/
├── notebooks/       # 教程 notebook（只读）
├── data/            # 参考和示例数据（只读）
└── tools/           # 辅助库（只读）
```

**关键要点**：
- 👥 **共享**：所有用户都可以看到这些文件
- 🔒 **只读**：没有人（包括你）可以修改这些文件
- 📚 **参考资料**：这些是模板和学习材料

---

## 🚀 如何使用本平台

### 场景 1：学习和探索（只读模式）

**最适合**：首次使用、学习基础知识

1. 在文件浏览器中导航到 `/shared/notebooks/`
2. 打开任意教程（例如 `01_quickstart.ipynb`）
3. 运行单元格来学习（Shift+Enter 或点击"运行"）
4. 结果自动保存到 `~/work/results/`

**优点**：
- ✅ 始终拥有原始模板
- ✅ 不会意外破坏任何内容
- ✅ 始终是最新版本

**缺点**：
- ❌ 无法修改 notebook
- ❌ 无法保存自己的代码更改

### 场景 2：实验和自定义（复制并修改）

**最适合**：自定义分析、实验探索

1. 导航到 `/shared/notebooks/`
2. 找到你想要使用的 notebook
3. **右键点击** → **复制**
4. 导航到 `~/work/notebooks/`
5. **粘贴**（Ctrl+V）
6. 打开复制的 notebook 并自由修改

**优点**：
- ✅ 可以自由修改和实验
- ✅ 保留自己的版本
- ✅ 原始模板保持不变

**示例**：
```
/shared/notebooks/01_quickstart.ipynb  →  复制
~/work/notebooks/01_quickstart.ipynb    →  修改和实验
```

### 场景 3：创建自己的分析

**最适合**：生产分析、自定义工作流程

1. 复制 `05_custom_analysis.ipynb` 到你的工作空间
2. 重命名（例如 `my_chr22_analysis.ipynb`）
3. 根据你的具体需求修改
4. 定期保存结果

---

## 📝 逐步操作：复制 Notebook

### 方法 1：使用 JupyterLab 界面（推荐）

1. **打开文件浏览器**（左侧边栏）
2. **导航到** `/shared/notebooks/`
3. **右键点击**你想要的 notebook
4. **选择"复制"**
5. **导航到** `~/work/notebooks/`
6. **在空白处右键点击**
7. **选择"粘贴"**

### 方法 2：使用代码（自动）

在 notebook 单元格中运行：

```python
# 以编程方式复制 notebook
import shutil
from pathlib import Path

src = Path('/shared/notebooks/01_quickstart.ipynb')
dst = Path.home() / 'work' / 'notebooks' / 'my_quickstart.ipynb'

shutil.copy(src, dst)
print(f"✅ 已复制到 {dst}")
```

---

## 💾 保存你的工作

### 我的结果在哪里？

默认情况下，结果保存到：

```
~/work/results/
├── quickstart_20250208_143022/
├── variant_analysis_20250208_150145/
└── batch_analysis_20250208_160230/
```

每次分析都会创建一个**带时间戳的目录**来保持结果有序。

### 手动保存

```python
from pathlib import Path

# 保存到特定位置
output_dir = Path.home() / 'work' / 'results' / 'my_analysis'
output_dir.mkdir(parents=True, exist_ok=True)

# 在这里保存你的文件
```

---

## 🔍 查找你的文件

### 在 JupyterLab 中

1. 打开**文件浏览器**（左侧边栏）
2. 点击 `~/work/` 的**文件夹图标**
3. 浏览子目录

### 文件位置

| 内容 | 位置 |
|------|------|
| 你的 notebook | `~/work/notebooks/` |
| 分析结果 | `~/work/results/` |
| 上传的数据 | `~/work/data/` |
| 保存的图表 | `~/work/figures/` |
| 导出文件（CSV/Excel） | `~/work/exports/` |
| 教程模板 | `/shared/notebooks/`（只读）|

---

## 📤 与团队分享结果

由于每个用户的 `~/work/` 是私有的，通过以下方式分享结果：

### 方法 1：导出为 CSV/Excel

```python
# 导出结果
from alphagenome_tools import export_to_csv, export_to_excel
import pandas as pd

# 你的结果
results_df = pd.DataFrame(...)

# 导出到共享位置（如果配置了）
export_to_csv(results_df, '~/work/exports/my_results.csv')
```

然后通过以下方式分享文件：
- 邮件
- 共享网络驱动器
- 内部消息系统
- Git 仓库

### 方法 2：生成报告

```python
# 将 notebook 转换为 HTML
!jupyter nbconvert --to html my_analysis.ipynb

# 分享 HTML 文件
```

### 方法 3：使用共享协作目录（可选）

如果管理员配置了 `/shared/teamwork/`：

```python
# 保存到共享位置
shared_dir = Path('/shared/teamwork')
results.to_csv(shared_dir / 'team_results.csv')
```

**注意**：所有用户都可以看到和修改这里的文件！

---

## 🏗️ 最佳实践

### 组织你的工作

```
~/work/
├── notebooks/
│   ├── 01_quickstart_copy.ipynb        # 教程副本
│   ├── chr22_analysis.ipynb            # 你的自定义分析
│   └── batch_processing_v1.ipynb
├── results/
│   ├── chr22_region1/                  # 按项目组织
│   ├── chr22_region2/
│   └── batch_analysis_20250208/
├── data/
│   ├── my_variants.csv                 # 你的输入数据
│   ├── custom_regions.bed
│   └── project_data/
├── figures/
│   ├── figure1.png
│   └── publication_figure.pdf
└── exports/
    ├── summary_20250208.xlsx
    └── results.csv
```

### 文件命名技巧

- ✅ 使用描述性名称：`chr22_variant_analysis.ipynb`
- ✅ 添加日期：`results_20250208.csv`
- ✅ 使用版本号：`analysis_v1.ipynb`、`analysis_v2.ipynb`
- ❌ 避免：`test.ipynb`、`analysis1.ipynb`、`final_final.ipynb`

### 定期清理

```python
# 清理旧结果（超过 90 天）
import shutil
from pathlib import Path
from datetime import datetime, timedelta

results_dir = Path.home() / 'work' / 'results'
cutoff = datetime.now() - timedelta(days=90)

for item in results_dir.iterdir():
    if item.is_dir():
        # 从目录名称解析日期
        # 如果早于截止日期则删除
        pass
```

---

## 🔄 工作流程示例

### 示例 1：快速变异分析

```bash
# 1. 复制教程
cp /shared/notebooks/02_variant_analysis.ipynb ~/work/notebooks/

# 2. 打开并使用你的变异进行修改
# （在 JupyterLab 中）

# 3. 运行并在 ~/work/results/ 中检查结果
```

### 示例 2：批量处理

```bash
# 1. 上传你的 CSV
# 使用 JupyterLab 上传按钮上传到 ~/work/data/

# 2. 打开批量分析 notebook
# /shared/notebooks/03_batch_analysis.ipynb

# 3. 修改以加载你的数据
# data_file = '~/work/data/my_variants.csv'

# 4. 运行并导出结果
```

### 示例 3：可重现的分析

```bash
# 1. 复制模板
cp /shared/notebooks/05_custom_analysis.ipynb ~/work/notebooks/my_project.ipynb

# 2. 为你的项目修改
# - 添加元数据
# - 配置参数
# - 记录你的分析

# 3. 使用清晰的名称保存所有结果
# 4. 导出以便分享
```

---

## ❓ 常见问题

### Q: 我能看到其他用户的文件吗？
**A**: 不能。每个用户的 `~/work/` 目录完全私有且相互隔离。

### Q: 我应该把工作保存在哪里？
**A**: 始终保存到 `~/work/`。子目录有助于组织：
- `~/work/notebooks/` - 你的分析 notebook
- `~/work/results/` - 分析输出
- `~/work/data/` - 你的输入数据

### Q: 我需要复制每个 notebook 吗？
**A**: 不需要。只有在你想要修改时才复制。对于学习，可以直接从 `/shared/notebooks/` 运行。

### Q: 如何分享我的结果？
**A**: 导出为 CSV/Excel 并分享文件，或使用 `/shared/teamwork/`（如果已配置）。

### Q: 我退出登录后会发生什么？
**A**: 你的工作会被保存。`~/work/` 中的所有内容在会话之间持久存在。

### Q: 我会意外删除模板吗？
**A**: 不会。`/shared/notebooks/` 是只读的。你无法修改或删除模板。

### Q: 我有多少空间？
**A**: 受服务器磁盘空间限制。检查方法：
```python
import shutil
disk = shutil.disk_usage(str(Path.home()))
print(f"可用空间: {disk.free / (1024**3):.2f} GB")
```

---

## 🎯 总结

| 任务 | 方法 |
|------|------|
| **学习** | 从 `/shared/notebooks/` 运行（只读）|
| **实验** | 先复制到 `~/work/notebooks/` |
| **分析** | 使用 `05_custom_analysis.ipynb` 模板 |
| **保存** | 结果自动保存到 `~/work/results/` |
| **分享** | 导出为 CSV/Excel 或使用 `/shared/teamwork/` |

---

## 📖 相关文档

- **README_CN.md** - 项目中文主页
- **QUICKSTART.md** - 快速开始指南
- **FILE_STRUCTURE.md** - 文件系统结构说明
- **USER_GUIDE.md** - 英文用户指南

---

## 💡 使用提示

### 使用 Notebook

- ✅ **只读**：直接从 `/shared/notebooks/` 运行
- ✅ **实验**：在修改前复制到 `~/work/notebooks/`
- ✅ **保存**：结果自动保存到 `~/work/results/`

### 管理数据

- ✅ 上传文件到 `~/work/data/`
- ✅ 使用 CSV 格式存储变异/区间
- ✅ 将数据文件组织在文件夹中

### API 配额管理

- ✅ 在大批量作业前检查配额
- ✅ 从小批次开始（10-20 项）
- ✅ 在长时间运行期间监控使用情况

### 协作

- ❌ 每个用户的 `~/work/` 都是**私有的**（不共享）
- ✅ 通过导出为 CSV/Excel 分享结果
- ✅ 如果需要协作，使用 `/shared/teamwork/`

---

**需要更多帮助？** 查看 `QUICKSTART.md` 或 `README_CN.md`

**祝你分析顺利！🧬**
