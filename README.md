# 📖 生活日志追踪工具

一个智能的个人生活日志工具，使用 Google Gemini AI 自动分析你复制的文字和图片内容，生成结构化的日志记录，帮助你追踪和分析时间使用情况。

## ✨ 特性

- 🤖 **AI 智能分析**：使用 Google Gemini API 自动分析内容，生成总结、分类和标签
- ⏱️ **智能时长追踪**：自动计算并更新日志实际时长，无需手动估计
- 📋 **便捷输入**：从剪贴板直接读取文字和图片
- 🖼️ **多模态支持**：同时支持文字和图片输入
- 💾 **本地存储**：使用 SQLite 数据库，数据完全在本地
- 📊 **统计分析**：自动统计活动类型、耗时和标签分布
- 🖥️ **双界面**：命令行工具（快速操作）+ Web 界面（深度分析）
- 🎨 **美观界面**：Rich 库美化命令行输出，现代化的 Web UI

## 📦 安装

### 前置要求

- Python 3.10 或更高版本
- [uv](https://github.com/astral-sh/uv) - Python 包管理工具
- Google Gemini API Key

### 安装步骤

#### 方式 1：全局安装（推荐）

使用 `uv tool` 全局安装，可以在任何目录直接使用 `timeflow` 命令：

```bash
# 1. 克隆或进入项目目录
cd /path/to/logger

# 2. 全局安装（可编辑模式）
uv tool install --editable .

# 或使用 Makefile
make install
```

安装后，`timeflow` 命令将在任何目录都可用！✨

#### 方式 2：项目内使用

如果你只想在项目目录内使用：

```bash
# 1. 进入项目目录
cd /path/to/logger

# 2. 安装依赖
uv sync
```

然后使用 `uv run timeflow` 命令（需要在项目目录内）。

### 配置 API Key

复制 `.env.example` 到 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 Gemini API Key：

```env
GEMINI_API_KEY=your_actual_api_key_here
```

获取 Gemini API Key：访问 [Google AI Studio](https://makersuite.google.com/app/apikey)

### 验证安装

```bash
# 如果使用全局安装
timeflow --help

# 如果使用项目内安装
uv run timeflow --help
```

看到帮助信息说明安装成功！✅

## 🚀 使用方法

> 💡 **新特性**：现在默认进入交互编辑模式，可以一次输入中多次粘贴文字和图片！详见 [交互模式指南](INTERACTIVE_MODE_GUIDE.md)

> 📝 **注意**：以下示例假设你已全局安装。如果使用项目内安装，请在命令前加 `uv run`（如 `uv run timeflow add`）

### 命令行界面

#### 1. 添加日志

**交互编辑模式**（默认，推荐）：

```bash
# 进入交互编辑模式，可以多次粘贴内容
timeflow add

# 或明确指定
timeflow add --edit
```

在交互模式下：
1. 可以多次粘贴文字和图片
2. 每次粘贴后按回车确认
3. 输入 `done` 或按 `Ctrl+D` 完成输入
4. 所有内容会合并后一起发送给 AI 分析

**快速模式**（直接从剪贴板读取一次）：

```bash
# 先复制内容，然后运行
timeflow add --no-edit
```

**直接指定文字**：

```bash
timeflow add --text "正在学习 Python 编程"
```

**指定图片**：

```bash
timeflow add --image /path/to/image.jpg
```

**同时指定文字和图片**：

```bash
timeflow add --text "代码截图" --image screenshot.png
```

#### 2. 查询日志

**查看最近 10 条**：

```bash
timeflow list
```

**查看今天的日志**：

```bash
timeflow list --today
```

**查看指定日期**：

```bash
timeflow list --date 2025-11-27
```

**查看日期范围**：

```bash
timeflow list --range 2025-11-01 2025-11-30
```

**按分类筛选**：

```bash
timeflow list --category 工作
```

**自定义数量**：

```bash
timeflow list --limit 50
```

#### 3. 统计分析

**总体统计**：

```bash
timeflow stats
```

**今日统计**：

```bash
timeflow stats --today
```

**本周统计**：

```bash
timeflow stats --week
```

**本月统计**：

```bash
timeflow stats --month
```

#### 4. 启动 Web 界面

```bash
timeflow web
```

默认在 `http://127.0.0.1:8000` 启动。

指定端口和主机：

```bash
timeflow web --host 0.0.0.0 --port 5000
```

### Web 界面

启动 Web 服务后，在浏览器中访问：

- **时间线页面** (`/`)：查看所有日志记录，支持按分类、日期筛选
- **统计页面** (`/stats`)：查看图表化的统计分析，包括分类分布、耗时统计、标签云等

## ⏱️ 智能时长追踪

> **🆕 新特性**：从 v0.3.0 开始，系统会自动计算并更新日志的实际时长！

### 工作原理

当你添加一条新日志时，系统会：

1. 🔍 **查找上一条日志**：在当天（00:00-23:59）范围内查找最近的一条日志
2. ⏰ **计算时间差**：新日志时间 - 上一条日志时间 = 实际活动时长
3. 🔄 **自动更新**：将计算结果更新到上一条日志的时长字段
4. 💬 **友好提示**：在控制台显示更新信息

### 使用示例

```bash
$ timeflow add
# ... 交互输入内容 ...

💾 保存到数据库...
⏱  已自动更新上一条日志 (ID: 5) 的时长：45 分钟
✅ 日志已保存！ (ID: 6)
```

### 实际场景

假设你今天的活动记录：

```
08:30 - 📝 开始写代码（时长：0分钟）
10:00 - 💬 参加会议（自动更新上一条：90分钟）
11:30 - ☕ 喝咖啡休息（自动更新上一条：90分钟）
```

最终每条日志都有准确的实际时长，无需手动估计！

### 详细文档

更多信息请参考：[AUTO_DURATION_UPDATE.md](AUTO_DURATION_UPDATE.md)

## 📊 数据结构

每条日志包含以下信息：

- **ID**：唯一标识
- **创建时间**：记录创建的时间戳
- **原始文字**：复制的文字内容
- **图片路径**：保存的图片文件路径
- **AI 总结**：Gemini 生成的活动总结（50-100字）
- **分类**：活动类型（工作、学习、娱乐、运动、社交、生活、其他）
- **标签**：3-5个关键标签
- **时长（duration_estimate）**：活动持续时间（分钟），自动计算或AI估算

## 🗂️ 项目结构

```
logger/
├── src/
│   └── logger/
│       ├── __init__.py
│       ├── cli.py              # 命令行界面
│       ├── config.py           # 配置管理
│       ├── api/
│       │   └── gemini.py       # Gemini API 集成
│       ├── db/
│       │   ├── models.py       # 数据库模型
│       │   └── operations.py  # CRUD 操作
│       ├── web/
│       │   ├── app.py          # FastAPI 应用
│       │   ├── templates/      # HTML 模板
│       │   └── static/         # CSS 样式
│       └── utils/
│           └── clipboard.py    # 剪贴板处理
├── data/
│   ├── logger.db              # SQLite 数据库
│   └── images/                # 图片存储
├── pyproject.toml             # 项目配置
├── .env                       # 环境变量（需自己创建）
└── README.md                  # 本文档
```

## ⚙️ 配置选项

在 `.env` 文件中可配置以下选项：

```env
# 必需配置
GEMINI_API_KEY=your_api_key_here

# 可选配置
DATABASE_PATH=./data/logger.db          # 数据库路径
IMAGE_STORAGE_PATH=./data/images        # 图片存储路径
GEMINI_MODEL=gemini-1.5-flash          # 模型选择（flash 或 pro）
```

## 💡 使用技巧

1. **快速记录**：养成复制关键内容的习惯，然后立即运行 `timeflow add`
2. **命令自动补全**：启用 shell 自动补全，按 Tab 键自动补全命令（见 [SHELL_COMPLETION.md](SHELL_COMPLETION.md)）
3. **创建快捷别名**：在 `~/.zshrc` 中添加 `alias la='timeflow add'`，快速记录
4. **定期回顾**：使用 `timeflow stats --week` 查看每周的时间分配
5. **分析优化**：通过统计数据识别时间黑洞，优化时间使用
6. **标签筛选**：合理使用 AI 生成的标签，便于后续查找
7. **图片记录**：截图重要界面或文档，让日志更完整

## 🎯 使用场景

- 📚 **学习追踪**：记录学习内容和时长，分析学习效率
- 💼 **工作记录**：追踪工作任务和时间分配
- 🎮 **娱乐分析**：了解娱乐活动占用时间
- 🏃 **运动记录**：追踪运动频率和时长
- 📝 **生活日志**：记录日常生活的点点滴滴

## 🔧 常见问题

### 1. 如何获取 Gemini API Key？

访问 [Google AI Studio](https://makersuite.google.com/app/apikey) 创建 API Key。

### 2. 剪贴板读取失败？

- macOS：确保终端有访问剪贴板的权限
- Linux：可能需要安装 `xclip` 或 `xsel`
- Windows：通常无需额外配置

### 3. 数据存储在哪里？

所有数据存储在 `data/` 目录下：
- `data/logger.db`：SQLite 数据库
- `data/images/`：图片文件

### 4. 如何备份数据？

只需复制 `data/` 目录即可备份所有数据。

### 5. AI 分析结果不准确？

可以尝试：
- 提供更详细的文字描述
- 切换到 `gemini-1.5-pro` 模型（在 .env 中配置）

## 🛠️ 开发

### 管理工具

如果已全局安装，可以使用 Makefile 命令：

```bash
# 查看所有可用命令
make help

# 重新安装
make reinstall

# 卸载
make uninstall

# 检查状态
make status

# 清理临时文件
make clean
```

### 运行测试

测试各个命令：

```bash
# 测试添加功能
timeflow add --text "测试日志"

# 测试查询功能
timeflow list --today

# 测试统计功能
timeflow stats

# 测试 Web 界面
timeflow web
```

### 代码结构

- `cli.py`：命令行入口，使用 Click 框架
- `api/gemini.py`：Gemini API 封装
- `db/models.py`：SQLAlchemy 数据模型
- `db/operations.py`：数据库 CRUD 操作
- `web/app.py`：FastAPI Web 应用
- `utils/clipboard.py`：跨平台剪贴板处理

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式

如有问题或建议，请提交 Issue。

## 📚 文档索引

- **README.md** - 本文档，完整功能说明
- **[QUICKSTART.md](QUICKSTART.md)** - 快速入门指南
- **[SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)** - 详细安装说明 ⭐ 包含全局安装指南
- **[SHELL_COMPLETION.md](SHELL_COMPLETION.md)** - Shell 自动补全配置 ⭐ 新增
- **[INTERACTIVE_MODE_GUIDE.md](INTERACTIVE_MODE_GUIDE.md)** - 交互编辑模式详细指南
- **[USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)** - 实际使用示例集合
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - 项目技术摘要
- **Makefile** - 便捷管理命令（`make help` 查看）

---

⭐ 如果这个项目对你有帮助，请给它一个 Star！

