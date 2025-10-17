"""
Modern styling for the application using PyQt6 stylesheets.
"""

def get_app_stylesheet() -> str:
    """Get the main application stylesheet."""
    return """
    QMainWindow {
        background-color: #ffffff;
    }
    
    /* Input field styling */
    QLineEdit#fast_input {
        font-size: 28px;
        padding: 12px 16px;
        border: 2px solid #000000;
        border-radius: 8px;
        background-color: white;
        color: #000000;
        font-weight: 600;
        max-width: 300px;
    }
    
    QLineEdit#fast_input:focus {
        border: 2px solid #000000;
        background-color: #ffffff;
    }
    
    /* Button styling - Tailwind inspired */
    QPushButton {
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 500;
        border: 1px solid #d4d4d4;
        background-color: #ffffff;
        color: #000000;
    }
    
    QPushButton#primary_button {
        background-color: #000000;
        color: white;
        border: 1px solid #000000;
        padding: 8px 20px;
    }
    
    QPushButton#primary_button:hover {
        background-color: #1a1a1a;
    }
    
    QPushButton#primary_button:pressed {
        background-color: #000000;
    }
    
    QPushButton#success_button {
        background-color: #000000;
        color: white;
        border: 1px solid #000000;
        padding: 8px 20px;
    }
    
    QPushButton#success_button:hover {
        background-color: #1a1a1a;
    }
    
    QPushButton#danger_button {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #d4d4d4;
        padding: 8px 20px;
    }
    
    QPushButton#danger_button:hover {
        background-color: #f5f5f5;
    }
    
    QPushButton#start_button {
        background-color: #000000;
        color: white;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: 600;
        border: 1px solid #000000;
        border-radius: 6px;
        min-width: 80px;
        max-width: 120px;
    }
    
    QPushButton#start_button:hover {
        background-color: #1a1a1a;
    }
    
    QPushButton#stop_button {
        background-color: #ffffff;
        color: #000000;
        padding: 12px 16px;
        font-size: 14px;
        font-weight: 600;
        border: 1px solid #d4d4d4;
        border-radius: 50%;
        min-width: 80px;
        max-width: 120px;
        min-height: 40px;
    }
    
    QPushButton#stop_button:hover {
        background-color: #f5f5f5;
    }
    
    QPushButton:disabled {
        background-color: #f5f5f5;
        color: #999999;
        border: 2px solid #d4d4d4;
    }
    
    QPushButton:hover {
        background-color: #f9f9f9;
    }
    
    /* Label styling */
    QLabel#timer_label {
        font-size: 40px;
        font-weight: 700;
        color: #000000;
        padding: 16px;
        background-color: white;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        qproperty-alignment: AlignCenter;
    }
    
    QLabel#timer_label_running {
        font-size: 40px;
        font-weight: 700;
        color: #000000;
        padding: 16px;
        background-color: #ffffff;
        border: 1px solid #d4d4d4;
        border-radius: 8px;
        qproperty-alignment: AlignCenter;
    }
    
    QLabel#timer_label_stopped {
        font-size: 40px;
        font-weight: 700;
        color: #000000;
        padding: 16px;
        background-color: #ffffff;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        qproperty-alignment: AlignCenter;
    }
    
    QLabel#category_name {
        font-size: 20px;
        font-weight: 600;
        color: #000000;
        padding: 8px;
        background-color: #ffffff;
        qproperty-alignment: AlignCenter;
    }
    
    QLabel#stats_label {
        font-size: 14px;
        color: #000000;
        padding: 4px;
        qproperty-alignment: AlignCenter;
    }
    
    /* Category widget styling */
    QWidget#category_widget {
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #d4d4d4;
    }
    
    /* Table styling - Minimalistic */
    QTableWidget {
        background-color: #ffffff;
        border: none;
        border-top: 1px solid #e5e5e5;
        border-bottom: 1px solid #e5e5e5;
        gridline-color: #f5f5f5;
        font-size: 13px;
        color: #000000;
        selection-background-color: #f9f9f9;
    }
    
    QTableWidget::item {
        padding: 10px 12px;
        color: #000000;
        border: none;
        border-bottom: 1px solid #f5f5f5;
    }
    
    QTableWidget::item:selected {
        background-color: #f9f9f9;
        color: #000000;
    }
    
    QTableWidget::item:hover {
        background-color: #fafafa;
    }
    
    QHeaderView::section {
        background-color: #ffffff;
        color: #666666;
        padding: 12px;
        border: none;
        border-bottom: 1px solid #e5e5e5;
        font-weight: 600;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    QHeaderView::section:hover {
        background-color: #fafafa;
    }
    
    /* ScrollArea styling */
    QScrollArea {
        border: none;
        background-color: #ffffff;
    }
    
    QScrollBar:horizontal {
        border: 1px solid #000000;
        background: #ffffff;
        height: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:horizontal {
        background: #000000;
        border-radius: 6px;
        min-width: 40px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background: #333333;
    }
    
    QScrollBar:vertical {
        border: 1px solid #000000;
        background: #ffffff;
        width: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:vertical {
        background: #000000;
        border-radius: 6px;
        min-height: 40px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: #333333;
    }
    
    /* ComboBox styling */
    QComboBox {
        padding: 8px;
        border: 2px solid #000000;
        border-radius: 4px;
        background-color: white;
        color: #000000;
        font-size: 14px;
    }
    
    QComboBox:focus {
        border: 3px solid #000000;
    }
    
    QComboBox::drop-down {
        border: none;
        padding-right: 10px;
    }
    
    /* Status messages */
    QLabel#success_message {
        color: #000000;
        background-color: #e0e0e0;
        font-size: 14px;
        font-weight: bold;
        padding: 10px;
        border: 2px solid #000000;
        border-radius: 4px;
    }
    
    QLabel#warning_message {
        color: #000000;
        background-color: #ffffff;
        font-size: 14px;
        font-weight: bold;
        padding: 10px;
        border: 2px solid #000000;
        border-radius: 4px;
    }
    
    QLabel#error_message {
        color: #ffffff;
        background-color: #000000;
        font-size: 14px;
        font-weight: bold;
        padding: 10px;
        border: 2px solid #000000;
        border-radius: 4px;
    }
    
    /* Dialog styling */
    QDialog {
        background-color: #ffffff;
        color: #000000;
    }
    
    QDialog QLabel {
        color: #000000;
        background-color: transparent;
    }
    
    QGroupBox {
        font-weight: 600;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        margin-top: 16px;
        padding: 16px 12px 12px 12px;
        color: #000000;
        background-color: #ffffff;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 12px;
        top: -8px;
        padding: 2px 8px;
        color: #000000;
        background-color: #ffffff;
        border: 1px solid #e5e5e5;
        border-radius: 4px;
        font-size: 13px;
    }
    
    QLineEdit {
        color: #000000;
        background-color: #ffffff;
        border: 1px solid #e5e5e5;
        padding: 5px;
        border-radius: 4px;
    }
    
    /* Remove border from table cell editors */
    QTableWidget QLineEdit {
        border: none;
        padding: 0px;
        margin: 0px;
        background-color: #ffffff;
        color: #000000;
        font-size: 13px;
    }
    """


def get_category_colors() -> list:
    """Get a list of distinct grayscale colors for categories."""
    return [
        '#000000',  # Black
        '#333333',  # Dark Gray
        '#666666',  # Medium Gray
        '#999999',  # Light Gray
        '#222222',  # Very Dark Gray
        '#444444',  # Dark Medium Gray
        '#555555',  # Medium Dark Gray
        '#777777',  # Medium Light Gray
        '#888888',  # Light Medium Gray
        '#aaaaaa',  # Very Light Gray
    ]


def get_category_color(index: int) -> str:
    """Get a color for a category by index."""
    colors = get_category_colors()
    return colors[index % len(colors)]

