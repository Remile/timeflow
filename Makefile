.PHONY: install uninstall reinstall test clean help

help:  ## 显示帮助信息
	@echo "Logger 项目管理命令："
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## 安装 logger 工具（可编辑模式）
	@echo "📦 安装 logger 工具..."
	uv tool install --editable .
	@echo "✅ 安装完成！现在可以在任何目录使用 'logger' 命令"

uninstall:  ## 卸载 logger 工具
	@echo "🗑️  卸载 logger 工具..."
	uv tool uninstall logger
	@echo "✅ 卸载完成"

reinstall:  ## 重新安装 logger 工具
	@echo "🔄 重新安装 logger 工具..."
	uv tool install --reinstall --editable .
	@echo "✅ 重新安装完成"

upgrade:  ## 升级 logger 工具
	@echo "⬆️  升级 logger 工具..."
	uv tool upgrade logger
	@echo "✅ 升级完成"

dev:  ## 安装开发依赖
	@echo "🔧 安装开发环境..."
	uv sync --all-extras --dev
	@echo "✅ 开发环境准备完成"

test:  ## 运行测试（如果有的话）
	@echo "🧪 运行测试..."
	@echo "⚠️  暂无测试"

clean:  ## 清理临时文件
	@echo "🧹 清理临时文件..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ 清理完成"

status:  ## 检查 logger 工具状态
	@echo "📊 Logger 工具状态："
	@echo ""
	@if command -v logger >/dev/null 2>&1; then \
		echo "✅ logger 命令已安装"; \
		echo ""; \
		echo "版本信息："; \
		uv tool list | grep logger || echo "未找到版本信息"; \
	else \
		echo "❌ logger 命令未安装"; \
		echo ""; \
		echo "运行 'make install' 来安装"; \
	fi

build:  ## 构建分发包
	@echo "📦 构建分发包..."
	uv build
	@echo "✅ 构建完成，文件位于 dist/ 目录"

publish:  ## 发布到 PyPI
	@echo "🚀 发布到 PyPI..."
	uv publish
	@echo "✅ 发布完成"

