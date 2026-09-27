#!/usr/bin/env bash
# Grava a saída real de cada etapa em assets/terminal/*.log (com cores ANSI).
# Os PNGs de terminal são renderizados a partir desses logs por render_terminal.py.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
OUT="assets/terminal"
MODEL=".julia/Julia-1"
PY=".julia/.venv/bin/python"
mkdir -p "$OUT"

run() {
  local name="$1"; shift
  { printf '\033[1;32m$\033[0m %s\n' "$*"; eval "$@" 2>&1; } | tee "$OUT/$name.log"
}

run 01-ambiente "$PY -c 'import sys, torch, transformers; print(\"python\", sys.version.split()[0]); print(\"torch\", torch.__version__); print(\"transformers\", transformers.__version__)'; sysctl -n machdep.cpu.brand_string; shasum -a 256 $MODEL/model.safetensors"
run 02-casos-ptbr "$PY -u run_ptbr.py $MODEL"
run 03-variacao-rotulos "$PY -u input_ablation.py $MODEL"
run 04-msgs-novas "$PY -u holdout.py $MODEL"
REPRO_OUT=".julia/typed-cpu-capture-$(date +%H%M%S)"
DATASET="$(ls .julia/typed-cpu*/test-00000-of-00001.parquet 2>/dev/null | head -1 || true)"
run 05-reproducao-oficial "cd $MODEL && ../.venv/bin/python -u scripts/reproduce_typed.py --output ../../$REPRO_OUT ${DATASET:+--dataset ../../$DATASET} | grep -E 'done|by_type|weights_sha256'; cd - >/dev/null"
