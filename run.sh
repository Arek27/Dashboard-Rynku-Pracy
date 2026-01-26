#!/bin/bash
cd "$(dirname "$0")"

echo "Uruchamianie aplikacji Streamlit: Dashboard – Rynek Pracy"
echo "-----------------------------------------------"

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

streamlit run app.py
