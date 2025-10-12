"""
Category widget for displaying category information, timer, and entries.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMenu, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QColor
from ..core.category import Category
from ..core.timer import TimerState
from .styles import get_category_color


class CategoryWidget(QWidget):
    """Widget for displaying a single category with timer and entries."""
    
    timer_started = pyqtSignal(str)  # category_name
    timer_stopped = pyqtSignal(str)  # category_name
    entry_edited = pyqtSignal(str, str)  # entry_id, category_name
    entry_deleted = pyqtSignal(str, str)  # entry_id, category_name
    
    def __init__(self, category: Category, color_index: int = 0, parent=None):
        super().__init__(parent)
        self.category = category
        self.color_index = color_index
        self.color = get_category_color(color_index)
        
        self.setObjectName("category_widget")
        self.setup_ui()
        
        # Timer for updating display
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_timer_display)
        self.update_timer.start(100)  # Update every 100ms
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Category name
        self.name_label = QLabel(self.category.name)
        self.name_label.setObjectName("category_name")
        layout.addWidget(self.name_label)
        
        # Timer display
        self.timer_label = QLabel("00:00:00")
        self.timer_label.setObjectName("timer_label")
        layout.addWidget(self.timer_label)
        
        # Statistics
        self.stats_label = QLabel("0 / 0 finished")
        self.stats_label.setObjectName("stats_label")
        layout.addWidget(self.stats_label)
        
        # Start/Stop button
        self.control_btn = QPushButton("Start Timer")
        self.control_btn.setObjectName("start_button")
        self.control_btn.clicked.connect(self.toggle_timer)
        layout.addWidget(self.control_btn)
        
        # Add stretch to push content to top
        layout.addStretch()
        
        # Set size policy for responsive 2-column layout
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumWidth(400)
        self.setMaximumHeight(250)
        
        # Initial update
        self.update_display()
    
    def toggle_timer(self):
        """Toggle timer start/stop."""
        if self.category.timer.state == TimerState.NOT_STARTED:
            self.category.timer.start()
            self.control_btn.setText("Stop Timer")
            self.control_btn.setObjectName("stop_button")
            self.control_btn.setStyleSheet("")  # Reset style to apply new object name
            self.timer_started.emit(self.category.name)
        elif self.category.timer.state == TimerState.RUNNING:
            self.category.timer.stop()
            self.control_btn.setText("Timer Stopped")
            self.control_btn.setEnabled(False)
            self.timer_stopped.emit(self.category.name)
    
    def update_timer_display(self):
        """Update the timer display."""
        if self.category.timer.is_running():
            time_str = self.category.timer.format_elapsed_time()
            self.timer_label.setText(time_str)
            self.timer_label.setObjectName("timer_label_running")
            self.timer_label.setStyleSheet("")  # Reset to apply new object name
    
    def update_display(self):
        """Update all displays with current data."""
        # Update statistics
        total = self.category.get_total_participants()
        finished = self.category.get_finished_count()
        self.stats_label.setText(f"{finished} / {total} finished")
        
        # Update timer display
        time_str = self.category.timer.format_elapsed_time()
        self.timer_label.setText(time_str)
        
        # Update timer label style based on state
        if self.category.timer.state == TimerState.RUNNING:
            self.timer_label.setObjectName("timer_label_running")
        elif self.category.timer.state == TimerState.STOPPED:
            self.timer_label.setObjectName("timer_label_stopped")
        else:
            self.timer_label.setObjectName("timer_label")
        self.timer_label.setStyleSheet("")  # Reset to apply new object name
        
        # Update button text and state based on timer state
        if self.category.timer.state == TimerState.RUNNING:
            self.control_btn.setText("Stop Timer")
            self.control_btn.setObjectName("stop_button")
            self.control_btn.setEnabled(True)
            # Force style update
            self.control_btn.style().unpolish(self.control_btn)
            self.control_btn.style().polish(self.control_btn)
        elif self.category.timer.state == TimerState.STOPPED:
            self.control_btn.setText("Timer Stopped")
            self.control_btn.setEnabled(False)
        else:
            self.control_btn.setText("Start Timer")
            self.control_btn.setObjectName("start_button")
            self.control_btn.setEnabled(True)
            # Force style update
            self.control_btn.style().unpolish(self.control_btn)
            self.control_btn.style().polish(self.control_btn)
    
    def show_context_menu(self, position):
        """Show context menu - not used anymore since table was removed."""
        pass

