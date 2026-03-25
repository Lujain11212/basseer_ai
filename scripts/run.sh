#!/bin/bash
set -e
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "═══════════════════════════════════════════════════"
echo "  🛡️  بصير AI – الحارس الدلالي v2"
echo "═══════════════════════════════════════════════════"

# Python
PYTHON=${PYTHON:-python3}
command -v $PYTHON &>/dev/null || { echo "❌ Python not found"; exit 1; }
echo "🐍 $($PYTHON --version)"

# .env
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📄 تم إنشاء .env من .env.example"
fi

# Venv
if [ ! -d venv ]; then
    echo "📦 إنشاء البيئة الافتراضية..."
    $PYTHON -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt -q

# Generate dataset
echo "📊 توليد البيانات التجريبية..."
$PYTHON scripts/generate_dataset.py

# Backend
echo "🚀 تشغيل Backend على المنفذ 8000..."
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload &
sleep 3

# Ingest
echo "📥 إدخال البيانات..."
$PYTHON scripts/ingest_dataset.py

# Dashboard
echo "🖥️  تشغيل Dashboard على المنفذ 8501..."
streamlit run dashboard/app.py --server.port 8501 --server.headless true &

echo ""
echo "═══════════════════════════════════════════════════"
echo "  ✅ Backend:   http://127.0.0.1:8000"
echo "  ✅ API Docs:  http://127.0.0.1:8000/docs"
echo "  ✅ Dashboard: http://127.0.0.1:8501"
echo "  Ctrl+C لإيقاف"
echo "═══════════════════════════════════════════════════"
wait
