# AlphaGenome JupyterHub 部署方案设计

**日期**: 2025-02-08
**团队规模**: 2-5 人
**目标用户**: 医药研发团队

---

## 1. 项目概述

为医药研发团队部署基于 JupyterHub 的 AlphaGenome 分析平台，支持序列预测、变异效应分析、可视化和批量分析功能。

**关键需求**:
- 部署在公司内部服务器
- 用户熟悉 Python 和 Jupyter
- 2-5 人并发使用
- 支持序列预测、变异效应分析、可视化、批量分析
- 共享 API key（团队内部使用）

---

## 2. 系统架构

### 2.1 本地开发环境（Windows 11 + Docker Desktop）

**核心组件**:
- Docker Desktop for Windows
- 基于 `jupyterhub/jupyterhub:4.1.5` 定制镜像
- Python 3.8+ 环境
- AlphaGenome 客户端库及依赖

**目录结构**:
```
alphagenome-deploy/
├── docker/                      # Docker 配置
│   ├── Dockerfile               # JupyterHub 镜像
│   └── docker-compose.yml
├── notebooks/                   # 示例和分析模板
│   ├── 01_quickstart.ipynb
│   ├── 02_variant_analysis.ipynb
│   ├── 03_batch_analysis.ipynb
│   ├── 04_visualization.ipynb
│   └── 05_custom_analysis.ipynb
├── alphagenome_tools/           # 自定义工具库
│   ├── __init__.py
│   ├── helpers.py
│   └── visualization.py
├── config/                      # 配置文件
│   └── jupyterhub_config.py
├── data/                        # 示例数据
│   ├── reference/
│   └── examples/
├── .env                         # API key（不提交 git）
└── .gitignore
```

### 2.2 服务器部署环境（Linux）

**部署方式**:
- 导出 Docker 镜像 → 传输到服务器 → 运行
- 使用 Docker Compose 管理服务
- 通过 systemd 管理 Docker 服务
- 内网访问: `http://服务器IP:8000`

**网络配置**:
- JupyterHub 监听 8000 端口
- 防火墙允许内网 IP 访问
- 可选: nginx 反向代理 + HTTPS

---

## 3. 用户交互流程

### 3.1 登录流程
1. 访问 `http://服务器IP:8000`
2. 输入用户名和密码（PAM 或本地认证）
3. JupyterHub 启动个人 JupyterLab 容器
4. 自动挂载共享目录和个人目录

### 3.2 JupyterLab 工作区

**目录布局**:
```
/shared/
├── notebooks/      # 只读示例和模板
├── data/           # 只读参考数据
└── tools/          # 只读工具库
~/work/             # 用户个人工作空间
```

### 3.3 典型工作流

**场景 A: 单序列预测**
1. 打开 `01_quickstart.ipynb`
2. 输入染色体区域
3. 运行预测，查看结果
4. 保存到 `~/work/`

**场景 B: 变异效应分析**
1. 打开 `02_variant_analysis.ipynb`
2. 定义变异（位置、ref、alt）
3. 运行变异预测
4. 生成对比可视化
5. 导出报告

**场景 C: 批量分析**
1. 准备变异列表 CSV
2. 打开 `03_batch_analysis.ipynb`
3. 加载 CSV，批量调用 API
4. 汇总统计
5. 保存批量结果

---

## 4. 数据管理和存储

### 4.1 Docker Volume 映射

```yaml
volumes:
  # 共享资源（只读）
  - ./notebooks:/shared/notebooks:ro
  - ./data:/shared/data:ro
  - ./alphagenome_tools:/shared/tools:ro

  # 用户数据（读写）
  - jupyterhub-user-data:/home

  # 持久化配置
  - jupyterhub-config:/etc/jupyterhub
```

### 4.2 数据管理策略

**输入数据**:
- 用户通过 JupyterLab 界面上传到 `~/work/`
- 或通过 SCP/SMB 传输
- 支持格式: CSV, BED, VCF, FASTA

**输出数据**:
- 保存到 `~/work/results/`
- 自动添加时间戳
- 导出格式: PNG/SVG/PDF（图表）、CSV/Excel/JSON（数据）、HTML（报告）

**数据清理**:
- 定期提醒清理旧数据
- 可选 cron 任务清理 90 天以上临时文件

### 4.3 API 配额管理

**工具库功能**:
- 追踪 API 调用次数
- 显示剩余配额
- 接近限制时警告
- 记录日志到 `~/work/api_usage.log`

---

## 5. 安全性设计

### 5.1 API Key 管理

**存储方式**:
```yaml
# docker-compose.yml
environment:
  - ALPHAGENOME_API_KEY=${ALPHAGENOME_API_KEY}
env_file:
  - .env
```

```python
# config/jupyterhub_config.py
c.Spawner.environment = {
    'ALPHAGENOME_API_KEY': os.environ.get('ALPHAGENOME_API_KEY', ''),
}
```

**安全措施**:
- `.env` 添加到 `.gitignore`
- 文件权限 `600`
- 定期轮换 API key
- 提供模板文件 `.env.example`

### 5.2 用户认证

**推荐方案（2-5人团队）**:
- PAMAuthenticator（Linux 系统账号）
- 或 SimpleLocalAuthenticator（本地用户）
- 预设用户: user1-user5
- 初始密码管理员分配

**可选增强**:
- LDAP/Active Directory 集成
- OAuth（需要外网）

### 5.3 网络安全

**内网访问**:
- 监听 `0.0.0.0:8000` 或内网 IP
- 防火墙限制内网 IP 段访问

**HTTPS（可选）**:
- 内网: 自签名证书
- 有域名: Let's Encrypt
- nginx 反向代理处理 SSL

### 5.4 容器隔离

- 每个用户容器独立运行
- 限制 CPU 和内存资源
- Docker 用户命名空间增强隔离

### 5.5 数据隔离

- 用户只能访问自己的 home 目录
- 共享目录只读
- 可选协作目录 `/shared/teamwork/`

---

## 6. 示例 Notebook 设计

### 6.1 01_quickstart.ipynb
快速入门示例:
- 导入库和初始化
- 创建模型连接
- 定义分析区域
- 运行序列预测
- 简单可视化
- 保存结果

### 6.2 02_variant_analysis.ipynb
变异效应分析:
- 定义变异（点变异、插入、缺失）
- 预测参考 vs 替代等位基因
- 计算差异分数
- 生成对比图表
- 导出变异效应报告

### 6.3 03_batch_analysis.ipynb
批量分析:
- 从 CSV 加载变异列表
- 批量预测（带进度条）
- API 配额监控
- 汇总统计和可视化
- 导出批量结果

### 6.4 04_visualization.ipynb
高级可视化:
- 基因表达热图
- 剪接模式可视化
- 染色质特征图谱
- 多模态组合图
- 自定义图表样式
- 导出出版级图片

### 6.5 05_custom_analysis.ipynb
自定义分析模板:
- 常用导入
- 代码框架
- 注释说明
- 用户可基于此创建分析

---

## 7. 工具库设计（alphagenome_tools）

### 7.1 helpers.py

**核心函数**:
```python
batch_predict_variants(variants, model, ontology_terms, show_progress)
    # 批量预测变异效应

load_variants_from_csv(filepath)
    # 从 CSV 加载变异列表

save_results(outputs, prefix, output_dir)
    # 保存结果到多个格式

export_to_excel(dataframes, filename)
    # 导出 Excel 文件

create_comparison_table(ref_outputs, alt_outputs)
    # 创建对比表格
```

### 7.2 visualization.py

**可视化函数**:
```python
quick_plot(outputs, figsize)
    # 快速生成预览图表

plot_variant_comparison(ref_outputs, alt_outputs, variant)
    # 对比参考和替代等位基因

plot_batch_summary(results_df)
    # 批量结果汇总图

plot_expression_heatmap(outputs)
    # 基因表达热图
```

---

## 8. 部署流程

### 8.1 本地开发（Windows 11）

```bash
# 创建项目
mkdir alphagenome-deploy
cd alphagenome-deploy
mkdir -p docker notebooks alphagenome_tools config data/{reference,examples}

# 配置 API key
echo "ALPHAGENOME_API_KEY=your_key_here" > .env

# 启动服务
docker-compose up --build

# 访问 http://localhost:8000 测试
```

### 8.2 服务器部署（Linux）

```bash
# 安装 Docker
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker

# 创建目录
sudo mkdir -p /opt/alphagenome-deploy
cd /opt/alphagenome-deploy

# 传输文件（从 Windows）
# 1. docker save 导出镜像
# 2. scp 传输镜像和配置文件
# 3. docker load 加载镜像

# 启动服务
docker-compose up -d

# 配置防火墙
sudo ufw allow 8000/tcp

# 创建用户账号
sudo adduser user1
sudo adduser user2
# ...
```

---

## 9. 运维管理

### 9.1 日常维护

```bash
# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 停止服务
docker-compose down
```

### 9.2 备份策略

**用户数据备份**:
```bash
docker run --rm \
  -v jupyterhub-user-data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/user-data-$(date +%Y%m%d).tar.gz /data
```

**配置文件备份**:
```bash
tar czf config-$(date +%Y%m%d).tar.gz .env config/
```

### 9.3 监控和告警（可选）

- 容器健康检查: HEALTHCHECK 指令
- 磁盘空间监控
- API 使用监控（工具库记录日志）

### 9.4 更新升级

- 定期更新 AlphaGenome 客户端库
- 更新示例 Notebook
- 安全补丁: 更新基础镜像

---

## 10. 下一步行动

1. **本地开发环境搭建**
   - 创建项目目录结构
   - 编写 Dockerfile 和 docker-compose.yml
   - 配置 JupyterHub

2. **开发工具库和示例 Notebook**
   - 实现 `alphagenome_tools/helpers.py`
   - 实现 `alphagenome_tools/visualization.py`
   - 创建 5 个示例 Notebook

3. **本地测试**
   - 启动 Docker 环境
   - 测试所有示例 Notebook
   - 验证 API 调用和数据存储

4. **服务器部署**
   - 准备 Linux 服务器
   - 传输镜像和配置
   - 启动服务并测试
   - 创建用户账号

5. **团队培训**
   - 准备使用文档
   - 演示主要功能
   - 收集反馈并迭代

---

## 附录: Docker 配置示例

### Dockerfile
```dockerfile
FROM jupyterhub/jupyterhub:4.1.5

USER root
RUN apt-get update && apt-get install -y \
    git vim \
    && rm -rf /var/lib/apt/lists/*

USER jovyan
RUN pip install --no-cache-dir \
    alphagenome \
    matplotlib \
    seaborn \
    pandas \
    biopython \
    tqdm \
    openpyxl

COPY alphagenome_tools /opt/alphagenome_tools
COPY notebooks /shared/notebooks

WORKDIR /home/jovyan/work
EXPOSE 8000

CMD ["jupyterhub", "-C", "/etc/jupyterhub/jupyterhub_config.py"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  jupyterhub:
    build:
      context: .
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - ALPHAGENOME_API_KEY=${ALPHAGENOME_API_KEY}
    volumes:
      - ./notebooks:/shared/notebooks:ro
      - ./data:/shared/data:ro
      - ./alphagenome_tools:/shared/tools:ro
      - jupyterhub-user-data:/home
      - ./config/jupyterhub_config.py:/etc/jupyterhub/jupyterhub_config.py:ro
    restart: unless-stopped

volumes:
  jupyterhub-user-data:
```

---

**文档状态**: ✅ 设计完成，等待用户确认后进入实施阶段
