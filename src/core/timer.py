"""
Timer management for categories.
"""
from datetime import datetime, timedelta
from typing import Optional
from enum import Enum


class TimerState(Enum):
    """Possible states for a timer."""
    NOT_STARTED = "not_started"
    RUNNING = "running"
    STOPPED = "stopped"
    PAUSED = "paused"


class Timer:
    """Manages timing for a category."""
    
    def __init__(self):
        self.state = TimerState.NOT_STARTED
        self.start_time: Optional[datetime] = None
        self.stop_time: Optional[datetime] = None
        self.pause_time: Optional[datetime] = None
        self.accumulated_pause_duration: timedelta = timedelta(0)
    
    def start(self) -> None:
        """Start the timer."""
        if self.state == TimerState.NOT_STARTED:
            self.start_time = datetime.now()
            self.state = TimerState.RUNNING
        elif self.state == TimerState.PAUSED:
            # Resume from pause
            if self.pause_time:
                self.accumulated_pause_duration += datetime.now() - self.pause_time
                self.pause_time = None
            self.state = TimerState.RUNNING
    
    def stop(self) -> None:
        """Stop the timer."""
        if self.state == TimerState.RUNNING:
            self.stop_time = datetime.now()
            self.state = TimerState.STOPPED
    
    def pause(self) -> None:
        """Pause the timer."""
        if self.state == TimerState.RUNNING:
            self.pause_time = datetime.now()
            self.state = TimerState.PAUSED
    
    def reset(self) -> None:
        """Reset the timer to not started."""
        self.state = TimerState.NOT_STARTED
        self.start_time = None
        self.stop_time = None
        self.pause_time = None
        self.accumulated_pause_duration = timedelta(0)
    
    def get_elapsed_time(self, at_time: Optional[datetime] = None) -> timedelta:
        """
        Get elapsed time since start.
        
        Args:
            at_time: Calculate elapsed time at this specific time (for finish entries)
                    If None, uses current time
        
        Returns:
            Elapsed time as timedelta
        """
        if self.state == TimerState.NOT_STARTED:
            return timedelta(0)
        
        if not self.start_time:
            return timedelta(0)
        
        # Determine the end time
        if at_time:
            end_time = at_time
        elif self.state == TimerState.STOPPED and self.stop_time:
            end_time = self.stop_time
        elif self.state == TimerState.PAUSED and self.pause_time:
            end_time = self.pause_time
        else:
            end_time = datetime.now()
        
        elapsed = end_time - self.start_time - self.accumulated_pause_duration
        return elapsed if elapsed > timedelta(0) else timedelta(0)
    
    def format_elapsed_time(self) -> str:
        """Format elapsed time as HH:MM:SS."""
        elapsed = self.get_elapsed_time()
        total_seconds = int(elapsed.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def is_running(self) -> bool:
        """Check if timer is currently running."""
        return self.state == TimerState.RUNNING
    
    def to_dict(self) -> dict:
        """Convert timer to dictionary for serialization."""
        return {
            'state': self.state.value,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'stop_time': self.stop_time.isoformat() if self.stop_time else None,
            'pause_time': self.pause_time.isoformat() if self.pause_time else None,
            'accumulated_pause_duration': str(self.accumulated_pause_duration)
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Timer':
        """Create timer from dictionary (for deserialization)."""
        timer = cls()
        timer.state = TimerState(data['state'])
        timer.start_time = datetime.fromisoformat(data['start_time']) if data['start_time'] else None
        timer.stop_time = datetime.fromisoformat(data['stop_time']) if data['stop_time'] else None
        timer.pause_time = datetime.fromisoformat(data['pause_time']) if data['pause_time'] else None
        
        # Parse accumulated_pause_duration
        duration_str = data['accumulated_pause_duration']
        if duration_str and duration_str != '0:00:00':
            parts = duration_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds_parts = parts[2].split('.')
            seconds = int(seconds_parts[0])
            microseconds = int(seconds_parts[1]) if len(seconds_parts) > 1 else 0
            timer.accumulated_pause_duration = timedelta(
                hours=hours,
                minutes=minutes,
                seconds=seconds,
                microseconds=microseconds
            )
        
        return timer

