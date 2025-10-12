"""
Main application window.
"""
import uuid
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QScrollArea, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox, QInputDialog, QHeaderView
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QKeySequence, QShortcut, QColor
from ..core.category import Category
from ..core.entry import FinishEntry
from ..core.session import Session
from ..utils.validation import find_participant_category
from ..utils.excel_export import export_to_excel, generate_default_filename
from .category_widget import CategoryWidget
from .csv_loader import CSVLoaderDialog


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.session = Session()
        self.category_widgets = []
        self.last_entries = []  # Track last entries for undo
        
        self.setWindowTitle("MTB Time Tracker")
        self.setMinimumSize(1200, 800)
        
        self.setup_ui()
        self.setup_shortcuts()
        self.setup_auto_save()
        
        # Try to load last session
        self.prompt_load_last_session()
    
    def setup_ui(self):
        """Set up the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(24, 24, 24, 24)
        
        # Header: Title and controls row
        header_layout = QHBoxLayout()
        
        title = QLabel("MTB Time Tracker")
        title.setStyleSheet("font-size: 20px; font-weight: 600; color: #000000; background-color: #ffffff;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        load_csv_btn = QPushButton("Load Category")
        load_csv_btn.setObjectName("primary_button")
        load_csv_btn.clicked.connect(self.load_category)
        header_layout.addWidget(load_csv_btn)
        
        save_btn = QPushButton("Save")
        save_btn.setObjectName("success_button")
        save_btn.clicked.connect(self.save_session)
        header_layout.addWidget(save_btn)
        
        export_btn = QPushButton("Export")
        export_btn.setObjectName("primary_button")
        export_btn.clicked.connect(self.export_results)
        header_layout.addWidget(export_btn)
        
        end_session_btn = QPushButton("End Session")
        end_session_btn.setObjectName("danger_button")
        end_session_btn.clicked.connect(self.end_session)
        header_layout.addWidget(end_session_btn)
        
        main_layout.addLayout(header_layout)
        
        # Input section - centered at top
        input_section = QVBoxLayout()
        input_section.setSpacing(8)
        
        # Center the input row
        input_row = QHBoxLayout()
        input_row.setSpacing(12)
        
        input_row.addStretch()  # Left spacer
        
        self.input_field = QLineEdit()
        self.input_field.setObjectName("fast_input")
        self.input_field.setPlaceholderText("Startnummer")
        self.input_field.returnPressed.connect(self.process_entry)
        input_row.addWidget(self.input_field)
        
        self.undo_btn = QPushButton("Undo")
        self.undo_btn.clicked.connect(self.undo_last_entry)
        self.undo_btn.setEnabled(False)
        input_row.addWidget(self.undo_btn)
        
        input_row.addStretch()  # Right spacer
        
        input_section.addLayout(input_row)
        
        # Status message - centered
        self.status_label = QLabel("")
        self.status_label.setMinimumHeight(24)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_section.addWidget(self.status_label)
        
        main_layout.addLayout(input_section)
        
        # Categories section - show 2 side by side
        categories_label = QLabel("Categories")
        categories_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #000000; background-color: #ffffff; margin-top: 8px;")
        main_layout.addWidget(categories_label)
        
        # Container for categories (no scroll, just 2 side by side)
        self.categories_container = QWidget()
        self.categories_layout = QHBoxLayout(self.categories_container)
        self.categories_layout.setSpacing(16)
        self.categories_layout.setContentsMargins(0, 0, 0, 0)
        self.categories_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        main_layout.addWidget(self.categories_container)
        
        # Recent entries section - at bottom
        recent_label = QLabel("Recent Entries")
        recent_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #000000; background-color: #ffffff; margin-top: 8px;")
        main_layout.addWidget(recent_label)
        
        self.recent_entries_table = QTableWidget()
        self.recent_entries_table.setColumnCount(4)
        self.recent_entries_table.setHorizontalHeaderLabels(["ID", "NAME", "CATEGORY", "TIME"])
        self.recent_entries_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.recent_entries_table.setMaximumHeight(180)
        self.recent_entries_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.recent_entries_table.setShowGrid(False)
        self.recent_entries_table.setAlternatingRowColors(False)
        self.recent_entries_table.verticalHeader().setVisible(False)
        # Enable inline editing on double-click
        self.recent_entries_table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        self.recent_entries_table.itemChanged.connect(self.on_recent_entry_item_changed)
        main_layout.addWidget(self.recent_entries_table)
        
        # Update recent entries initially
        self.update_recent_entries()
    
    def setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        # Ctrl+S: Save
        save_shortcut = QShortcut(QKeySequence.StandardKey.Save, self)
        save_shortcut.activated.connect(self.save_session)
        
        # Ctrl+E: Export
        export_shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        export_shortcut.activated.connect(self.export_results)
        
        # Ctrl+N: New session
        new_shortcut = QShortcut(QKeySequence.StandardKey.New, self)
        new_shortcut.activated.connect(self.end_session)
        
        # Ctrl+Z: Undo
        undo_shortcut = QShortcut(QKeySequence.StandardKey.Undo, self)
        undo_shortcut.activated.connect(self.undo_last_entry)
        
        # Ctrl+L: Load category
        load_shortcut = QShortcut(QKeySequence("Ctrl+L"), self)
        load_shortcut.activated.connect(self.load_category)
    
    def setup_auto_save(self):
        """Set up auto-save timer."""
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_timer.start(30000)  # Auto-save every 30 seconds
    
    def load_category(self):
        """Load a new category from CSV."""
        dialog = CSVLoaderDialog(self)
        if dialog.exec():
            category = dialog.get_category()
            if category:
                self.session.add_category(category)
                self.add_category_widget(category)
                self.show_status(f"Loaded category: {category.name}", "success")
    
    def add_category_widget(self, category: Category):
        """Add a category widget to the UI."""
        color_index = len(self.category_widgets)
        widget = CategoryWidget(category, color_index)
        widget.timer_started.connect(lambda name: self.show_status(f"Timer started for {name}", "success"))
        widget.timer_stopped.connect(lambda name: self.show_status(f"Timer stopped for {name}", "warning"))
        widget.entry_edited.connect(self.edit_entry)
        widget.entry_deleted.connect(self.delete_entry)
        
        self.categories_layout.addWidget(widget)
        self.category_widgets.append(widget)
    
    def process_entry(self):
        """Process a participant ID entry."""
        participant_id = self.input_field.text().strip()
        
        if not participant_id:
            return
        
        # Find which category this participant belongs to
        category = find_participant_category(participant_id, self.session.categories)
        
        if category is None:
            # ID not found in any category - still record but warn
            self.show_status(f"⚠ Warning: ID {participant_id} not found in any category. Entry recorded.", "warning")
            # Try to assign to a running category or first category
            category = next((c for c in self.session.categories if c.timer.is_running()), 
                          self.session.categories[0] if self.session.categories else None)
            
            if category is None:
                self.show_status("Error: No categories loaded!", "error")
                return
            
            is_valid = False
            participant_data = {}
        else:
            is_valid = True
            participant_data = category.get_participant_data(participant_id) or {}
        
        # Check if timer is running
        if not category.timer.is_running():
            self.show_status(f"⚠ Warning: Timer for {category.name} is not running!", "warning")
        
        # Create finish entry
        entry = FinishEntry(
            entry_id=str(uuid.uuid4()),
            participant_id=participant_id,
            category_name=category.name,
            finish_time=datetime.now(),
            elapsed_time=category.timer.get_elapsed_time(),
            first_name=participant_data.get('first_name'),
            last_name=participant_data.get('last_name'),
            team=participant_data.get('team'),
            birth_year=participant_data.get('birth_year'),
            gender=participant_data.get('gender'),
            is_valid_id=is_valid
        )
        
        # Add entry to category
        category.add_entry(entry)
        
        # Track for undo
        self.last_entries.append((entry, category))
        if len(self.last_entries) > 10:  # Keep only last 10
            self.last_entries.pop(0)
        self.undo_btn.setEnabled(True)
        
        # Update displays
        self.update_category_widget(category)
        self.update_recent_entries()
        
        # Show success message
        if is_valid:
            name = entry.get_full_name()
            time = entry.format_elapsed_time()
            self.show_status(f"✓ Recorded: {name} ({participant_id}) - {time}", "success")
        
        # Clear input and refocus
        self.input_field.clear()
        self.input_field.setFocus()
    
    def undo_last_entry(self):
        """Undo the last entry."""
        if not self.last_entries:
            return
        
        entry, category = self.last_entries.pop()
        
        # Remove from category
        category.entries = [e for e in category.entries if e.entry_id != entry.entry_id]
        
        # Update displays
        self.update_category_widget(category)
        self.update_recent_entries()
        
        self.show_status(f"Undone: {entry.participant_id}", "warning")
        
        if not self.last_entries:
            self.undo_btn.setEnabled(False)
    
    def update_category_widget(self, category: Category):
        """Update a specific category widget."""
        for widget in self.category_widgets:
            if widget.category.name == category.name:
                widget.update_display()
                break
    
    def update_recent_entries(self):
        """Update the recent entries table."""
        # Temporarily block signals to avoid triggering itemChanged during update
        self.recent_entries_table.blockSignals(True)
        
        all_entries = self.session.get_all_entries()[:20]  # Last 20 entries
        
        self.recent_entries_table.setRowCount(len(all_entries))
        
        for i, entry in enumerate(all_entries):
            # ID (editable)
            id_item = QTableWidgetItem(entry.participant_id)
            id_item.setData(Qt.ItemDataRole.UserRole, entry.entry_id)  # Store entry_id
            id_item.setFlags(id_item.flags() | Qt.ItemFlag.ItemIsEditable)
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if not entry.is_valid_id:
                id_item.setBackground(QColor(200, 200, 200))  # Gray highlight for invalid IDs
                font = id_item.font()
                font.setBold(True)
                id_item.setFont(font)
            self.recent_entries_table.setItem(i, 0, id_item)
            
            # Name (read-only)
            name_item = QTableWidgetItem(entry.get_full_name())
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.recent_entries_table.setItem(i, 1, name_item)
            
            # Category (read-only)
            # Show "-" for invalid IDs instead of category name
            if entry.is_valid_id:
                category_item = QTableWidgetItem(entry.category_name)
                # Use grayscale coding by category - make text bold and use different shades
                category = self.session.get_category(entry.category_name)
                if category:
                    cat_index = self.session.categories.index(category)
                    from .styles import get_category_color
                    color = QColor(get_category_color(cat_index))
                    # Make lighter for background
                    lightness = 200 + (cat_index * 10) % 50  # Vary between 200-250
                    category_item.setBackground(QColor(lightness, lightness, lightness))
                    font = category_item.font()
                    font.setBold(True)
                    category_item.setFont(font)
            else:
                category_item = QTableWidgetItem("-")
                category_item.setForeground(QColor(150, 150, 150))  # Gray text
            
            category_item.setFlags(category_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            category_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.recent_entries_table.setItem(i, 2, category_item)
            
            # Time (read-only) - show elapsed time
            time_item = QTableWidgetItem(entry.format_elapsed_time())
            time_item.setFlags(time_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.recent_entries_table.setItem(i, 3, time_item)
        
        # Don't call resizeColumnsToContents() - we're using stretch mode
        
        # Re-enable signals
        self.recent_entries_table.blockSignals(False)
    
    def on_recent_entry_item_changed(self, item):
        """Handle when an item is edited in the recent entries table."""
        # Only process ID column (column 0)
        if item.column() != 0:
            return
        
        new_id = item.text().strip()
        entry_id = item.data(Qt.ItemDataRole.UserRole)
        
        if not new_id or not entry_id:
            return
        
        # Find the entry in all categories
        entry = None
        category = None
        for cat in self.session.categories:
            entry = next((e for e in cat.entries if e.entry_id == entry_id), None)
            if entry:
                category = cat
                break
        
        if not entry or not category:
            return
        
        # If ID hasn't changed, do nothing
        if new_id == entry.participant_id:
            return
        
        # Update ID and search for participant data
        entry.participant_id = new_id
        
        found_category = None
        participant_data = None
        
        for cat in self.session.categories:
            if cat.has_participant(new_id):
                found_category = cat
                participant_data = cat.get_participant_data(new_id)
                break
        
        # Update entry with new participant data
        if participant_data:
            entry.first_name = participant_data.get('first_name', '')
            entry.last_name = participant_data.get('last_name', '')
            entry.team = participant_data.get('team', '')
            entry.birth_year = participant_data.get('birth_year', '')
            entry.gender = participant_data.get('gender', '')
            entry.is_valid_id = True
            
            # Update category if it changed
            if found_category and found_category.name != entry.category_name:
                # Move entry to correct category
                category.entries.remove(entry)
                entry.category_name = found_category.name
                found_category.add_entry(entry)
                self.update_category_widget(found_category)
            
            self.show_status(f"✓ Updated: {entry.get_full_name()} ({new_id})", "success")
        else:
            # ID not found - mark as invalid
            entry.is_valid_id = False
            entry.first_name = ''
            entry.last_name = ''
            entry.team = ''
            entry.birth_year = ''
            entry.gender = ''
            self.show_status(f"⚠ ID {new_id} not found in any category", "warning")
        
        # Update displays
        self.update_category_widget(category)
        self.update_recent_entries()
    
    def edit_entry(self, entry_id: str, category_name: str):
        """Edit an entry's ID."""
        category = self.session.get_category(category_name)
        if not category:
            return
        
        # Find the entry
        entry = next((e for e in category.entries if e.entry_id == entry_id), None)
        if not entry:
            return
        
        # Create custom dialog for editing
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Participant ID")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        # ID field
        id_layout = QHBoxLayout()
        id_layout.addWidget(QLabel("Participant ID:"))
        id_field = QLineEdit(entry.participant_id)
        id_field.setFocus()
        id_layout.addWidget(id_field)
        layout.addLayout(id_layout)
        
        # Current info (read-only)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        current_label = QLabel(f"Current: {entry.get_full_name()}")
        current_label.setStyleSheet("color: #000; font-weight: 600; margin-top: 10px;")
        info_layout.addWidget(current_label)
        
        time_label = QLabel(f"Time: {entry.format_elapsed_time()} (Category: {entry.category_name})")
        time_label.setStyleSheet("color: #666; font-style: italic;")
        info_layout.addWidget(time_label)
        
        layout.addLayout(info_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save")
        save_btn.setObjectName("primary_button")
        save_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
        if dialog.exec():
            new_id = id_field.text().strip()
            
            if not new_id:
                QMessageBox.warning(self, "Error", "ID cannot be empty")
                return
            
            # Update ID and check if it's valid in any category
            old_id = entry.participant_id
            entry.participant_id = new_id
            
            # Search for the new ID in all categories
            found_category = None
            participant_data = None
            
            for cat in self.session.categories:
                if cat.has_participant(new_id):
                    found_category = cat
                    participant_data = cat.get_participant_data(new_id)
                    break
            
            # Update entry with new participant data
            if participant_data:
                entry.first_name = participant_data.get('first_name', '')
                entry.last_name = participant_data.get('last_name', '')
                entry.team = participant_data.get('team', '')
                entry.birth_year = participant_data.get('birth_year', '')
                entry.gender = participant_data.get('gender', '')
                entry.is_valid_id = True
                
                # Update category if it changed
                if found_category and found_category.name != entry.category_name:
                    # Move entry to correct category
                    category.entries.remove(entry)
                    entry.category_name = found_category.name
                    found_category.add_entry(entry)
                    self.update_category_widget(found_category)
                
                self.show_status(f"Updated entry: {entry.get_full_name()} ({new_id})", "success")
            else:
                # ID not found - keep it but mark as invalid
                entry.is_valid_id = False
                entry.first_name = ''
                entry.last_name = ''
                entry.team = ''
                entry.birth_year = ''
                entry.gender = ''
                self.show_status(f"⚠ ID {new_id} not found in any category", "warning")
            
            self.update_category_widget(category)
            self.update_recent_entries()
    
    def delete_entry(self, entry_id: str, category_name: str):
        """Delete an entry."""
        category = self.session.get_category(category_name)
        if not category:
            return
        
        # Find the entry
        entry = next((e for e in category.entries if e.entry_id == entry_id), None)
        if not entry:
            return
        
        reply = QMessageBox.question(
            self,
            "Delete Entry",
            f"Delete entry for {entry.get_full_name()} ({entry.participant_id})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            category.entries = [e for e in category.entries if e.entry_id != entry_id]
            self.update_category_widget(category)
            self.update_recent_entries()
            self.show_status(f"Deleted entry for {entry.participant_id}", "warning")
    
    def save_session(self):
        """Manually save the session."""
        try:
            path = self.session.save()
            self.show_status(f"Session saved to {path.name}", "success")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save session:\n{str(e)}")
    
    def auto_save(self):
        """Auto-save the session."""
        if self.session.categories:
            try:
                self.session.save()
            except Exception as e:
                print(f"Auto-save failed: {e}")
    
    def export_results(self):
        """Export results to Excel."""
        if not self.session.categories:
            QMessageBox.warning(self, "Warning", "No categories to export!")
            return
        
        # Check if any entries exist
        if not any(cat.entries for cat in self.session.categories):
            QMessageBox.warning(self, "Warning", "No entries to export!")
            return
        
        # Get default save location (Documents or Downloads folder)
        from pathlib import Path as PathLib
        import os
        
        # Try to use Documents folder, fallback to Downloads, then Home
        if os.name == 'nt':  # Windows
            default_dir = PathLib(os.environ.get('USERPROFILE', PathLib.home())) / 'Documents'
        else:  # macOS and Linux
            default_dir = PathLib.home() / 'Documents'
            if not default_dir.exists():
                default_dir = PathLib.home() / 'Downloads'
            if not default_dir.exists():
                default_dir = PathLib.home()
        
        default_filename = generate_default_filename()
        default_path = str(default_dir / default_filename)
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Race Results",
            default_path,
            "Excel Files (*.xlsx);;All Files (*)"
        )
        
        if file_path:
            try:
                # Ensure .xlsx extension
                if not file_path.endswith('.xlsx'):
                    file_path += '.xlsx'
                
                export_to_excel(self.session.categories, Path(file_path))
                QMessageBox.information(
                    self, 
                    "Export Successful", 
                    f"Results exported successfully!\n\nSaved to:\n{file_path}"
                )
                self.show_status("Results exported successfully!", "success")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export results:\n{str(e)}")
    
    def end_session(self):
        """End the current session and start a new one."""
        if self.session.categories:
            reply = QMessageBox.question(
                self,
                "End Session",
                "Are you sure you want to end the current session?\nMake sure to export results first!",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        # Clear session
        self.session.clear()
        
        # Clear UI
        for widget in self.category_widgets:
            widget.deleteLater()
        self.category_widgets.clear()
        
        self.last_entries.clear()
        self.undo_btn.setEnabled(False)
        
        self.update_recent_entries()
        self.show_status("New session started", "success")
        self.input_field.setFocus()
    
    def prompt_load_last_session(self):
        """Prompt to load the last session on startup."""
        last_session = Session.get_latest_session()
        if last_session:
            reply = QMessageBox.question(
                self,
                "Resume Session",
                f"Found a previous session:\n{last_session.name}\n\nDo you want to resume it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    self.session = Session.load(last_session)
                    
                    # Recreate category widgets
                    for category in self.session.categories:
                        self.add_category_widget(category)
                    
                    self.update_recent_entries()
                    self.show_status("Session resumed", "success")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to load session:\n{str(e)}")
    
    def show_status(self, message: str, status_type: str = "info"):
        """Show a status message."""
        self.status_label.setText(message)
        
        if status_type == "success":
            self.status_label.setObjectName("success_message")
        elif status_type == "warning":
            self.status_label.setObjectName("warning_message")
        elif status_type == "error":
            self.status_label.setObjectName("error_message")
        else:
            self.status_label.setObjectName("")
        
        self.status_label.setStyleSheet("")  # Reset to apply new object name
        
        # Clear message after 5 seconds
        QTimer.singleShot(5000, lambda: self.status_label.setText(""))
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Auto-save before closing
        if self.session.categories:
            self.auto_save()
        event.accept()

