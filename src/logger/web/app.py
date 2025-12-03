"""FastAPI web application for the logger."""
from datetime import datetime, timedelta
from typing import Optional, List
from pathlib import Path

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ..config import config
from ..db.models import init_database, get_session
from ..db.operations import LogOperations

# Initialize FastAPI app
app = FastAPI(title="Life Logger", description="Personal life logging tool with AI analysis")

# Setup templates and static files
template_dir = Path(__file__).parent / "templates"
static_dir = Path(__file__).parent / "static"
templates = Jinja2Templates(directory=str(template_dir))

# Mount static files
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Initialize database
engine = init_database(config.get_database_url())


def get_log_operations():
    """Get LogOperations instance."""
    session = get_session(engine)
    return LogOperations(session)


@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 50,
):
    """Home page with log timeline."""
    ops = get_log_operations()
    
    # Parse dates
    start = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    
    # Get logs
    logs = ops.get_logs(
        limit=limit,
        category=category,
        start_date=start,
        end_date=end,
    )
    
    # Get unique categories for filter
    all_logs = ops.get_logs(limit=1000)
    categories = sorted(set(log.category for log in all_logs))
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "logs": logs,
            "categories": categories,
            "selected_category": category,
            "start_date": start_date,
            "end_date": end_date,
        }
    )


@app.get("/stats", response_class=HTMLResponse)
async def stats_page(
    request: Request,
    period: str = "all",
):
    """Statistics page."""
    ops = get_log_operations()
    
    # Determine time range
    start_date = None
    end_date = None
    
    if period == "today":
        start_date = datetime.now().replace(hour=0, minute=0, second=0)
        period_name = "今日"
    elif period == "week":
        start_date = datetime.now() - timedelta(days=datetime.now().weekday())
        start_date = start_date.replace(hour=0, minute=0, second=0)
        period_name = "本周"
    elif period == "month":
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0)
        period_name = "本月"
    else:
        period_name = "全部"
    
    # Get statistics
    stats = ops.get_statistics(start_date=start_date, end_date=end_date)
    
    return templates.TemplateResponse(
        "stats.html",
        {
            "request": request,
            "stats": stats,
            "period": period,
            "period_name": period_name,
        }
    )


@app.get("/api/logs")
async def api_get_logs(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """API endpoint to get logs."""
    ops = get_log_operations()
    
    # Parse dates
    start = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    
    # Get logs
    logs = ops.get_logs(
        limit=limit,
        offset=offset,
        category=category,
        start_date=start,
        end_date=end,
    )
    
    return {
        "logs": [log.to_dict() for log in logs],
        "count": len(logs),
    }


@app.get("/api/stats")
async def api_get_stats(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """API endpoint to get statistics."""
    ops = get_log_operations()
    
    # Parse dates
    start = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    
    # Get statistics
    stats = ops.get_statistics(start_date=start, end_date=end)
    
    return stats


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


