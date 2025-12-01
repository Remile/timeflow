"""Command-line interface for the logger application."""
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import config
from .db.models import init_database, get_session
from .db.operations import LogOperations
from .api.gemini import GeminiAnalyzer
from .utils.clipboard import ClipboardHandler

console = Console()


def _interactive_edit_mode(clipboard_handler):
    """Interactive edit mode for adding content."""
    console.print("\n[bold cyan]📝 交互编辑模式[/bold cyan]")
    console.print("[dim]你可以多次粘贴文字和图片，输入 'done' 或按 Ctrl+D 完成[/dim]\n")
    
    collected_texts = []
    collected_images = []
    paste_count = 0
    
    while True:
        paste_count += 1
        console.print(f"[yellow]第 {paste_count} 次粘贴 - 请粘贴内容后按回车（输入 'done' 完成）：[/yellow]")
        
        try:
            user_input = input().strip()
            
            # Check if user wants to finish
            if user_input.lower() == 'done':
                break
            
            # If user typed something, use it as text
            if user_input:
                collected_texts.append(user_input)
                console.print(f"[green]✓ 已添加文字：{user_input[:50]}{'...' if len(user_input) > 50 else ''}[/green]")
            
            # Try to get image from clipboard
            console.print("[dim]检查剪贴板中的图片...[/dim]")
            image_path = clipboard_handler.get_image()
            if image_path:
                collected_images.append(image_path)
                console.print(f"[green]✓ 已添加图片：{image_path}[/green]")
            
            # If nothing was collected this round, try to get text from clipboard
            if not user_input and not image_path:
                clipboard_text = clipboard_handler.get_text()
                if clipboard_text:
                    collected_texts.append(clipboard_text)
                    console.print(f"[green]✓ 已添加剪贴板文字：{clipboard_text[:50]}{'...' if len(clipboard_text) > 50 else ''}[/green]")
                else:
                    console.print("[yellow]⚠️  没有检测到内容，请重新粘贴[/yellow]")
            
            console.print()
            
        except EOFError:
            # Ctrl+D pressed
            break
        except KeyboardInterrupt:
            console.print("\n[yellow]已取消[/yellow]")
            sys.exit(0)
    
    # Combine collected content
    final_text = "\n\n".join(collected_texts) if collected_texts else None
    final_image = collected_images[0] if collected_images else None  # Use first image for now
    
    if collected_texts or collected_images:
        console.print("\n[bold green]✓ 收集完成！[/bold green]")
        console.print(f"  - 文字段落：{len(collected_texts)} 段")
        console.print(f"  - 图片：{len(collected_images)} 张")
        if len(collected_images) > 1:
            console.print(f"[dim]  注意：暂时只使用第一张图片[/dim]")
        console.print()
    
    return final_text, final_image


@click.group()
def cli():
    """生活日志追踪工具 - 用AI分析你的日常活动"""
    pass


@cli.command()
@click.option("--text", "-t", help="直接指定文字内容")
@click.option("--image", "-i", type=click.Path(exists=True), help="指定图片路径")
@click.option("--edit", "-e", is_flag=True, default=True, help="进入交互编辑模式（默认）")
@click.option("--no-edit", is_flag=True, help="直接从剪贴板读取，不进入编辑模式")
def add(text: Optional[str], image: Optional[str], edit: bool, no_edit: bool):
    """添加新的日志记录"""
    try:
        # Validate configuration
        config.validate()
        
        # Initialize components
        clipboard_handler = ClipboardHandler(config.IMAGE_STORAGE_PATH)
        
        # Determine mode
        use_edit_mode = edit and not no_edit and not text and not image
        
        # Get content from clipboard or parameters
        if text or image:
            # Direct mode with parameters
            pass
        elif use_edit_mode:
            # Interactive edit mode
            text, image = _interactive_edit_mode(clipboard_handler)
        else:
            # Quick mode: read from clipboard once
            console.print("[yellow]从剪贴板读取内容...[/yellow]")
            text, image = clipboard_handler.get_content()
        
        if not text and not image:
            console.print("[red]❌ 错误：没有找到任何内容！[/red]")
            console.print("请先复制一些文字或图片，或使用 --text 或 --image 参数。")
            sys.exit(1)
        
        # Show what we got
        if text:
            preview = text[:100] + "..." if len(text) > 100 else text
            console.print(f"[green]📝 文字内容：[/green]{preview}")
        if image:
            console.print(f"[green]🖼️  图片：[/green]{image}")
        
        # Analyze content with Gemini
        console.print("\n[yellow]🤖 正在使用 Gemini AI 分析内容...[/yellow]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("分析中...", total=None)
            
            analyzer = GeminiAnalyzer(config.GEMINI_API_KEY, config.GEMINI_MODEL)
            result = analyzer.analyze_content(text=text, image_path=image)
            
            progress.update(task, completed=True)
        
        # Display analysis results
        console.print("\n[bold cyan]📊 分析结果：[/bold cyan]")
        result_table = Table(show_header=False, box=box.ROUNDED, show_edge=False)
        result_table.add_column("Field", style="cyan")
        result_table.add_column("Value", style="white")
        
        result_table.add_row("总结", result["summary"])
        result_table.add_row("分类", f"[bold]{result['category']}[/bold]")
        result_table.add_row("标签", ", ".join(result["tags"]) if result["tags"] else "无")
        result_table.add_row("预计耗时", f"{result['duration_estimate']} 分钟")
        
        console.print(result_table)
        
        # Save to database
        console.print("\n[yellow]💾 保存到数据库...[/yellow]")
        engine = init_database(config.get_database_url())
        session = get_session(engine)
        ops = LogOperations(session)
        
        # Auto-update previous log's duration before creating new log
        new_log_time = datetime.now()
        update_result = ops.auto_update_previous_log_duration(new_log_time)
        
        if update_result:
            prev_log, calculated_duration = update_result
            console.print(f"[cyan]⏱  已自动更新上一条日志 (ID: {prev_log.id}) 的时长：{calculated_duration} 分钟[/cyan]")
        
        log = ops.create_log(
            original_text=text,
            image_path=image,
            ai_summary=result["summary"],
            category=result["category"],
            tags=result["tags"],
            duration_estimate=result["duration_estimate"],
        )
        
        console.print(f"[green]✅ 日志已保存！ (ID: {log.id})[/green]")
        
        if "error" in result or "parse_error" in result:
            console.print("[yellow]⚠️  注意：AI分析过程中出现了一些问题，但仍然保存了基本信息。[/yellow]")
    
    except ValueError as e:
        console.print(f"[red]❌ 配置错误：{e}[/red]")
        console.print("\n请确保已设置 GEMINI_API_KEY 环境变量或在 .env 文件中配置。")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ 发生错误：{e}[/red]")
        sys.exit(1)


@cli.command()
@click.option("--limit", "-l", default=10, help="显示的日志数量")
@click.option("--today", is_flag=True, help="显示今天的日志")
@click.option("--date", "-d", help="显示指定日期的日志 (格式: YYYY-MM-DD)")
@click.option("--range", "-r", "date_range", nargs=2, help="显示日期范围内的日志")
@click.option("--category", "-c", help="按分类筛选")
def list(limit: int, today: bool, date: Optional[str], date_range: Optional[tuple], category: Optional[str]):
    """查询日志记录"""
    try:
        # Initialize database
        engine = init_database(config.get_database_url())
        session = get_session(engine)
        ops = LogOperations(session)
        
        # Determine query parameters
        start_date = None
        end_date = None
        
        if today:
            logs = ops.get_logs_today()
            title = "📅 今天的日志"
        elif date:
            target_date = datetime.strptime(date, "%Y-%m-%d")
            logs = ops.get_logs_by_date(target_date)
            title = f"📅 {date} 的日志"
        elif date_range:
            start_date = datetime.strptime(date_range[0], "%Y-%m-%d")
            end_date = datetime.strptime(date_range[1], "%Y-%m-%d")
            logs = ops.get_logs(limit=1000, category=category, start_date=start_date, end_date=end_date)
            title = f"📅 {date_range[0]} 至 {date_range[1]} 的日志"
        else:
            logs = ops.get_logs(limit=limit, category=category)
            title = f"📋 最近 {limit} 条日志" + (f" (分类: {category})" if category else "")
        
        if not logs:
            console.print("[yellow]没有找到符合条件的日志记录。[/yellow]")
            return
        
        # Display logs
        console.print(f"\n[bold cyan]{title}[/bold cyan]\n")
        
        for log in logs:
            # Create a panel for each log
            content_lines = []
            
            # Time
            time_str = log.created_at.strftime("%Y-%m-%d %H:%M:%S")
            content_lines.append(f"[dim]时间：{time_str}[/dim]")
            
            # Summary
            content_lines.append(f"\n[bold]{log.ai_summary}[/bold]")
            
            # Original text (preview)
            if log.original_text:
                preview = log.original_text[:150] + "..." if len(log.original_text) > 150 else log.original_text
                content_lines.append(f"\n[dim]原文：{preview}[/dim]")
            
            # Image
            if log.image_path:
                content_lines.append(f"\n[dim]🖼️  {log.image_path}[/dim]")
            
            # Metadata
            meta = []
            meta.append(f"[cyan]#{log.id}[/cyan]")
            meta.append(f"[magenta]{log.category}[/magenta]")
            if log.tags:
                meta.append(f"[blue]{', '.join(log.tags)}[/blue]")
            if log.duration_estimate:
                meta.append(f"[yellow]⏱ {log.duration_estimate}分钟[/yellow]")
            
            content_lines.append("\n" + " | ".join(meta))
            
            panel = Panel(
                "\n".join(content_lines),
                border_style="cyan",
                box=box.ROUNDED,
            )
            console.print(panel)
        
        console.print(f"\n[green]共 {len(logs)} 条记录[/green]")
    
    except Exception as e:
        console.print(f"[red]❌ 发生错误：{e}[/red]")
        sys.exit(1)


@cli.command()
@click.option("--today", is_flag=True, help="今日统计")
@click.option("--week", is_flag=True, help="本周统计")
@click.option("--month", is_flag=True, help="本月统计")
def stats(today: bool, week: bool, month: bool):
    """查看统计信息"""
    try:
        # Initialize database
        engine = init_database(config.get_database_url())
        session = get_session(engine)
        ops = LogOperations(session)
        
        # Determine time range
        if today:
            logs = ops.get_logs_today()
            title = "📊 今日统计"
            start_date = datetime.now().replace(hour=0, minute=0, second=0)
            end_date = None
        elif week:
            logs = ops.get_logs_this_week()
            title = "📊 本周统计"
            start_date = datetime.now() - timedelta(days=datetime.now().weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0)
            end_date = None
        elif month:
            logs = ops.get_logs_this_month()
            title = "📊 本月统计"
            start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0)
            end_date = None
        else:
            start_date = None
            end_date = None
            title = "📊 总体统计"
        
        stats_data = ops.get_statistics(start_date=start_date, end_date=end_date)
        
        console.print(f"\n[bold cyan]{title}[/bold cyan]\n")
        
        # Overview
        overview = Table(show_header=False, box=box.ROUNDED)
        overview.add_column("Metric", style="cyan")
        overview.add_column("Value", style="white", justify="right")
        
        overview.add_row("总日志数", f"[bold]{stats_data['total_logs']}[/bold] 条")
        overview.add_row("总耗时", f"[bold]{stats_data['total_duration_minutes']}[/bold] 分钟 ({stats_data['total_duration_minutes'] / 60:.1f} 小时)")
        
        console.print(overview)
        console.print()
        
        # Category distribution
        if stats_data['category_counts']:
            console.print("[bold cyan]📁 分类分布[/bold cyan]")
            
            category_table = Table(box=box.ROUNDED)
            category_table.add_column("分类", style="magenta")
            category_table.add_column("数量", justify="right", style="cyan")
            category_table.add_column("耗时", justify="right", style="yellow")
            category_table.add_column("占比", justify="right", style="green")
            
            for category, count in sorted(stats_data['category_counts'].items(), key=lambda x: x[1], reverse=True):
                duration = stats_data['duration_by_category'].get(category, 0)
                percentage = (count / stats_data['total_logs'] * 100) if stats_data['total_logs'] > 0 else 0
                category_table.add_row(
                    category,
                    str(count),
                    f"{duration} 分钟",
                    f"{percentage:.1f}%"
                )
            
            console.print(category_table)
            console.print()
        
        # Top tags
        if stats_data['top_tags']:
            console.print("[bold cyan]🏷️  热门标签[/bold cyan]")
            
            tags_table = Table(box=box.ROUNDED, show_header=False)
            tags_table.add_column("Tag", style="blue")
            tags_table.add_column("Count", justify="right", style="cyan")
            
            # Sort tags by count and get top 10
            sorted_tags = sorted(stats_data['top_tags'].items(), key=lambda x: x[1], reverse=True)[:10]
            for tag, count in sorted_tags:
                tags_table.add_row(tag, str(count))
            
            console.print(tags_table)
    
    except Exception as e:
        console.print(f"[red]❌ 发生错误：{e}[/red]")
        sys.exit(1)


@cli.command()
@click.option("--port", "-p", default=8000, help="Web服务器端口")
@click.option("--host", "-h", default="127.0.0.1", help="Web服务器主机")
def web(port: int, host: str):
    """启动Web界面"""
    try:
        import uvicorn
        from .web.app import app
        
        console.print(f"\n[bold cyan]🚀 启动 Web 界面...[/bold cyan]")
        console.print(f"[green]访问地址：http://{host}:{port}[/green]")
        console.print("[dim]按 Ctrl+C 停止服务器[/dim]\n")
        
        uvicorn.run(app, host=host, port=port, log_level="info")
    
    except ImportError:
        console.print("[red]❌ 错误：无法导入 Web 应用模块[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ 发生错误：{e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    cli()

