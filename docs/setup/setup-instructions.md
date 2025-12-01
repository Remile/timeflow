# 🎯 安装和设置说明

## 第一步：获取 Gemini API Key

1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 使用 Google 账号登录
3. 点击 "Create API Key"
4. 复制生成的 API Key

## 第二步：全局安装 Logger 工具

### 使用 uv tool（推荐）

这是最简单的方式，可以在任何目录直接使用 `logger` 命令：

```bash
# 进入项目目录
cd /Users/moego-better/Documents/Personal/codes/logger

# 安装为全局工具（可编辑模式，代码改动立即生效）
uv tool install --editable .
```

安装完成后，`logger` 命令将在任何目录都可用！

### 或使用 Makefile（更方便）

```bash
# 进入项目目录
cd /Users/moego-better/Documents/Personal/codes/logger

# 使用 make 命令安装
make install
```

## 第三步：配置 API Key

1. 创建 .env 文件：
```bash
cp .env.example .env
```

2. 编辑 .env 文件：
```bash
# 使用你喜欢的编辑器打开
nano .env
# 或
vim .env
# 或
open .env
```

3. 将 API Key 粘贴进去：
```env
GEMINI_API_KEY=你从Google AI Studio获取的实际API Key
```

## 第四步：验证安装

在**任意目录**运行以下命令测试：

```bash
logger --help
```

应该看到命令帮助信息。如果看到了，说明安装成功！✅

## 第五步：开始使用

现在你可以在**任何目录**直接使用 logger 命令：

### 添加第一条日志

```bash
# 方式1：交互式编辑模式（默认，推荐）
logger add

# 方式2：直接输入文字
logger add --text "开始使用生活日志工具"

# 方式3：指定图片
logger add --image /path/to/image.png
```

### 查看日志

```bash
# 查看最近 10 条日志
logger list

# 查看今天的日志
logger list --today

# 查看指定日期的日志
logger list --date 2025-12-01

# 按分类筛选
logger list --category 工作
```

### 查看统计

```bash
# 总体统计
logger stats

# 今日统计
logger stats --today

# 本周统计
logger stats --week

# 本月统计
logger stats --month
```

### 启动 Web 界面

```bash
logger web
```

然后在浏览器打开：http://127.0.0.1:8000

## 🎉 完成！

现在你可以开始记录你的生活日志了！

## 🚀 进阶配置

### 启用命令自动补全（强烈推荐）

在 `~/.zshrc` 文件末尾添加：

```bash
# Logger 命令自动补全
eval "$(_LOGGER_COMPLETE=zsh_source logger)"
```

然后重新加载配置：
```bash
source ~/.zshrc
```

现在按 Tab 键就可以自动补全命令和选项了！详见 [shell-completion.md](../user-guide/shell-completion.md)

### 创建快捷别名（可选）

如果你觉得 `logger` 太长，可以创建更短的别名：

```bash
# 在 ~/.zshrc 或 ~/.bashrc 中添加
alias log='logger'
alias la='logger add'
alias ll='logger list'
alias ls='logger stats'
```

然后重新加载配置：
```bash
source ~/.zshrc  # 或 source ~/.bashrc
```

之后就可以使用更简短的命令：
```bash
la              # 添加日志
ll --today      # 查看今天的日志
ls --week       # 查看本周统计
log web         # 启动 Web 界面
```

## 📚 更多帮助

- 查看完整文档：[README.md](../../README.md)
- 快速入门：[quickstart.md](../user-guide/quickstart.md)
- 项目摘要：[project-summary.md](../development/project-summary.md)

