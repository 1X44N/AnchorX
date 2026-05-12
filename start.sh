#!/bin/bash
echo "============================================"
echo "  WRITERX 2026 - AI Humanizer"
echo "  Starting application..."
echo "============================================"
echo ""
pip3 install -r requirements.txt -q 2>/dev/null || pip install -r requirements.txt -q 2>/dev/null
echo ""
echo "Launching WriterX 2026..."
python3 main.py || python main.py
