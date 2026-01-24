#!/bin/bash

# Fix Import Errors Script
# This script fixes all circular import issues in the project

echo "================================================"
echo "🔧 Fixing Import Errors"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    echo -e "${RED}❌ Error: Not in project root directory${NC}"
    echo "Please run this script from: ~/SonmaHairAPI"
    exit 1
fi

echo "Step 1: Fixing app/models/__init__.py..."
cat > app/models/__init__.py << 'EOF'
"""
Models Package
"""
# Import base classes only to avoid circular imports
from app.models.base import Base, BaseDBModel

__all__ = [
    "Base",
    "BaseDBModel",
]
EOF
echo -e "${GREEN}✓${NC} Fixed app/models/__init__.py"
echo ""

echo "Step 2: Checking alembic/env.py imports..."
# Check if alembic/env.py needs fixing
if grep -q "from app.models import" alembic/env.py 2>/dev/null; then
    echo -e "${YELLOW}⚠${NC} Found incorrect imports in alembic/env.py"
    echo "   Fixing..."
    
    # Fix the imports in alembic/env.py
    sed -i.bak 's/from app\.models import Users/from app.models.user import Users/g' alembic/env.py
    sed -i.bak 's/from app\.models import Addresses/from app.models.address import Addresses/g' alembic/env.py
    sed -i.bak 's/from app\.models import AuditTrail/from app.models.audit import AuditTrail/g' alembic/env.py
    sed -i.bak 's/from app\.models import BranchLocations/from app.models.branch import BranchLocations/g' alembic/env.py
    
    echo -e "${GREEN}✓${NC} Fixed alembic/env.py"
else
    echo -e "${GREEN}✓${NC} alembic/env.py is already correct"
fi
echo ""

echo "Step 3: Checking for other incorrect imports..."
# Search for problematic imports in all Python files
found_issues=0

for file in $(find app -name "*.py" -type f); do
    if grep -q "from app\.models import Users" "$file" 2>/dev/null; then
        echo -e "${YELLOW}⚠${NC} Found issue in: $file"
        sed -i.bak 's/from app\.models import Users/from app.models.user import Users/g' "$file"
        found_issues=1
    fi
    if grep -q "from app\.models import Addresses" "$file" 2>/dev/null; then
        echo -e "${YELLOW}⚠${NC} Found issue in: $file"
        sed -i.bak 's/from app\.models import Addresses/from app.models.address import Addresses/g' "$file"
        found_issues=1
    fi
    if grep -q "from app\.models import AuditTrail" "$file" 2>/dev/null; then
        echo -e "${YELLOW}⚠${NC} Found issue in: $file"
        sed -i.bak 's/from app\.models import AuditTrail/from app.models.audit import AuditTrail/g' "$file"
        found_issues=1
    fi
done

if [ $found_issues -eq 0 ]; then
    echo -e "${GREEN}✓${NC} No issues found in app/ directory"
else
    echo -e "${GREEN}✓${NC} Fixed all import issues"
fi
echo ""

echo "Step 4: Cleaning up backup files..."
find . -name "*.bak" -delete
echo -e "${GREEN}✓${NC} Cleaned up backup files"
echo ""

echo "Step 5: Testing imports..."
python3 << 'PYEOF'
import sys
try:
    # Test base imports
    from app.models.base import Base, BaseDBModel
    print("✅ Base imports OK")
    
    # Test individual model imports
    from app.models.user import Users
    print("✅ Users import OK")
    
    from app.models.address import Addresses
    print("✅ Addresses import OK")
    
    from app.models.audit import AuditTrail
    print("✅ AuditTrail import OK")
    
    from app.models.branch import BranchLocations
    print("✅ BranchLocations import OK")
    
    print("\n✅ All imports successful!")
    sys.exit(0)
    
except Exception as e:
    print(f"\n❌ Import test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYEOF

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo -e "${GREEN}✅ All Fixes Applied Successfully!${NC}"
    echo "================================================"
    echo ""
    echo "Next steps:"
    echo "1. Restart your API (if running, press Ctrl+C and restart)"
    echo "2. Run: uvicorn app.main:app --reload"
    echo "3. Test: http://localhost:8000/api/docs"
    echo ""
else
    echo ""
    echo "================================================"
    echo -e "${RED}❌ Import Test Failed${NC}"
    echo "================================================"
    echo ""
    echo "There are still import issues. Check the error above."
    echo "You may need to manually check your imports."
    echo ""
fi