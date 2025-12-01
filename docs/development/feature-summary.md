# ✨ 新功能：交互编辑模式

## 🎯 功能概述

现在运行 `uv run logger add` 时，会默认进入**交互编辑模式**，让你可以：

✅ 在一次输入中多次粘贴内容  
✅ 混合粘贴文字和图片  
✅ 从不同来源收集信息  
✅ 更灵活地记录复杂活动  

## 🚀 快速开始

### 基础用法

```bash
# 运行命令
uv run logger add

# 会看到提示
📝 交互编辑模式
你可以多次粘贴文字和图片，输入 'done' 或按 Ctrl+D 完成

# 粘贴第一部分内容
第 1 次粘贴 - 请粘贴内容后按回车（输入 'done' 完成）：
[粘贴内容并按回车]

# 粘贴更多内容
第 2 次粘贴 - 请粘贴内容后按回车（输入 'done' 完成）：
[继续粘贴]

# 完成输入
第 3 次粘贴 - 请粘贴内容后按回车（输入 'done' 完成）：
done

# AI 自动分析并保存
🤖 正在使用 Gemini AI 分析内容...
✅ 日志已保存！
```

## 📋 典型使用场景

### 场景 1：学习编程

```bash
$ uv run logger add

# 第 1 次：复制教程标题
学习 Python 装饰器高级用法

# 第 2 次：截图示例代码
[Cmd+Shift+4 截图并粘贴]

# 第 3 次：输入自己的理解
关键点：@wraps 保留原函数的元信息

# 输入 done 完成
```

### 场景 2：工作任务

```bash
$ uv run logger add

# 从项目管理系统复制任务
修复登录页面响应式布局问题

# 粘贴设计稿截图
[粘贴图片]

# 添加技术方案
使用 flexbox 重构布局，兼容移动端

# 完成
done
```

### 场景 3：阅读笔记

```bash
$ uv run logger add

# 书籍章节
阅读《深入理解计算机系统》第三章

# 关键观点
虚拟内存是现代操作系统的核心抽象

# 个人思考  
理解了地址翻译的过程

# 完成
done
```

## 🔄 如何切换模式

### 默认：交互模式

```bash
uv run logger add
```

### 快速模式：直接从剪贴板读取

```bash
uv run logger add --no-edit
```

### 直接指定内容

```bash
uv run logger add --text "内容"
uv run logger add --image "图片.png"
```

## ⌨️ 快捷操作

| 操作 | 说明 |
|------|------|
| `Enter` | 确认当前粘贴 |
| `done` + `Enter` | 完成输入 |
| `Ctrl+D` | 快速完成 |
| `Ctrl+C` | 取消操作 |

## 💡 使用技巧

### 1. 准备工作流
- 打开要记录的内容（网页、文档、代码）
- 运行 `logger add`
- 依次复制粘贴各部分内容
- 输入 `done` 完成

### 2. 多窗口协作
- 终端窗口：运行 logger
- 浏览器/编辑器：准备内容
- 来回切换复制粘贴

### 3. 截图技巧 (macOS)
```bash
Cmd + Shift + 4         # 区域截图到文件
Cmd + Shift + Ctrl + 4  # 截图到剪贴板（推荐）
```

## 📚 详细文档

- **[interactive-mode.md](../user-guide/interactive-mode.md)** - 完整的交互模式指南
- **[usage-examples.md](../user-guide/usage-examples.md)** - 更多实际使用示例
- **[quickstart.md](../user-guide/quickstart.md)** - 快速入门教程

## ❓ 常见问题

**Q: 如何使用旧的行为（直接从剪贴板读取）？**  
A: 使用 `uv run logger add --no-edit`

**Q: 可以粘贴多少次？**  
A: 没有限制，但建议每次记录保持在 10 次以内

**Q: 能编辑已经粘贴的内容吗？**  
A: 目前不支持，可以按 `Ctrl+C` 取消后重新开始

**Q: 多张图片怎么处理？**  
A: 目前使用第一张图片，未来版本会支持多图片

**Q: 我更喜欢旧的方式，能改回去吗？**  
A: 可以，使用 `--no-edit` 标志，或创建别名：
```bash
alias quicklog='uv run logger add --no-edit'
```

## 🎉 反馈

如果你有任何建议或发现问题，欢迎提交 Issue！

---

**版本**: v0.2.0  
**发布日期**: 2025-11-27  
**状态**: ✅ 稳定

