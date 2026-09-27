#!/usr/bin/env bash
# Roda a análise completa do Julia 1: casos pt-BR, controles e reprodução oficial.
# Uso: ./run_all.sh [pasta_base]  (padrão: .julia ao lado deste script)
# Na primeira vez cria o venv e baixa o modelo (cerca de 550 MB) do Hugging Face.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
BASE="${1:-$HERE/.julia}"
MODEL="$BASE/Julia-1"
mkdir -p "$BASE"

if [ ! -f "$BASE/.venv/bin/activate" ]; then
  echo "== Preparando ambiente Python em $BASE/.venv"
  python3.12 -m venv "$BASE/.venv"
fi
source "$BASE/.venv/bin/activate"

if [ ! -f "$MODEL/model.safetensors" ]; then
  echo "== Baixando SupersonicLabs/Julia-1 do Hugging Face"
  pip install -q huggingface_hub
  python -c "from huggingface_hub import snapshot_download; snapshot_download('SupersonicLabs/Julia-1', local_dir='$MODEL')"
fi
if ! python -c "import julia, pyarrow" 2>/dev/null; then
  echo "== Instalando o pacote do Julia e dependências"
  pip install -q -e "$MODEL" pyarrow
fi

echo "== 1/3 Casos pt-BR (roteamento, urgência, sim/não, sentimento)"
cd "$HERE" && python -u run_ptbr.py "$MODEL"

echo
echo "== 2/3 Controles: pt vs en, descrição longa vs rótulo curto"
cd "$HERE" && python -u controls.py "$MODEL"

echo
echo "== 3/3 Reprodução oficial (typed decisions, 2.000 perguntas, leva uns 3 min)"
OUT="$BASE/typed-cpu-$(date +%H%M%S)"
DATASET="$(ls "$BASE"/typed-cpu*/test-00000-of-00001.parquet 2>/dev/null | head -1 || true)"
cd "$MODEL" && python -u scripts/reproduce_typed.py --output "$OUT" ${DATASET:+--dataset "$DATASET"}
python - "$OUT/results.json" <<'EOF'
import json, sys
r = json.load(open(sys.argv[1]))
def find(d):
    if isinstance(d, dict):
        if {"choice", "noul", "score"} <= d.keys():
            return d
        for v in d.values():
            hit = find(v)
            if hit:
                return hit
t = find(r)
print("\nReprodução:", {k: f'{t[k]["correct"]}/{t[k]["count"]}' for k in ("choice", "score", "noul")})
print("README (CPU FP32, 26/09): choice 426/600, score 542/800, noul 483/600")
EOF
