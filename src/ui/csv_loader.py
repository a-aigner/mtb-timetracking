"""
CSV Loader dialog for importing participant data.
"""
import pandas as pd
from pathlib import Path
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QLineEdit,
    QFileDialog, QMessageBox, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from ..core.category import Category


class CSVLoaderDialog(QDialog):
    """Dialog for loading CSV files and selecting ID column."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.csv_path: Path = None
        self.dataframe: pd.DataFrame = None
        self.selected_id_column: str = None
        self.category_name: str = None
        
        self.setWindowTitle("Load CSV File")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("QDialog { background-color: #fafafa; }")
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # File selection section
        file_group = QGroupBox()
        file_group.setStyleSheet("QGroupBox { margin-top: 8px; }")
        file_layout = QHBoxLayout()
        file_layout.setContentsMargins(8, 8, 8, 8)
        
        self.file_path_label = QLabel("No file selected")
        self.file_path_label.setWordWrap(True)
        self.file_path_label.setStyleSheet("color: #666; font-size: 13px;")
        file_layout.addWidget(self.file_path_label, 1)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.setObjectName("primary_button")
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Category name section
        name_group = QGroupBox()
        name_layout = QHBoxLayout()
        name_layout.setContentsMargins(8, 8, 8, 8)
        
        name_layout.addWidget(QLabel("Disziplin:"))
        self.category_name_input = QLineEdit()
        self.category_name_input.setPlaceholderText("MTB, E-MTB ...")
        name_layout.addWidget(self.category_name_input, 1)
        
        name_group.setLayout(name_layout)
        layout.addWidget(name_group)
        
        # Column selection section
        column_group = QGroupBox()
        column_layout = QHBoxLayout()
        column_layout.setContentsMargins(8, 8, 8, 8)
        
        column_layout.addWidget(QLabel("Startnummer Spalte auswählen..."))
        self.column_combo = QComboBox()
        self.column_combo.currentTextChanged.connect(self.on_column_changed)
        column_layout.addWidget(self.column_combo, 1)
        
        column_group.setLayout(column_layout)
        layout.addWidget(column_group)
        
        # Preview table
        preview_label = QLabel("Data Preview")
        preview_label.setStyleSheet("font-weight: 600; font-size: 13px; color: #000000; background-color: #ffffff; margin-top: 12px;")
        layout.addWidget(preview_label)
        
        self.preview_table = QTableWidget()
        self.preview_table.setAlternatingRowColors(False)
        self.preview_table.setShowGrid(False)
        self.preview_table.verticalHeader().setVisible(False)  # Hide row numbers
        self.preview_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e5e5e5;
                border-radius: 6px;
                background-color: #ffffff;
            }
        """)
        layout.addWidget(self.preview_table)
        
        # Info label
        self.info_label = QLabel("")
        self.info_label.setStyleSheet("color: #000000; font-style: italic; background-color: #ffffff;")
        layout.addWidget(self.info_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        self.load_btn = QPushButton("Load Category")
        self.load_btn.setObjectName("primary_button")
        self.load_btn.clicked.connect(self.accept_and_load)
        self.load_btn.setEnabled(False)
        button_layout.addWidget(self.load_btn)
        
        layout.addLayout(button_layout)
    
    def browse_file(self):
        """Open file browser to select CSV file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            self.load_csv(Path(file_path))
    
    def load_csv(self, path: Path):
        """Load and parse CSV file."""
        try:
            self.csv_path = path
            self.file_path_label.setText(str(path))
            
            # Try different delimiters and encodings - NO HEADER ROW
            df = None
            for delimiter in [';', ',', '\t']:
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        # Read CSV without header (header=None)
                        temp_df = pd.read_csv(path, delimiter=delimiter, encoding=encoding, header=None)
                        if len(temp_df.columns) > 1:  # Valid CSV should have multiple columns
                            df = temp_df
                            break
                    except:
                        continue
                if df is not None:
                    break
            
            if df is None:
                raise ValueError("Could not parse CSV file with any known format")
            
            # Create column names as A, B, C, D, etc.
            column_letters = []
            for i in range(len(df.columns)):
                if i < 26:
                    column_letters.append(chr(65 + i))  # A-Z
                else:
                    # For more than 26 columns: AA, AB, AC, etc.
                    first = chr(65 + (i // 26) - 1)
                    second = chr(65 + (i % 26))
                    column_letters.append(first + second)
            
            df.columns = column_letters
            
            # Clean data
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].astype(str).str.strip().str.strip('"')
            
            self.dataframe = df
            
            # Populate column combo with letter labels
            self.column_combo.clear()
            column_items = [f"Column {col} (Index {i})" for i, col in enumerate(df.columns)]
            self.column_combo.addItems(column_items)
            
            # Default to first column (usually the ID column)
            if len(df.columns) > 0:
                self.column_combo.setCurrentIndex(0)
            
            # Set category name from filename if not set
            if not self.category_name_input.text():
                default_name = path.stem.replace('_', ' ').replace('-', ' ').title()
                self.category_name_input.setText(default_name)
            
            # Update preview
            self.update_preview()
            
            # Update info
            self.info_label.setText(f"Loaded {len(df)} rows with {len(df.columns)} columns")
            
            self.load_btn.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load CSV file:\n{str(e)}")
            self.load_btn.setEnabled(False)
    
    def update_preview(self):
        """Update the preview table with current data."""
        if self.dataframe is None:
            return
        
        df = self.dataframe.head(20)  # Show first 20 rows
        
        self.preview_table.setRowCount(len(df))
        self.preview_table.setColumnCount(len(df.columns))
        self.preview_table.setHorizontalHeaderLabels(df.columns.tolist())
        
        # Get the selected column letter from combo box
        selected_text = self.column_combo.currentText()
        # Extract column letter from "Column A (Index 0)" format
        id_col = selected_text.split()[1] if selected_text else df.columns[0]
        
        for i, row in enumerate(df.itertuples(index=False)):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                
                # Highlight ID column with black border and bold text
                if df.columns[j] == id_col:
                    item.setBackground(QColor(220, 220, 220))  # Light gray background
                    item.setForeground(QColor(0, 0, 0))  # Black text
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                else:
                    item.setForeground(QColor(0, 0, 0))  # Black text
                
                self.preview_table.setItem(i, j, item)
        
        self.preview_table.resizeColumnsToContents()
    
    def on_column_changed(self):
        """Handle ID column selection change."""
        self.update_preview()
    
    def accept_and_load(self):
        """Validate and accept the dialog."""
        if not self.category_name_input.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter a category name.")
            return
        
        if self.dataframe is None:
            QMessageBox.warning(self, "Warning", "Please load a CSV file first.")
            return
        
        # Extract the column letter from "Column A (Index 0)" format
        selected_text = self.column_combo.currentText()
        self.selected_id_column = selected_text.split()[1] if selected_text else self.dataframe.columns[0]
        self.category_name = self.category_name_input.text().strip()
        
        # Validate that ID column has data
        id_values = self.dataframe[self.selected_id_column].dropna()
        if len(id_values) == 0:
            QMessageBox.warning(self, "Warning", "The selected ID column appears to be empty.")
            return
        
        self.accept()
    
    def get_category(self) -> Category:
        """Create and return a Category object from the loaded data."""
        if self.dataframe is None or not self.category_name:
            return None
        
        # Create category with the dataframe
        category = Category(
            name=self.category_name,
            csv_path=self.csv_path,
            id_column=self.selected_id_column,
            dataframe=self.dataframe
        )
        
        return category

