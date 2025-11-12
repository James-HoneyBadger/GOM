#!/bin/bash
# DreamBerd IDE Distribution Script
# This script builds and packages the native DreamBerd IDE

set -e

echo "🏗️  Building DreamBerd IDE..."

# Build release version
cargo build --release --bin dreamberd-ide

echo "📦 Creating distribution package..."

# Create distribution directory
DIST_DIR="dreamberd-ide-$(uname -m)"
mkdir -p "$DIST_DIR"

# Copy executable
cp target/release/dreamberd-ide "$DIST_DIR/"

# Copy examples
cp -r examples "$DIST_DIR/"

# Create README for distribution
cat > "$DIST_DIR/README.txt" << 'EOF'
DreamBerd IDE - Native Edition
=============================

This is the native DreamBerd IDE, a standalone application for DreamBerd development.

Features:
- Native GUI with no external dependencies
- Code editor with syntax highlighting
- File operations (open/save)
- Real-time code execution
- Debug panel and variable inspection
- Multiple themes and font sizes

Usage:
1. Run the dreamberd-ide executable
2. Click "Open" to load a .db file from the examples/ folder
3. Edit code in the left panel
4. Click "Run" to execute
5. View output in the right panel

Examples are included in the examples/ directory.

For more information, visit: https://github.com/James-HoneyBadger/dreamberd-interpreter
EOF

# Create run script for convenience
cat > "$DIST_DIR/run_ide.sh" << 'EOF'
#!/bin/bash
# Run DreamBerd IDE
./dreamberd-ide
EOF
chmod +x "$DIST_DIR/run_ide.sh"

# Create archive
ARCHIVE_NAME="dreamberd-ide-$(uname -s | tr '[:upper:]' '[:lower:]')-$(uname -m).tar.gz"
tar -czf "$ARCHIVE_NAME" "$DIST_DIR"

echo "✅ Distribution package created: $ARCHIVE_NAME"
echo "📁 Package contents:"
ls -la "$DIST_DIR/"
echo ""
echo "To run the IDE:"
echo "  cd $DIST_DIR"
echo "  ./dreamberd-ide"
echo ""
echo "Or use the convenience script:"
echo "  ./run_ide.sh"