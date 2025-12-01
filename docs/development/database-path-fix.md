# 🔧 数据库路径问题修复说明

## 问题描述

在全局安装 logger 工具后，当在非项目目录执行命令时会出现以下错误：

```
❌ 发生错误：(sqlite3.OperationalError) unable to open database file
```

## 原因分析

原配置使用了相对路径 `./data/logger.db`，当在其他目录运行时，会尝试从当前工作目录查找数据库文件，导致找不到数据库。

## 解决方案

修改了 `config.py` 的路径解析逻辑：

### 1. 环境变量加载优化
- 优先从项目目录的 `.env` 文件加载配置
- 如果项目目录没有 `.env`，则从当前目录加载（兼容性）

### 2. 路径解析规则

#### 数据库路径（DATABASE_PATH）：
1. **如果设置了环境变量**：
   - 绝对路径：直接使用
   - 相对路径：相对于项目根目录（ROOT_DIR）解析
2. **如果未设置**：使用默认路径 `~/.logger/data/logger.db`

#### 图片存储路径（IMAGE_STORAGE_PATH）：
1. **如果设置了环境变量**：
   - 绝对路径：直接使用
   - 相对路径：相对于项目根目录（ROOT_DIR）解析
2. **如果未设置**：使用默认路径 `~/.logger/data/images`

## 现在的行为

### 场景 1：使用项目目录的 .env 配置（推荐）

你的 `.env` 文件：
```env
DATABASE_PATH=./data/logger.db
IMAGE_STORAGE_PATH=./data/images
```

实际使用的路径（会自动解析为绝对路径）：
- 数据库：`/Users/moego-better/Documents/Personal/codes/logger/data/logger.db`
- 图片：`/Users/moego-better/Documents/Personal/codes/logger/data/images`

**优点**：数据和项目代码在一起，便于管理和备份

### 场景 2：不设置路径（使用默认值）

如果 `.env` 中没有设置这些路径，会使用：
- 数据库：`~/.logger/data/logger.db`
- 图片：`~/.logger/data/images`

**优点**：
- 数据独立于项目目录
- 多个项目可以共享同一个数据库
- 更符合 Unix/Linux 应用的标准做法

### 场景 3：使用绝对路径（完全自定义）

```env
DATABASE_PATH=/path/to/my/custom/location/logger.db
IMAGE_STORAGE_PATH=/path/to/my/custom/location/images
```

**优点**：完全控制数据存储位置

## 验证修复

在任意目录运行以下命令都应该正常工作：

```bash
# 在主目录
cd ~
logger list --today

# 在临时目录
cd /tmp
logger stats --today

# 在任何其他目录
cd /path/to/anywhere
logger add --text "测试"
```

## 建议

### 开发模式
如果你在开发这个项目，建议保持当前的配置（使用相对路径），数据会存储在项目目录中。

### 日常使用模式
如果只是作为工具使用，可以考虑：

1. **使用默认路径**（推荐）：
   注释掉 `.env` 中的路径配置：
   ```env
   # DATABASE_PATH=./data/logger.db
   # IMAGE_STORAGE_PATH=./data/images
   ```
   数据会存储在 `~/.logger/data/`

2. **或使用绝对路径**：
   ```env
   DATABASE_PATH=/Users/moego-better/.logger/data/logger.db
   IMAGE_STORAGE_PATH=/Users/moego-better/.logger/data/images
   ```

### 迁移现有数据

如果要从项目目录迁移到 home 目录：

```bash
# 创建目标目录
mkdir -p ~/.logger/data

# 复制数据库
cp /Users/moego-better/Documents/Personal/codes/logger/data/logger.db ~/.logger/data/

# 复制图片
cp -r /Users/moego-better/Documents/Personal/codes/logger/data/images ~/.logger/data/

# 更新 .env（可选）
# 注释掉路径配置，使用默认值
```

## 技术细节

修改的核心代码逻辑：

```python
# 对于相对路径，相对于项目根目录解析
if _db_path:
    _db_path_obj = Path(_db_path)
    if _db_path_obj.is_absolute():
        DATABASE_PATH = str(_db_path_obj)
    else:
        # 相对路径：相对于 ROOT_DIR 解析
        DATABASE_PATH = str(ROOT_DIR / _db_path)
else:
    # 默认：使用 home 目录
    DATABASE_PATH = str(DEFAULT_DATA_DIR / "logger.db")
```

## 注意事项

1. **可编辑安装的优势**：因为使用了 `uv tool install --editable .`，代码修改立即生效，无需重新安装

2. **配置优先级**：
   - 环境变量 > .env 文件 > 默认值

3. **兼容性**：修改完全向后兼容，不影响现有配置

## 总结

✅ 问题已完全修复
✅ 可以在任何目录使用 logger 命令
✅ 支持相对路径、绝对路径和默认路径三种模式
✅ 向后兼容，不影响现有用户

