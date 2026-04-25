#!/bin/bash
# K10 Chat — Configuração Automática (Mac / Linux)
# Uso: ./setup.sh <URL_DO_RENDER>
# Ex:  ./setup.sh k10-signaling.onrender.com

if [ -z "$1" ]; then
  echo ""
  echo "============================================================"
  echo "  K10 Chat — Configuração Automática"
  echo "============================================================"
  echo ""
  echo "  Uso:"
  echo "    ./setup.sh <URL_DO_SEU_SERVIDOR>"
  echo ""
  echo "  Exemplo:"
  echo "    ./setup.sh k10-signaling.onrender.com"
  echo ""
  exit 1
fi

python3 setup.py "$1"
