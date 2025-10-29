#!/bin/bash
# Quick Start Script for ConversAI (Mac/Linux)
# This script helps you set up and test ConversAI quickly

echo "============================================================"
echo "  ConversAI - Quick Start Setup"
echo "============================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check Python installation
echo -e "${GREEN}[1/6] Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "  ${GREEN}✓ Python found: $PYTHON_VERSION${NC}"
else
    echo -e "  ${RED}✗ Python not found! Please install Python 3.11+${NC}"
    exit 1
fi

# Check if in correct directory
echo -e "\n${GREEN}[2/6] Checking directory structure...${NC}"
if [ ! -d "backend" ]; then
    echo -e "  ${RED}✗ Backend folder not found! Are you in the conversai directory?${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓ Directory structure looks good${NC}"

# Check for .env file
echo -e "\n${GREEN}[3/6] Checking environment configuration...${NC}"
if [ ! -f ".env" ]; then
    echo -e "  ${YELLOW}ℹ .env file not found. Creating from template...${NC}"
    cp .env.example .env
    echo -e "  ${GREEN}✓ Created .env file${NC}"
    echo ""
    echo -e "  ${RED}⚠ IMPORTANT: Edit .env and add your GROQ_API_KEY!${NC}"
    echo -e "  ${CYAN}Get it from: https://console.groq.com${NC}"
    echo ""
    read -p "  Have you added your GROQ_API_KEY? (y/n): " continue
    if [ "$continue" != "y" ]; then
        echo -e "  ${YELLOW}Please add your API key to .env and run this script again.${NC}"
        exit 0
    fi
else
    echo -e "  ${GREEN}✓ .env file exists${NC}"
    
    # Check if GROQ_API_KEY is set
    if grep -q "GROQ_API_KEY=gsk_" .env; then
        echo -e "  ${GREEN}✓ GROQ_API_KEY appears to be configured${NC}"
    else
        echo -e "  ${YELLOW}⚠ GROQ_API_KEY may not be configured correctly${NC}"
        echo -e "  ${YELLOW}Make sure it starts with 'gsk_'${NC}"
    fi
fi

# Create virtual environment
echo -e "\n${GREEN}[4/6] Setting up Python virtual environment...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo -e "  ${CYAN}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "  ${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "  ${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo -e "\n${GREEN}[5/6] Installing dependencies...${NC}"
echo -e "  ${CYAN}This may take 2-3 minutes...${NC}"

pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

if [ $? -eq 0 ]; then
    echo -e "  ${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "  ${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi

# Test import
echo -e "\n${GREEN}[6/6] Testing installation...${NC}"
TEST_RESULT=$(python3 -c "
try:
    import fastapi
    import groq
    import sqlalchemy
    print('SUCCESS')
except ImportError as e:
    print(f'ERROR: {e}')
")

if [ "$TEST_RESULT" = "SUCCESS" ]; then
    echo -e "  ${GREEN}✓ All dependencies working correctly${NC}"
else
    echo -e "  ${RED}✗ Dependency test failed: $TEST_RESULT${NC}"
    exit 1
fi

# Success message
echo ""
echo "============================================================"
echo -e "  ${GREEN}✓ Setup Complete! ConversAI is ready to run.${NC}"
echo "============================================================"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "  ${NC}1. Start the server:${NC}"
echo -e "     ${CYAN}uvicorn app.main:app --reload${NC}"
echo ""
echo -e "  ${NC}2. Open your browser to:${NC}"
echo -e "     ${CYAN}http://localhost:8000/docs${NC}"
echo ""
echo -e "  ${NC}3. Try a test query:${NC}"
echo -e '     ${CYAN}{"message": "What is Bitcoin'"'"'s price?"}${NC}'
echo ""
echo -en "${YELLOW}Would you like to start the server now? (y/n): ${NC}"
read start_now

if [ "$start_now" = "y" ]; then
    echo ""
    echo -e "${GREEN}Starting ConversAI server...${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
    echo ""
    uvicorn app.main:app --reload
else
    echo ""
    echo -e "${YELLOW}To start the server later, run:${NC}"
    echo -e "  ${CYAN}cd backend${NC}"
    echo -e "  ${CYAN}source venv/bin/activate${NC}"
    echo -e "  ${CYAN}uvicorn app.main:app --reload${NC}"
fi
