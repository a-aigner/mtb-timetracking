# Quick Start Guide

## Getting Started in 5 Minutes

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python main.py
```

### 3. Load Your Categories

1. Click **"Load Category"** button
2. Browse to `sample-files/mtb.csv`
3. Select **"Column A (Index 0)"** as the ID column (this is usually the participant ID)
4. Name it "MTB"
5. Click **"Load Category"**
6. Repeat for `sample-files/e-mtb.csv` and name it "E-MTB"

**Note**: CSV files should have no header row. The app shows columns as A, B, C, etc.

### 4. Start Racing!

1. Click **"Start Timer"** on the first category when they start
2. Type participant IDs in the input field at the top
3. Press **Enter** after each ID
4. The app automatically:
   - Detects which category the ID belongs to
   - Records the finish time
   - Shows participant name and time
   - Displays recent finishers

### 5. Export Results

When done:
1. Click **"Export Results"**
2. Choose where to save the Excel file
3. Done! The file will have separate sheets for each category plus a combined "All Results" sheet

## Key Features at a Glance

### Fast Input
- Just type ID + Enter
- Auto-focus after each entry
- Visual feedback for each entry
- Warnings for invalid IDs (but still records them)

### Live Timers
- Each category has its own timer
- Updates in real-time
- Shows elapsed time since start
- Color-coded for easy identification

### Smart Category Detection
- Automatically finds which category an ID belongs to
- Handles multiple categories finishing at the same time
- Warns if ID not found but still records

### Session Management
- Auto-saves every 30 seconds
- Can manually save anytime (Ctrl+S)
- Resume previous session on startup
- All data stored safely

### Excel Export
- One sheet per category (sorted by time)
- Combined "All Results" sheet
- Includes all original CSV data
- Adds finish time and elapsed time columns

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Submit participant ID |
| `Ctrl+S` | Save session |
| `Ctrl+E` | Export results |
| `Ctrl+Z` | Undo last entry |
| `Ctrl+N` | New session |
| `Ctrl+L` | Load category |

## Tips

1. **Keep input field focused** - It auto-focuses after each entry
2. **Watch the status bar** - Shows feedback for each entry
3. **Use Undo** - Made a mistake? Hit Ctrl+Z immediately
4. **Check recent entries** - Bottom table shows last 20 entries across all categories
5. **Right-click entries** - Edit time, delete, or mark as DNF
6. **Export often** - Better safe than sorry!

## File Structure

```
time-measurement-mtb/
├── main.py              # Run this to start
├── requirements.txt     # Dependencies
├── README.md           # Full documentation
├── QUICKSTART.md       # This file
├── sample-files/       # Your CSV files
│   ├── mtb.csv
│   └── e-mtb.csv
└── src/                # Application code
    ├── core/           # Data models
    ├── ui/             # User interface
    └── utils/          # Utilities
```

## Troubleshooting

**App won't start?**
```bash
pip install -r requirements.txt --force-reinstall
```

**CSV won't load?**
- Check it uses `;`, `,`, or tab as delimiter
- CSV files should have NO header row - just data
- First column should typically be the ID column

**Wrong entry?**
- Click "Undo Last" or press Ctrl+Z

**Need to edit a time?**
- Right-click the entry in the category widget

## Building Executables

### For Windows:
```bash
python build_windows.py
```

### For macOS:
```bash
python build_macos.py
```

### For Linux:
```bash
python build_linux.py
```

The executable will be in the `dist/` folder.

---

**Ready to track some times? Run `python main.py` and get started!**

