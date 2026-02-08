# AlphaGenome JupyterHub 部署方案

一个基于 Docker 的完整 JupyterHub 部署方案，用于在公司研发环境中运行 AlphaGenome（Google DeepMind 的基因组预测模型）。

## 项目概述

本项目提供了一个预配置的 Docker-based JupyterHub 部署方案，包含：

- 🚀 **快速开始**：预装所有依赖的 Docker 镜像
- 👥 **多用户支持**：JupyterHub 认证，支持 2-5 用户（可扩展）
- 📚 **示例教程**：6 个完整的教程，涵盖常见分析场景
- 🛠️ **自定义工具**：用于批量处理和数据导出的 Python 辅助库
- 🔒 **安全设计**：通过环境变量管理 API key
- 📦 **简单部署**：Docker Compose 一键启动

## 功能特性

- **🚀 快速上手**：预装 AlphaGenome 客户端库和所有依赖的 Docker 镜像
- **👥 多用户支持**：JupyterHub 认证系统，支持 2-5 名用户（可扩展）
- **📚 示例教程**：6 个全面的教程涵盖：
  - 快速入门指南
  - 变异效应分析
  - 批量处理
  - 高级可视化
  - 自定义分析模板
- **🛠️ 自定义工具**：用于批量处理、数据导出和可视化的辅助库
- **🔒 安全管理**：通过环境变量管理 API key
- **📦 易于部署**：Docker Compose 简化配置和部署

## 项目结构

```
alphagenome-deploy/
├── docker/
│   ├── Dockerfile              # JupyterHub 镜像定义
│   └── docker-compose.yml      # 服务编排
├── notebooks/                  # 示例教程（6个）
│   ├── 00_welcome_and_setup.ipynb    # 欢迎和设置
│   ├── 01_quickstart.ipynb           # 快速入门
│   ├── 02_variant_analysis.ipynb     # 变异效应分析
│   ├── 03_batch_analysis.ipynb       # 批量处理
│   ├── 04_visualization.ipynb        # 高级可视化
│   └── 05_custom_analysis.ipynb      # 自定义分析模板
├── alphagenome_tools/         # 自定义辅助库
│   ├── __init__.py
│   ├── helpers.py             # 批量处理工具
│   └── visualization.py       # 可视化工具
├── config/
│   └── jupyterhub_config.py   # JupyterHub 配置
├── data/
│   ├── reference/             # 参考基因组数据
│   └── examples/              # 示例数据集
├── .env.example               # API key 模板
├── .gitignore
├── README.md                  # 英文文档
└── README_CN.md               # 中文文档（本文件）
```

## 快速开始

### 前置要求

- Docker Desktop（Windows/Mac）或 Docker Engine（Linux）
- AlphaGenome API key（从 https://alphagenome.google/ 获取）
- 至少 8GB 可用内存

### 1. 获取项目

```bash
git clone https://github.com/timoxue/alphagenome-deploy.git
cd alphagenome-deploy
```

### 2. 配置 API Key

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
# Windows: notepad .env
# Mac/Linux: nano .env
```

在 `.env` 中添加你的 API key：
```
ALPHAGENOME_API_KEY=你的实际API密钥
```

**重要提示**：永远不要分享或提交 `.env` 文件！

### 3. 启动服务

```bash
# 构建并启动（首次运行需要 5-10 分钟）
docker-compose up --build

# 或在后台运行
docker-compose up -d --build
```

### 4. 访问 JupyterHub

1. 打开浏览器访问：http://localhost:8000
2. 使用系统用户名和密码登录
3. 开始探索 `/shared/notebooks/` 中的示例教程

## 使用指南

### 第一次使用：快速入门教程

1. 在 JupyterLab 中打开 `/shared/notebooks/`
2. 运行 `00_welcome_and_setup.ipynb` 了解平台
3. 运行 `01_quickstart.ipynb` 学习基础知识
4. 逐步尝试其他教程

### 分析基因变异

使用 `02_variant_analysis.ipynb` 来：
- 定义基因变异（SNP、插入、缺失）
- 对比参考等位基因和替代等位基因
- 计算效应分数
- 生成对比可视化

### 批量处理

使用 `03_batch_analysis.ipynb` 来：
- 从 CSV 文件加载多个变异
- 带进度追踪的批量预测
- 监控 API 配额
- 导出汇总结果

### 高级可视化

使用 `04_visualization.ipynb` 来：
- 创建发表级质量图表
- 构建多面板可视化
- 应用自定义样式和注释
- 导出为 PNG/PDF/SVG

### 自定义分析

复制 `05_custom_analysis.ipynb` 到你的工作空间（`~/work/`）来：
- 开始自己的分析
- 使用提供的模板结构
- 基于辅助函数构建

## 自定义工具

`alphagenome_tools` 包提供以下功能：

### `helpers.py`
- `batch_predict_variants()` - 批量变异预测
- `batch_predict_sequences()` - 批量序列预测
- `load_variants_from_csv()` - 从 CSV 加载变异
- `load_intervals_from_csv()` - 从 CSV 加载区间
- `save_results()` - 保存多种格式的结果
- `export_to_csv()` / `export_to_excel()` - 数据导出
- `monitor_api_quota()` - 追踪 API 使用情况

### `visualization.py`
- `quick_plot()` - 快速预览图
- `plot_variant_comparison()` - 变异对比图
- `plot_batch_summary()` - 批量结果汇总
- `plot_expression_heatmap()` - 基因表达热图
- `plot_tracks_overlaid()` - 重叠基因组轨道
- `create_multi_panel_figure()` - 多面板发表图

## 部署到生产服务器

### 本地开发（Windows 11）

1. 本地构建和测试：
   ```bash
   docker-compose up --build
   ```

2. 测试所有 notebook 并验证功能

3. 导出 Docker 镜像：
   ```bash
   docker save alphagenome-jupyterhub:latest > alphagenome-jupyterhub.tar
   ```

### 服务器部署（Linux）

1. 传输文件到服务器：
   ```bash
   scp alphagenome-jupyterhub.tar user@server:/opt/
   scp -r .env config/ user@server:/opt/alphagenome-deploy/
   ```

2. 在服务器上：
   ```bash
   # 安装 Docker
   sudo apt-get update
   sudo apt-get install -y docker.io docker-compose
   sudo systemctl start docker

   # 加载镜像
   docker load < /opt/alphagenome-jupyterhub.tar

   # 启动服务
   cd /opt/alphagenome-deploy
   docker-compose up -d
   ```

3. 配置防火墙：
   ```bash
   sudo ufw allow 8000/tcp
   ```

4. 访问地址：`http://服务器IP:8000`

## 配置说明

### JupyterHub

编辑 `config/jupyterhub_config.py`：
- 认证方式（PAM、LDAP、OAuth）
- 用户权限和管理员
- 资源限制（CPU、内存）
- Spawner 设置

### Docker 资源

编辑 `docker-compose.yml`：
- CPU 和内存限制
- 端口映射
- 卷挂载
- 网络设置

### API 配额

AlphaGenome 免费版限制：
- 适合中小规模分析
- 约 100 万次预测（查看当前限制）
- 使用 `monitor_api_quota()` 监控使用情况

## 故障排除

### 容器无法启动
```bash
# 查看日志
docker-compose logs -f

# 重新构建镜像
docker-compose build --no-cache
docker-compose up -d
```

### API key 不工作
- 验证 `.env` 文件是否存在且包含有效的 key
- 检查 API key 是否过期
- 确保 `ALPHAGENOME_API_KEY` 设置正确

### 内存不足
- 在 `docker-compose.yml` 中增加内存限制
- 减少并发用户数量
- 处理更小的批次

### 无法从网络访问
- 检查防火墙设置
- 验证端口 8000 是否开放
- 确保 JupyterHub 监听 `0.0.0.0`

## 维护和备份

### 备份用户数据

```bash
# 备份用户卷
docker run --rm \
  -v alphagenome-deploy_jupyterhub-user-data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/user-data-$(date +%Y%m%d).tar.gz /data
```

### 更新 AlphaGenome

```bash
# 拉取最新更改
git pull

# 重新构建镜像
docker-compose build --no-cache

# 重启服务
docker-compose up -d
```

### 监控资源

```bash
# 检查容器状态
docker stats

# 查看日志
docker-compose logs -f jupyterhub
```

## 安全注意事项

- **永远不要提交 `.env`** 到版本控制（它包含 API keys）
- 为用户账户使用强密码
- 限制网络访问（防火墙、仅内网）
- 定期更新 Docker 镜像以获取安全补丁
- 生产环境考虑使用 HTTPS
- 监控 API 使用情况以发现异常活动

## 文档

- **README.md** - 英文文档
- **README_CN.md** - 中文文档（本文件）
- **QUICKSTART.md** - 快速开始指南（英文）
- **USER_GUIDE.md** - 用户使用指南（英文）
- **USER_GUIDE_CN.md** - 用户使用指南（中文）
- **FILE_STRUCTURE.md** - 文件系统结构说明

## 贡献

如需添加新功能或修复问题：

1. 先在本地测试更改
2. 更新相关文档
3. 确保所有 notebook 仍能正常工作
4. 提交 Pull Request 并描述更改内容

## 许可证

本部署配置按原样提供，供内部企业使用。

AlphaGenome API 遵守 Google 的使用条款：
- 非商业用途免费
- 提供商业许可
- 参见：https://github.com/google-deepmind/alphagenome

## 支持

相关问题：
- **本部署**：查看故障排除部分或联系 IT 团队
- **AlphaGenome API**：https://github.com/google-deepmind/alphagenome/issues
- **JupyterHub**：https://discourse.jupyter.org/

## 致谢

- AlphaGenome by Google DeepMind
- JupyterHub by Project Jupyter
- Docker by Docker Inc.

---

**版本**：1.0.0
**最后更新**：2025-02-08
**维护团队**：你的研发 IT 团队

---

## 相关链接

- 🌐 **GitHub 仓库**：https://github.com/timoxue/alphagenome-deploy
- 📖 **AlphaGenome 官方文档**：https://github.com/google-deepmind/alphagenome
- 🐳 **Docker 文档**：https://docs.docker.com/
- 📚 **JupyterHub 文档**：https://jupyterhub.readthedocs.io/

---

**切换语言**：[English](README.md) | **中文**
