#!/usr/bin/env bash
# Roda os testes de rótulo: variação nas mesmas mensagens e mensagens novas.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
source .julia/.venv/bin/activate
echo "== 1/2 Variação de rótulos (mesmas mensagens de antes)"
python -u input_ablation.py .julia/Julia-1
echo
echo "== 2/2 Mensagens novas, gabarito escrito antes de rodar"
python -u holdout.py .julia/Julia-1
