set -e

echo "Flask Blog Setup"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Python 3 found: $(python3 --version)"
echo ""

if [ ! -d "venv" ]; then
    echo "Creating virtual environment"
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi
echo ""

echo "Activating virtual environment"
source venv/bin/activate
echo "Virtual environment activated"
echo ""

echo "Upgrading pip"
pip install --upgrade pip > /dev/null
echo "pip upgraded"
echo ""

echo "Installing dependencies from requirements.txt"
pip install -r requirements.txt
echo "All dependencies installed"
echo ""

echo "Creating necessary platform specific directories"
mkdir -p uploads
mkdir -p app/static/assets
echo "Directories created"

echo ""
echo "Setup Complete!"
echo ""