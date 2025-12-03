# 🚀 快速入门指南

> 📝 **注意**：本指南假设你已全局安装了 logger 工具。如果还没有安装，请先查看 [安装说明](SETUP_INSTRUCTIONS.md)

## 第一步：全局安装（推荐）

### 1. 安装 logger 工具

```bash
cd /path/to/logger
uv tool install --editable .

# 或使用 Makefile
make install
```

### 2. 配置 API Key

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env`，添加你的 Gemini API Key：

```env
GEMINI_API_KEY=你的实际API密钥
```

💡 获取 API Key：https://makersuite.google.com/app/apikey

### 3. 验证安装

在任意目录运行：

```bash
timeflow --help
```

看到帮助信息说明安装成功！✅

## 第二步：添加第一条日志

### 方式 1：交互编辑模式（推荐✨）

运行命令进入交互模式：

```bash
timeflow add
```

然后你可以：

1. **粘贴文字**：直接粘贴或输入文字，按回车
2. **粘贴图片**：从截图或复制的图片粘贴
3. **多次粘贴**：可以添加多段文字和图片
4. **完成输入**：输入 `done` 或按 `Ctrl+D`

示例流程：
```
第 1 次粘贴 - 请粘贴内容后按回车（输入 'done' 完成）：
今天学习了 Python 装饰器
✓ 已添加文字：今天学习了 Python 装饰器

第 2 次粘贴 - 请粘贴内容后按回车（输入 'done' 完成）：
[粘贴代码截图]
✓ 已添加图片：/path/to/image.png

第 3 次粘贴 - 请粘贴内容后按回车（输入 'done' 完成）：
done

✓ 收集完成！
  - 文字段落：1 段
  - 图片：1 张
```

### 方式 2：快速模式

先复制内容，然后快速添加：

```bash
timeflow add --no-edit
```

### 方式 3：直接输入

```bash
timeflow add --text "正在编写项目文档"
```

### 方式 4：指定图片

```bash
timeflow add --image /path/to/screenshot.png
```

## 第三步：查看日志

### 查看今天的日志

```bash
timeflow list --today
```

### 查看最近 20 条

```bash
timeflow list --limit 20
```

### 按分类查看

```bash
timeflow list --category 工作
```

## 第四步：查看统计

### 今日统计

```bash
timeflow stats --today
```

你会看到：
- 今天记录的日志数量
- 各类活动的时间分布
- 最常用的标签
- 总耗时统计

### 本周统计

```bash
timeflow stats --week
```

## 第五步：使用 Web 界面

启动 Web 服务器：

```bash
timeflow web
```

然后在浏览器访问：http://127.0.0.1:8000

### Web 界面功能

- **时间线页面**：查看所有日志，可按日期、分类筛选
- **统计页面**：可视化图表展示统计数据

## 实际使用场景

### 场景 1：学习记录

```bash
# 运行命令进入交互模式
timeflow add

# 第 1 次粘贴：文章标题和摘要
# 第 2 次粘贴：文章截图
# 第 3 次粘贴：自己的学习笔记
# 输入 done 完成

# AI 会自动分析并记录：
# - 分类：学习
# - 标签：Python, 教程, 编程
# - 预计耗时：20分钟
```

### 场景 2：工作任务

```bash
# 进入交互模式
timeflow add

# 粘贴任务描述、需求文档截图、相关链接
# 一次性记录完整的任务信息
# 输入 done 完成

# 周末查看本周工作统计
timeflow stats --week
```

### 场景 3：娱乐追踪

```bash
# 看视频、玩游戏时记录一下
timeflow add --text "观看《三体》第三集"

# 月底查看娱乐时间占比
timeflow stats --month
```

## 每日工作流建议

### 早晨

```bash
# 查看昨天的日志，计划今天
timeflow list --limit 10
```

### 工作中

- 每次切换任务时，复制任务描述并运行 `timeflow add`
- 看到重要信息时，截图并运行 `timeflow add`
- 💡 提示：按 Tab 键使用命令自动补全

### 晚上

```bash
# 回顾今天的活动
timeflow stats --today

# 启动 Web 界面深度分析
timeflow web
```

### 周末

```bash
# 查看本周统计
timeflow stats --week

# 通过 Web 界面查看图表
timeflow web
# 访问 http://127.0.0.1:8000/stats
```

## 高级技巧

### 1. 启用命令自动补全（强烈推荐）

在 `~/.zshrc` 文件末尾添加：

```bash
# Logger 命令自动补全
eval "$(_LOGGER_COMPLETE=zsh_source logger)"
```

重新加载配置：

```bash
source ~/.zshrc
```

现在按 Tab 键就可以自动补全命令和选项了！详见 [SHELL_COMPLETION.md](SHELL_COMPLETION.md)

### 2. 创建快捷别名

在 `~/.zshrc` 或 `~/.bashrc` 中添加：

```bash
alias la='timeflow add'
alias ll='timeflow list'
alias ls='timeflow stats'
```

然后就可以使用更简短的命令：

```bash
la              # 添加日志
ll --today      # 查看今天的日志
ls --week       # 查看本周统计
```

### 3. 快速查询特定日期

```bash
timeflow list --date 2025-11-27
```

### 4. 查看日期范围

```bash
timeflow list --range 2025-11-01 2025-11-30
```

### 5. 数据备份

定期备份 `data/` 目录：

```bash
cp -r data/ ~/Backups/logger-backup-$(date +%Y%m%d)
```

### 6. 使用 Makefile 管理

```bash
# 查看所有可用命令
make help

# 检查工具状态
make status

# 重新安装
make reinstall
```

## 常见问题

### Q: 剪贴板读取失败？

**A:** macOS 用户需要给终端授予剪贴板访问权限。如果还是不行，可以使用 `--text` 参数直接输入。

### Q: AI 分析结果不满意？

**A:** 可以尝试：
1. 提供更详细的文字描述
2. 修改 `.env` 中的模型为 `gemini-1.5-pro`（更准确但更慢）

### Q: 如何删除日志？

**A:** 目前需要直接操作数据库，或者使用 SQLite 工具。

### Q: 数据存在哪里？

**A:** 所有数据在 `data/` 目录：
- `data/logger.db` - 数据库
- `data/images/` - 图片文件

## 下一步

- 养成记录的习惯，每天至少记录 3-5 条
- 每周查看统计，分析时间使用
- 通过 Web 界面深度探索数据
- 根据分析结果优化时间分配

---

🎉 开始记录你的生活日志吧！

