"""
MTB Time Tracker - Time measurement tool for marathons and mountain bike trails.

Main entry point for the application.
"""
import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.ui.styles import get_app_stylesheet


def main():
    """Main application entry point."""
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("MTB Time Tracker")
    app.setOrganizationName("MTB Time Tracker")
    
    # Apply stylesheet
    app.setStyleSheet(get_app_stylesheet())
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

