#!/bin/bash

# Complete Fix Script
# Cleans all cache and restarts the API fresh

echo "================================================"
echo "🔧 Complete Fix - Clean Slate"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check directory
if [ ! -f "app/main.py" ]; then
    echo -e "${RED}❌ Not in project root${NC}"
    exit 1
fi

echo "Step 1: Stopping any running API processes..."
pkill -f "uvicorn app.main" 2>/dev/null || true
sleep 2
echo -e "${GREEN}✓${NC} Processes stopped"
echo ""

echo "Step 2: Cleaning all Python cache..."
# Delete all __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
# Delete all .pyc files
find . -name "*.pyc" -delete 2>/dev/null || true
# Delete all .pyo files
find . -name "*.pyo" -delete 2>/dev/null || true
echo -e "${GREEN}✓${NC} Cache cleaned"
echo ""

echo "Step 3: Fixing app/models/__init__.py..."
cat > app/models/__init__.py << 'EOF'
"""
Models Package
"""
from app.models.base import Base, BaseDBModel

__all__ = [
    "Base",
    "BaseDBModel",
]
EOF
echo -e "${GREEN}✓${NC} Fixed"
echo ""

echo "Step 4: Verifying the fix..."
cat app/models/__init__.py
echo ""

echo "Step 5: Testing imports (may take a moment)..."
python3 << 'PYEOF'
import sys
import os

# Make sure we're importing fresh
if 'app' in sys.modules:
    del sys.modules['app']
if 'app.models' in sys.modules:
    del sys.modules['app.models']
if 'app.models.user' in sys.modules:
    del sys.modules['app.models.user']

try:
    print("Testing base imports...")
    from app.models.base import Base, BaseDBModel
    print("✅ Base imports OK")
    
    print("Testing User import...")
    from app.models.user import User
    print("✅ User import OK")
    
    print("Testing app creation...")
    from app.main import app
    print("✅ App creation OK")
    
    print(f"✅ All tests passed! API has {len(app.routes)} routes")
    
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYEOF

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo -e "${GREEN}✅ All Fixed!${NC}"
    echo "================================================"
    echo ""
    echo "Starting the API now..."
    echo "Press Ctrl+C to stop"
    echo ""
    echo "Once started, open: http://localhost:8000/api/docs"
    echo ""
    sleep 2
    
    # Start the API
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
else
    echo ""
    echo "================================================"
    echo -e "${RED}❌ Still has errors${NC}"
    echo "================================================"
    echo ""
    echo "Please share the error output above for more help."
fi