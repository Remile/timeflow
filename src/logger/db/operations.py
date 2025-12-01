"""Database CRUD operations for the logger application."""
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from collections import Counter

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from .models import Log


class LogOperations:
    """Database operations for Log entries."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_log(
        self,
        ai_summary: str,
        category: str,
        original_text: Optional[str] = None,
        image_path: Optional[str] = None,
        tags: Optional[List[str]] = None,
        duration_estimate: Optional[int] = None,
    ) -> Log:
        """Create a new log entry."""
        log = Log(
            original_text=original_text,
            image_path=image_path,
            ai_summary=ai_summary,
            category=category,
            tags=tags or [],
            duration_estimate=duration_estimate,
        )
        self.session.add(log)
        self.session.commit()
        self.session.refresh(log)
        return log
    
    def get_log_by_id(self, log_id: int) -> Optional[Log]:
        """Get a log entry by ID."""
        return self.session.query(Log).filter(Log.id == log_id).first()
    
    def get_logs(
        self,
        limit: int = 10,
        offset: int = 0,
        category: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Log]:
        """Get log entries with optional filters."""
        query = self.session.query(Log)
        
        # Apply filters
        if category:
            query = query.filter(Log.category == category)
        
        if start_date:
            query = query.filter(Log.created_at >= start_date)
        
        if end_date:
            # Include the entire end date
            end_datetime = end_date.replace(hour=23, minute=59, second=59)
            query = query.filter(Log.created_at <= end_datetime)
        
        # Order by most recent first
        query = query.order_by(Log.created_at.desc())
        
        # Apply pagination
        query = query.limit(limit).offset(offset)
        
        return query.all()
    
    def get_logs_by_date(self, date: datetime) -> List[Log]:
        """Get all logs for a specific date."""
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        return self.session.query(Log).filter(
            and_(
                Log.created_at >= start_of_day,
                Log.created_at <= end_of_day
            )
        ).order_by(Log.created_at.desc()).all()
    
    def get_logs_today(self) -> List[Log]:
        """Get all logs for today."""
        return self.get_logs_by_date(datetime.now())
    
    def get_logs_this_week(self) -> List[Log]:
        """Get all logs for the current week."""
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        
        return self.session.query(Log).filter(
            Log.created_at >= start_of_week
        ).order_by(Log.created_at.desc()).all()
    
    def get_logs_this_month(self) -> List[Log]:
        """Get all logs for the current month."""
        today = datetime.now()
        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        return self.session.query(Log).filter(
            Log.created_at >= start_of_month
        ).order_by(Log.created_at.desc()).all()
    
    def delete_log(self, log_id: int) -> bool:
        """Delete a log entry."""
        log = self.get_log_by_id(log_id)
        if log:
            self.session.delete(log)
            self.session.commit()
            return True
        return False
    
    def get_statistics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Get statistics for logs."""
        query = self.session.query(Log)
        
        # Apply date filters
        if start_date:
            query = query.filter(Log.created_at >= start_date)
        
        if end_date:
            end_datetime = end_date.replace(hour=23, minute=59, second=59)
            query = query.filter(Log.created_at <= end_datetime)
        
        logs = query.all()
        
        # Calculate statistics
        total_logs = len(logs)
        
        # Category distribution
        categories = [log.category for log in logs]
        category_counts = dict(Counter(categories))
        
        # Total duration
        total_duration = sum(
            log.duration_estimate for log in logs if log.duration_estimate
        )
        
        # Duration by category
        duration_by_category = {}
        for log in logs:
            if log.duration_estimate:
                if log.category not in duration_by_category:
                    duration_by_category[log.category] = 0
                duration_by_category[log.category] += log.duration_estimate
        
        # Top tags
        all_tags = []
        for log in logs:
            if log.tags:
                all_tags.extend(log.tags)
        tag_counts = dict(Counter(all_tags).most_common(10))
        
        # Daily log counts
        daily_counts = {}
        for log in logs:
            date_key = log.created_at.date().isoformat()
            daily_counts[date_key] = daily_counts.get(date_key, 0) + 1
        
        return {
            "total_logs": total_logs,
            "category_counts": category_counts,
            "total_duration_minutes": total_duration,
            "duration_by_category": duration_by_category,
            "top_tags": tag_counts,
            "daily_counts": daily_counts,
        }
    
    def search_logs(self, keyword: str, limit: int = 50) -> List[Log]:
        """Search logs by keyword in text or summary."""
        return self.session.query(Log).filter(
            or_(
                Log.original_text.like(f"%{keyword}%"),
                Log.ai_summary.like(f"%{keyword}%")
            )
        ).order_by(Log.created_at.desc()).limit(limit).all()
    
    def get_last_log_of_day(self, target_date: datetime) -> Optional[Log]:
        """Get the last log entry of a specific day."""
        start_of_day = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = target_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        return self.session.query(Log).filter(
            and_(
                Log.created_at >= start_of_day,
                Log.created_at <= end_of_day
            )
        ).order_by(Log.created_at.desc()).first()
    
    def update_log_duration(self, log_id: int, duration_minutes: int) -> bool:
        """Update the duration estimate of a log entry."""
        log = self.get_log_by_id(log_id)
        if log:
            log.duration_estimate = duration_minutes
            self.session.commit()
            return True
        return False
    
    def auto_update_previous_log_duration(self, new_log_time: datetime) -> Optional[tuple]:
        """
        Automatically update the duration of the previous log on the same day.
        Returns (previous_log, calculated_duration) if updated, None otherwise.
        """
        # Get the last log before the new log time on the same day
        start_of_day = new_log_time.replace(hour=0, minute=0, second=0, microsecond=0)
        
        previous_log = self.session.query(Log).filter(
            and_(
                Log.created_at >= start_of_day,
                Log.created_at < new_log_time
            )
        ).order_by(Log.created_at.desc()).first()
        
        if previous_log:
            # Calculate duration in minutes
            time_diff = new_log_time - previous_log.created_at
            duration_minutes = int(time_diff.total_seconds() / 60)
            
            # Update the previous log's duration
            previous_log.duration_estimate = duration_minutes
            self.session.commit()
            
            return (previous_log, duration_minutes)
        
        return None

