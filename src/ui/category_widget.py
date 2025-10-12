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
        
        # Category name with number badge
        name_layout = QHBoxLayout()
        
        # Category number badge
        category_number = QLabel(f"#{self.color_index + 1}")
        category_number.setStyleSheet(
            "font-size: 16px; font-weight: 600; color: #000000; "
            "background-color: #ffffff; padding: 4px 10px; border: 2px solid #000000; border-radius: 4px;"
        )
        category_number.setFixedWidth(45)
        name_layout.addWidget(category_number)
        
        self.name_label = QLabel(self.category.name)
        self.name_label.setObjectName("category_name")
        name_layout.addWidget(self.name_label, 1)
        
        layout.addLayout(name_layout)
        
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
        
        # Recent entries table
        entries_label = QLabel("Recent Finishers")
        entries_label.setStyleSheet("font-weight: 600; font-size: 13px; margin-top: 8px; color: #000000; background-color: #ffffff;")
        layout.addWidget(entries_label)
        
        self.entries_table = QTableWidget()
        self.entries_table.setColumnCount(3)
        self.entries_table.setHorizontalHeaderLabels(["ID", "Name", "Time"])
        self.entries_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.entries_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.entries_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.entries_table.customContextMenuRequested.connect(self.show_context_menu)
        self.entries_table.setFixedHeight(250)
        layout.addWidget(self.entries_table)
        
        # No stretch - fixed height
        
        # Set size policy for responsive 2-column layout
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumWidth(400)
        
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
        
        # Update entries table
        recent_entries = self.category.get_recent_entries(15)
        recent_entries.reverse()  # Show most recent first
        
        self.entries_table.setRowCount(len(recent_entries))
        
        for i, entry in enumerate(recent_entries):
            # ID
            id_item = QTableWidgetItem(entry.participant_id)
            id_item.setData(Qt.ItemDataRole.UserRole, entry.entry_id)  # Store entry_id
            if not entry.is_valid_id:
                id_item.setBackground(QColor(200, 200, 200))  # Light gray highlight
                font = id_item.font()
                font.setBold(True)
                id_item.setFont(font)
            if entry.is_dnf:
                id_item.setForeground(QColor(0, 0, 0))  # Black text
                id_item.setBackground(QColor(230, 230, 230))  # Lighter gray
            self.entries_table.setItem(i, 0, id_item)
            
            # Name
            name_item = QTableWidgetItem(entry.get_full_name())
            if entry.is_dnf:
                name_item.setForeground(QColor(0, 0, 0))
                name_item.setBackground(QColor(230, 230, 230))
                font = name_item.font()
                font.setItalic(True)
                name_item.setFont(font)
            self.entries_table.setItem(i, 1, name_item)
            
            # Time
            time_item = QTableWidgetItem(entry.format_elapsed_time())
            if entry.is_dnf:
                time_item.setText("DNF")
                time_item.setForeground(QColor(0, 0, 0))
                time_item.setBackground(QColor(230, 230, 230))
                font = time_item.font()
                font.setBold(True)
                time_item.setFont(font)
            self.entries_table.setItem(i, 2, time_item)
        
        self.entries_table.resizeColumnsToContents()
    
    def show_context_menu(self, position):
        """Show context menu for entries table."""
        if self.entries_table.rowCount() == 0:
            return
        
        row = self.entries_table.rowAt(position.y())
        if row < 0:
            return
        
        menu = QMenu(self)
        
        edit_action = menu.addAction("Edit Time")
        delete_action = menu.addAction("Delete Entry")
        menu.addSeparator()
        dnf_action = menu.addAction("Mark as DNF")
        
        action = menu.exec(self.entries_table.viewport().mapToGlobal(position))
        
        if action:
            id_item = self.entries_table.item(row, 0)
            if id_item:
                entry_id = id_item.data(Qt.ItemDataRole.UserRole)
                
                if action == edit_action:
                    self.entry_edited.emit(entry_id, self.category.name)
                elif action == delete_action:
                    self.entry_deleted.emit(entry_id, self.category.name)
                elif action == dnf_action:
                    # Find and mark entry as DNF
                    for entry in self.category.entries:
                        if entry.entry_id == entry_id:
                            entry.is_dnf = True
                            self.update_display()
                            break

