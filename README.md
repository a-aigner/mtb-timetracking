# MTB Time Tracker

A cross-platform desktop application for tracking finish times in marathons and mountain bike races with multiple categories.

## Features

- **Multi-Category Support**: Load multiple CSV files as different race categories
- **Independent Timers**: Each category has its own timer that can be started independently
- **Fast Input**: Type participant ID + Enter to record finish times instantly
- **Session Management**: Auto-save functionality with manual save/load options
- **Excel Export**: Generate multi-sheet Excel reports with all results
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Detailed Setup

Follow these step-by-step instructions to set up the MTB Time Tracker on your computer.

#### Step 1: Clone the Repository

Open your terminal (Command Prompt on Windows, Terminal on macOS/Linux) and run:

```bash
git clone https://github.com/a-aigner/mtb-timetracking.git
cd mtb-timetracking
```

#### Step 2: Create a Virtual Environment

A virtual environment keeps the project dependencies isolated from your system Python installation.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear at the beginning of your command prompt, indicating the virtual environment is active.

#### Step 3: Install Dependencies

With the virtual environment activated, install all required packages:

```bash
pip install -r requirements.txt
```

This will install:
- PyQt6 (GUI framework)
- pandas (data handling)
- openpyxl (Excel export)
- pyinstaller (for building executables)

#### Step 4: Run the Application

Start the application with:

```bash
python main.py
```

The MTB Time Tracker window should open and be ready to use!

#### Step 5: (Optional) Deactivate Virtual Environment

When you're done using the application, you can deactivate the virtual environment:

```bash
deactivate
```

### Quick Start After Initial Setup

Once you've completed the initial setup, you only need to:

1. Navigate to the project directory:
   ```bash
   cd mtb-timetracking
   ```

2. Activate the virtual environment:
   - **Windows**: `venv\Scripts\activate`
   - **macOS/Linux**: `source venv/bin/activate`

3. Run the application:
   ```bash
   python main.py
   ```

## Usage

### Loading Categories

1. Click "Load Category" button
2. Browse and select a CSV file with participant data (no header row needed)
3. Preview the data and select which column contains the participant IDs (e.g., "Column A")
4. Enter a name for the category (e.g., "MTB", "E-MTB")
5. Click "Load Category"

**Note**: The preview will show columns labeled as A, B, C, D, etc. Simply select which column contains your participant IDs.

### CSV Format

CSV files should contain participant data **WITHOUT header rows**. The app will automatically assign column letters (A, B, C, etc.).

Expected column order:
- **Column A**: ID (required)
- **Column B**: First Name
- **Column C**: Last Name
- **Column D**: Team
- **Column E**: Birth Year
- **Column F**: Gender

Example structure (no header row):

```csv
101;John;Doe;Team A;1990;M
102;Jane;Smith;Team B;1985;F
103;Bob;Johnson;Team C;1988;M
```

Supported delimiters: semicolon (`;`), comma (`,`), tab

**Note**: When loading, you'll select which column contains the ID (e.g., "Column A"). The app will automatically map the other columns in order.

### Recording Finish Times

1. Start the timer for a category by clicking its "Start Timer" button
2. When a participant crosses the finish line:
   - Type their ID in the input field at the top
   - Press Enter
3. The system will:
   - Automatically detect their category
   - Record their finish time
   - Display their information in the recent entries

### Keyboard Shortcuts

- **Ctrl+S**: Save session manually
- **Ctrl+E**: Export results to Excel
- **Ctrl+Z**: Undo last entry
- **Ctrl+N**: Start new session
- **Ctrl+L**: Load new category
- **Enter**: Submit participant ID

### Managing Entries

- **Recent Entries**: View last entries in each category widget and at the bottom
- **Edit Time**: Right-click on an entry in a category to edit time
- **Delete Entry**: Right-click on an entry to delete it
- **Mark DNF**: Right-click to mark a participant as "Did Not Finish"
- **Undo**: Click "Undo Last" or press Ctrl+Z to undo the most recent entry

### Exporting Results

1. Click "Export Results" (or press Ctrl+E)
2. Choose a location and filename
3. The Excel file will contain:
   - One sheet per category (sorted by finish time)
   - One "All Results" sheet with combined data
   - All original participant data plus finish times

### Session Management

- **Auto-Save**: Sessions are automatically saved every 30 seconds
- **Manual Save**: Click "Save Session" or press Ctrl+S
- **Resume Session**: On startup, you'll be prompted to resume the last session
- **End Session**: Click "End Session" to clear data and start fresh

## Building Executables

To create standalone executables for distribution:

### Windows

```bash
python build_windows.py
```

The executable will be in `dist/MTBTimeTracker/`

### macOS

```bash
python build_macos.py
```

The app bundle will be in `dist/MTBTimeTracker.app`

### Linux

```bash
python build_linux.py
```

The executable will be in `dist/MTBTimeTracker/`

## Data Storage

Application data is stored in platform-specific locations:

- **Windows**: `%APPDATA%\MTBTimeTracker\`
- **macOS**: `~/Library/Application Support/MTBTimeTracker/`
- **Linux**: `~/.local/share/MTBTimeTracker/`

This includes:
- Session files (`sessions/`)
- Backup files (`backups/`)

## Tips for Race Day

1. **Preparation**:
   - Load all category CSV files before the race
   - Test the input system to ensure smooth operation
   - Position your computer near the finish line

2. **During the Race**:
   - Start timers as each category begins
   - Keep the input field focused (it auto-focuses after each entry)
   - Watch the status messages for feedback
   - Use the recent entries preview to verify correct entries

3. **After the Race**:
   - Stop all timers
   - Review entries for any errors
   - Export results to Excel
   - Save the session as backup

4. **Handling Issues**:
   - If you enter a wrong ID, immediately click "Undo Last"
   - Invalid IDs are recorded but highlighted in yellow - fix them after the race
   - Use the context menu to edit times if needed

## Troubleshooting

### CSV won't load
- Check that the file uses semicolon, comma, or tab as delimiter
- Ensure the file has data rows (no header row needed)
- Try opening the CSV in a text editor to verify format
- Make sure the ID column (usually first column) contains unique values

### Timer not accurate
- The timer updates every 100ms for display
- Actual finish times are recorded with millisecond precision
- Close other heavy applications for best performance

### Application won't start
- Ensure Python 3.8+ is installed: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
- Check console for error messages

## License

This application is provided as-is for time measurement at sporting events.

## Support

For issues, questions, or feature requests, please contact the development team.

