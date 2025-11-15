# Gulf of Mexico Web IDE Guide

## Quick Start

```bash
# Launch the Web IDE
python -m gulfofmexico.ide --web

# Or use the shortcut script
./run_web_ide.sh
```

The IDE will open automatically at: **http://localhost:8080/ide**

## Features

### 💾 Save Files
- Click **Save** button or press `Ctrl+S`
- Enter filename (`.gom` extension added automatically)
- Files are saved in the current workspace directory

### 📁 Load Files
- Click **Load** button or press `Ctrl+O`
- Browse all `.gom` files in the workspace
- Click a file to select it, then click **Load**

### ▶ Run Code
- Click **Run** button or press `Ctrl+Enter`
- Output appears in the right pane
- Errors shown in red, output in cyan

### 📝 Editor Features
- Syntax highlighting area
- Tab inserts 3 spaces (Gulf of Mexico standard)
- Example code snippets available in dropdown

### 🎨 Example Programs
Choose from pre-loaded examples:
- **Hello World** - Basic printing
- **Variables** - const/var declarations
- **Arrays** - -1 indexing and float indices
- **Functions** - Function definitions
- **Temporal** - current() and previous() keywords

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Run code |
| `Ctrl+S` | Save file |
| `Ctrl+O` | Load file |
| `Tab` | Insert 3 spaces |

## File Management

### Where Files Are Saved
Files are saved relative to where you launched the IDE:
```bash
# If you run from /home/james/GOM
# Files save to /home/james/GOM/your_file.gom
```

### Security
- Can only access `.gom` files
- Cannot access hidden directories (starting with `.`)
- Cannot save/load outside workspace directory

## Tips

1. **Auto-save**: Files are saved immediately when you click Save
2. **Status updates**: Watch the blue status bar for confirmation messages
3. **File list**: Refreshes each time you open the Load dialog
4. **Current file**: The IDE remembers which file you're working on

## Troubleshooting

**Port already in use?**
```bash
# Use a different port
python -m gulfofmexico.ide --web
```

**Can't see your file?**
- Make sure it has a `.gom` extension
- Check it's not in a hidden directory
- Refresh by closing and reopening the Load dialog

**Browser didn't open?**
- Manually visit http://localhost:8080/ide
- Check firewall settings

## Advantages Over Qt GUI

✅ Works on any system (no CPU requirements)  
✅ No Qt dependencies needed  
✅ Access from any browser  
✅ Lightweight and fast  
✅ Easy to deploy  

Enjoy coding in Gulf of Mexico! 🌊
