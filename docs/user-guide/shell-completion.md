# Shell 自动补全配置

为 logger 命令启用 shell 自动补全功能，可以让你更高效地使用命令行工具。

## 🐚 支持的 Shell

- Bash
- Zsh (推荐)
- Fish

## 📝 Zsh 配置（推荐）

如果你使用 Zsh（macOS 默认 shell），按以下步骤配置：

### 方法 1：直接添加到 ~/.zshrc（推荐）

在你的 `~/.zshrc` 文件末尾添加以下内容：

```bash
# Logger 命令自动补全
eval "$(_LOGGER_COMPLETE=zsh_source logger)"
```

然后重新加载配置：

```bash
source ~/.zshrc
```

### 方法 2：生成补全脚本文件

如果你想要更好的性能，可以生成静态补全文件：

```bash
# 创建补全目录（如果不存在）
mkdir -p ~/.zsh/completion

# 生成补全脚本
_LOGGER_COMPLETE=zsh_source logger > ~/.zsh/completion/_logger

# 在 ~/.zshrc 中添加
fpath=(~/.zsh/completion $fpath)
autoload -Uz compinit && compinit
```

## 🐚 Bash 配置

在你的 `~/.bashrc` 或 `~/.bash_profile` 中添加：

```bash
# Logger 命令自动补全
eval "$(_LOGGER_COMPLETE=bash_source logger)"
```

然后重新加载：

```bash
source ~/.bashrc
```

## 🐟 Fish 配置

在你的 `~/.config/fish/completions/` 目录中创建 `logger.fish` 文件：

```bash
# 创建目录
mkdir -p ~/.config/fish/completions

# 生成补全文件
env _LOGGER_COMPLETE=fish_source logger > ~/.config/fish/completions/logger.fish
```

## ✨ 使用自动补全

配置完成后，你可以：

1. **命令补全**：输入 `logger ` 后按 Tab 键，查看可用的子命令
   ```bash
   logger <Tab>
   # 显示：add  list  stats  web
   ```

2. **选项补全**：输入 `timeflow add -` 后按 Tab 键，查看可用的选项
   ```bash
   timeflow add -<Tab>
   # 显示：-t  --text  -i  --image  -e  --edit  --no-edit
   ```

3. **参数提示**：某些命令会显示参数提示和说明

## 🔍 验证配置

运行以下命令验证自动补全是否正常工作：

```bash
# 尝试补全
logger <Tab>

# 尝试选项补全
timeflow list --<Tab>
```

如果看到补全建议，说明配置成功！

## ⚠️ 故障排除

### 补全不工作

1. **确保 logger 已安装**：
   ```bash
   which logger
   # 应该显示：/Users/你的用户名/.local/bin/logger
   ```

2. **重新加载 shell 配置**：
   ```bash
   # Zsh
   source ~/.zshrc
   
   # Bash
   source ~/.bashrc
   ```

3. **检查 Click 版本**：
   ```bash
   uv pip show click
   # 确保版本 >= 8.0
   ```

### Zsh compinit 错误

如果遇到 "compinit: insecure directories" 错误：

```bash
# 修复权限
compaudit | xargs chmod g-w
```

## 💡 提示

- 自动补全功能基于 Click 框架的内置支持
- 首次使用可能需要按两次 Tab 键
- 补全脚本会随着命令更新自动变化（使用 eval 方法）
- 如果使用静态文件方法，更新命令后需要重新生成补全文件

