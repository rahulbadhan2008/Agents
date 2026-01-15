#!/bin/bash

# LLM Ops RAG Pipeline - Startup Script

# 1. Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting LLM Ops RAG Pipeline Server...${NC}"

# 2. Check for .env file
if [ ! -f .env ]; then
    if [ -f .env.production.example ]; then
        echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.production.example...${NC}"
        cp .env.production.example .env
        echo -e "${RED}🛑 Please update the .env file with your actual credentials and restart.${NC}"
        exit 1
    else
        echo -e "${RED}❌ Error: .env file and .env.production.example not found.${NC}"
        exit 1
    fi
fi

# 3. Load environment variables
export $(grep -v '^#' .env | xargs)

# 4. Check for virtual environment
if [ -d "venv" ]; then
    echo -e "${GREEN}📦 Activating virtual environment...${NC}"
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo -e "${GREEN}📦 Activating virtual environment...${NC}"
    source .venv/bin/activate
fi

# 5. Run Database Initialization (Optional/If needed)
# echo -e "${YELLOW}🔄 Initializing database...${NC}"
# python -m app.db.init_db

# 6. Start FastAPI with Uvicorn
echo -e "${GREEN}🔥 Server starting at http://localhost:8000${NC}"
echo -e "${YELLOW}📝 Documentation available at http://localhost:8000/docs${NC}"

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
