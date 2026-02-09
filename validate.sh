#!/bin/bash
# FOH System Validation Script
# Tests database schema, backend API setup, and frontend structure

echo "=================================="
echo "FOH System Validation"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track results
PASSED=0
FAILED=0

# Test function
test_component() {
    local name=$1
    local command=$2
    
    echo -n "Testing $name... "
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((FAILED++))
    fi
}

echo "1. Database Schema Files"
echo "------------------------"
test_component "init.sql exists" "[ -f database/init.sql ]"
test_component "schema.sql exists" "[ -f database/schema.sql ]"
test_component "indexes.sql exists" "[ -f database/indexes.sql ]"
test_component "sample_data.sql exists" "[ -f database/sample_data.sql ]"
test_component "database README exists" "[ -f database/README.md ]"
echo ""

echo "2. Backend API Files"
echo "-------------------"
test_component "app.py exists" "[ -f backend/app.py ]"
test_component "config.py exists" "[ -f backend/config.py ]"
test_component "database.py exists" "[ -f backend/database.py ]"
test_component "models.py exists" "[ -f backend/models.py ]"
test_component "requirements.txt exists" "[ -f backend/requirements.txt ]"
test_component "backend README exists" "[ -f backend/README.md ]"
test_component "Python syntax valid" "python3 -m py_compile backend/app.py backend/config.py backend/database.py backend/models.py"
echo ""

echo "3. Backend Routes"
echo "----------------"
test_component "sites route exists" "[ -f backend/routes/sites.py ]"
test_component "outplanting route exists" "[ -f backend/routes/outplanting.py ]"
test_component "photomosaics route exists" "[ -f backend/routes/photomosaics.py ]"
test_component "temperature route exists" "[ -f backend/routes/temperature.py ]"
test_component "surveys route exists" "[ -f backend/routes/surveys.py ]"
test_component "spatial route exists" "[ -f backend/routes/spatial.py ]"
echo ""

echo "4. Frontend Files"
echo "----------------"
test_component "index.html exists" "[ -f frontend/index.html ]"
test_component "styles.css exists" "[ -f frontend/css/styles.css ]"
test_component "api.js exists" "[ -f frontend/js/api.js ]"
test_component "map.js exists" "[ -f frontend/js/map.js ]"
test_component "popup.js exists" "[ -f frontend/js/popup.js ]"
test_component "charts.js exists" "[ -f frontend/js/charts.js ]"
test_component "frontend README exists" "[ -f frontend/README.md ]"
test_component "JavaScript syntax valid" "node -c frontend/js/api.js && node -c frontend/js/map.js"
echo ""

echo "5. Deployment Files"
echo "------------------"
test_component "docker-compose.yml exists" "[ -f docker-compose.yml ]"
test_component ".env.example exists" "[ -f .env.example ]"
test_component "Dockerfile exists" "[ -f backend/Dockerfile ]"
test_component "nginx.conf exists" "[ -f nginx.conf ]"
echo ""

echo "6. Documentation"
echo "---------------"
test_component "Main README exists" "[ -f README.md ]"
test_component "README has Quick Start" "grep -q 'Quick Start' README.md"
test_component "README has Architecture" "grep -q 'Architecture' README.md"
test_component "README has Deployment" "grep -q 'Deployment' README.md"
echo ""

echo "7. Database Schema Validation"
echo "----------------------------"
test_component "Schema has sites table" "grep -q 'CREATE TABLE sites' database/schema.sql"
test_component "Schema has mpas table" "grep -q 'CREATE TABLE mpas' database/schema.sql"
test_component "Schema has outplanting table" "grep -q 'CREATE TABLE outplanting_history' database/schema.sql"
test_component "Schema has photomosaics table" "grep -q 'CREATE TABLE photomosaics' database/schema.sql"
test_component "Schema has temperature table" "grep -q 'CREATE TABLE temperature_data' database/schema.sql"
test_component "Schema has growth table" "grep -q 'CREATE TABLE growth_data' database/schema.sql"
test_component "Schema has surveys table" "grep -q 'CREATE TABLE surveys' database/schema.sql"
test_component "Schema has photos table" "grep -q 'CREATE TABLE photos' database/schema.sql"
test_component "Schema uses PostGIS" "grep -q 'GEOMETRY' database/schema.sql"
test_component "Schema uses SRID 4326" "grep -q '4326' database/schema.sql"
echo ""

echo "8. API Endpoints"
echo "---------------"
test_component "Sites endpoints" "grep -q '/api/sites' backend/routes/sites.py"
test_component "Outplanting endpoints" "grep -q '/api/outplanting' backend/routes/outplanting.py"
test_component "Spatial queries" "grep -q '/api/spatial' backend/routes/spatial.py"
test_component "GeoJSON support" "grep -q 'geojson' backend/utils/geojson.py"
test_component "CORS configured" "grep -q 'CORSMiddleware' backend/app.py"
echo ""

echo "=================================="
echo "Validation Summary"
echo "=================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All validations passed!${NC}"
    echo ""
    echo "Next Steps:"
    echo "1. Setup PostgreSQL database:"
    echo "   cd database && psql -d foh_database -f init.sql -f schema.sql -f indexes.sql -f sample_data.sql"
    echo ""
    echo "2. Install backend dependencies:"
    echo "   cd backend && pip install -r requirements.txt"
    echo ""
    echo "3. Run the backend API:"
    echo "   cd backend && python app.py"
    echo ""
    echo "4. Open frontend in browser:"
    echo "   cd frontend && python -m http.server 8080"
    echo "   Then visit http://localhost:8080"
    echo ""
    echo "OR use Docker Compose:"
    echo "   docker-compose up -d"
    exit 0
else
    echo -e "${RED}✗ Some validations failed${NC}"
    exit 1
fi
