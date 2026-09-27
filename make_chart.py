# Gera as imagens dos resultados do Julia 1 em pt-BR a partir de julia1_ptbr_results.json.
# Saída: assets/julia1-ptbr-resultados.png (principal) e assets/thread/*.png (uma por mensagem).
import json
import math
import os
import shutil
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
    "axes.edgecolor": "#c9c9c9", "axes.linewidth": 0.8,
    "xtick.color": "#555", "ytick.color": "#555", "text.color": "#2b2b2b",
    "figure.dpi": 200,
})
RED, GRAY, GREEN, BLUE, INK, MUTED = "#d1495b", "#b8b8b8", "#2e8b70", "#3f6a8a", "#2b2b2b", "#777"
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
THREAD = os.path.join(ASSETS, "thread")
os.makedirs(THREAD, exist_ok=True)

with open(os.path.join(HERE, "julia1_ptbr_results.json")) as handle:
    data = json.load(handle)
HOLD, LV = data["holdout"], data["label_variants"]
REPRO = data["official_reproduction"]["by_type"]
LATENCY = data["first_test_ptbr"]["latency_ms"]["median"]

VARIANTS = [("original", "descrição original pt"), ("short_pt", "rótulo curto pt"),
            ("en", "pergunta e rótulos em inglês"), ("clean", "descrição reescrita pt")]
HOLD_KEYS = {"original": "{t}_original", "short_pt": "{t}_short_pt",
             "en": "{t}_question_labels_en", "clean": "{t}_clean"}
LV_KEYS = {"original": "original_pt", "short_pt": "short_pt", "en": "labels_en_msg_pt", "clean": "clean_pt"}
COLORS = {"original": GRAY, "short_pt": "#9aa9b5", "en": BLUE, "clean": GREEN}
FOOT = ("SupersonicLabs/Julia-1 · CPU local, PyTorch 2.14 FP32, strict encoding, 1.024 tokens · "
        "54 msgs sintéticas em pt-BR geradas por IA, gabarito antes de rodar · 27/09/2026")


def hold(task, variant):
    return HOLD[HOLD_KEYS[variant].format(t=task)]


def header(fig, title, subtitle):
    fig.text(0.05, 0.955, title, fontsize=16, fontweight="bold", va="top")
    fig.text(0.05, 0.885, subtitle, fontsize=9.8, color=MUTED, va="top")


def footer(fig, text=FOOT):
    fig.text(0.05, 0.02, text, fontsize=7.6, color="#999")


def hbars(ax, task, title):
    labels, values, totals, colors = [], [], [], []
    for key, name in VARIANTS:
        result = hold(task, key)
        labels.append(name); values.append(result["correct"]); totals.append(result["total"])
        colors.append(COLORS[key])
    y = range(len(labels))[::-1]
    pct = [v / t * 100 for v, t in zip(values, totals)]
    ax.barh(list(y), pct, color=colors, height=0.6)
    for yi, p, v, t in zip(y, pct, values, totals):
        ax.text(p + 2, yi, f"{v}/{t}", va="center", fontsize=10, fontweight="bold", color=INK)
    ax.set_yticks(list(y), labels, fontsize=9.5)
    ax.set_xlim(0, 115); ax.set_xticks([0, 50, 100], ["0%", "50%", "100%"], fontsize=8.5)
    ax.tick_params(axis="y", length=0)
    ax.spines["bottom"].set_visible(False)
    ax.grid(axis="x", color="#eee", lw=0.8); ax.set_axisbelow(True)
    ax.set_title(title, fontsize=11.5, fontweight="bold", pad=10, loc="left")


def save(fig, path):
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(path)


# 0) principal: mensagens novas, 4 redações de rótulo, nas duas tarefas
fig = plt.figure(figsize=(12, 5.6))
header(fig, "Julia 1 em pt-BR: o acerto depende de como o rótulo é escrito",
       "mesmas 22 mensagens novas, 4 redações de rótulo · nenhuma redação ganhou nas duas tarefas")
gs = fig.add_gridspec(1, 2, left=0.2, right=0.97, top=0.78, bottom=0.14, wspace=0.75)
hbars(fig.add_subplot(gs[0, 0]), "routing", "Roteamento em 6 times (16 msgs)")
hbars(fig.add_subplot(gs[0, 1]), "sentiment", "Sentimento em 3 classes (6 msgs)")
footer(fig)
save(fig, os.path.join(ASSETS, "julia1-ptbr-resultados.png"))
shutil.copy(os.path.join(ASSETS, "julia1-ptbr-resultados.png"), os.path.join(THREAD, "0-principal.png"))

# 1) contexto: reprodução oficial
fig = plt.figure(figsize=(10, 4.6))
header(fig, "O teste oficial deles bateu exato",
       "scripts/reproduce_typed.py do repositório do modelo, 2.000 perguntas, CPU FP32")
ax = fig.add_axes([0.05, 0.14, 0.9, 0.62]); ax.axis("off")
readme = {"choice": "426/600", "score": "542/800", "noul": "483/600"}
names = {"choice": "escolha", "score": "escala", "noul": "sim/não"}
cols = [0.0, 0.3, 0.58]
for x, text in zip(cols, ["tipo", "rodei aqui", "publicado no README"]):
    ax.text(x, 0.92, text, fontsize=10.5, fontweight="bold", color="#888", transform=ax.transAxes)
ax.plot([0, 0.9], [0.84, 0.84], color="#ddd", lw=0.8, transform=ax.transAxes)
for r, key in enumerate(["choice", "score", "noul"]):
    y = 0.66 - r * 0.22
    mine = f'{REPRO[key]["correct"]}/{REPRO[key]["count"]}'
    ax.text(cols[0], y, names[key], fontsize=13, color="#555", transform=ax.transAxes)
    ax.text(cols[1], y, mine, fontsize=13, fontweight="bold", transform=ax.transAxes)
    ax.text(cols[2], y, readme[key], fontsize=13, transform=ax.transAxes)
    ax.text(0.86, y, "igual" if mine == readme[key] else "diferente", fontsize=11,
            color=GREEN if mine == readme[key] else RED, fontweight="bold", transform=ax.transAxes)
weights = (data.get("weights_sha256") or "")[:12]
footer(fig, f"pesos sha256 {weights}…, o mesmo do anúncio · 144,3M parâmetros sobre mmBERT-small · "
            f"mediana de {LATENCY:.0f} ms por decisão nesta rodada, 18 a 35 ms entre rodadas (Apple M5, CPU, 4 threads)")
save(fig, os.path.join(THREAD, "1-contexto.png"))

# 2) roteamento: para onde as msgs novas foram
teams = ["financeiro", "matricula", "bolsa", "acesso", "cancelamento", "academico"]
team_colors = dict(zip(teams, ["#3f6a8a", RED, "#e0a458", "#76b7b2", "#8c6d9e", GREEN]))
rows = [("gabarito", Counter(c["gold"] for c in HOLD["routing_original"]["cases"]))]
for key, name in [("original", "descrição original pt"), ("en", "pergunta e rótulos em inglês"),
                  ("clean", "descrição reescrita pt")]:
    result = hold("routing", key)
    rows.append((f'{name}  ({result["correct"]}/{result["total"]})',
                 Counter(c["pred"] for c in result["cases"])))
fig = plt.figure(figsize=(12, 5.2))
matricula = rows[1][1]["matricula"]
header(fig, f"Com a descrição original, {matricula} de 16 msgs novas foram pra matrícula",
       "para qual time cada redação de rótulo mandou as mesmas 16 mensagens")
ax = fig.add_axes([0.27, 0.2, 0.68, 0.58])
for i, (name, counts) in enumerate(rows[::-1]):
    left = 0
    for team in teams:
        n = counts.get(team, 0)
        if n:
            ax.barh(i, n, left=left, color=team_colors[team], height=0.62, edgecolor="white", lw=1)
            ax.text(left + n / 2, i, str(n), ha="center", va="center", fontsize=9.5, color="white",
                    fontweight="bold")
            left += n
ax.set_yticks(range(len(rows)), [r[0] for r in rows[::-1]], fontsize=9.8)
ax.set_xlim(0, 16); ax.set_xticks([]); ax.spines["bottom"].set_visible(False)
ax.tick_params(axis="y", length=0)
handles = [plt.Rectangle((0, 0), 1, 1, color=team_colors[t]) for t in teams]
ax.legend(handles, teams, frameon=False, fontsize=9, ncol=6, loc="upper center",
          bbox_to_anchor=(0.5, -0.04))
stable = sum(r["pred"] == r["pred_reversed"] for r in data["first_test_ptbr"]["routing"])
footer(fig, f"invertendo só a ordem das opções, {24 - stable} de 24 respostas mudam (1º teste) · "
            "3 descrições originais citavam \"curso\", mas a versão em inglês também repete \"course\" e acertou mais")
save(fig, os.path.join(THREAD, "2-roteamento.png"))

# 3) sentimento: 4 redações, nos dois conjuntos
fig = plt.figure(figsize=(12, 5.2))
header(fig, "Sentimento vai de 2 a 6 acertos só trocando o rótulo",
       "mesmas mensagens, 4 redações de rótulo · 1º teste com 8 msgs, msgs novas com 6")
ax = fig.add_axes([0.07, 0.2, 0.88, 0.56])
groups = [("1º teste (8 msgs)", lambda k: LV["sentiment"][LV_KEYS[k]]),
          ("msgs novas (6 msgs)", lambda k: hold("sentiment", k))]
w = 0.19
for gi, (gname, getter) in enumerate(groups):
    for vi, (key, name) in enumerate(VARIANTS):
        result = getter(key)
        x = gi + (vi - 1.5) * w
        pct = result["correct"] / result["total"] * 100
        ax.bar(x, pct, w * 0.92, color=COLORS[key], label=name if gi == 0 else None)
        ax.text(x, pct + 2, f'{result["correct"]}/{result["total"]}', ha="center", fontsize=9.5,
                fontweight="bold")
ax.set_xticks([0, 1], [g[0] for g in groups], fontsize=10)
ax.set_ylim(0, 112); ax.set_yticks([0, 50, 100], ["0%", "50%", "100%"], fontsize=8.5)
ax.tick_params(axis="y", length=0); ax.grid(axis="y", color="#eee", lw=0.8); ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=9, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.1))
footer(fig, "o 6/6 é em 6 mensagens: intervalo de 95% (Wilson) de 61% a 100% · "
            "rótulos em inglês são tradução direta dos originais, escritos antes de ver erros")
save(fig, os.path.join(THREAD, "3-sentimento.png"))

# 4) treino: fatos com fonte, sem gráfico (não medimos fine-tuning)
fig = plt.figure(figsize=(10, 4.8))
header(fig, "Antes de decidir treinar: o que já dá pra afirmar",
       "nada aqui mede fine-tuning, isso é a pergunta em aberto")
facts = [
    ("R$540", "gasto de GPU no treino e experimentos do Julia 1,\nsobre o mmBERT-small já pré-treinado", "anúncio supersoniclabs.ia.br/julia-1"),
    ("inglês", "ModernBERT original: 2 trilhões de tokens\nde texto em inglês e código", "card answerdotai/ModernBERT-base"),
    ("mmBERT", "versão multilíngue do ModernBERT,\na base do próprio Julia", "card SupersonicLabs/Julia-1"),
    ("?", "quantas conversas nossas já têm o time certo marcado,\nesse é o custo de verdade", "não medido"),
]
for i, (big, text, source) in enumerate(facts):
    y = 0.73 - i * 0.18
    fig.text(0.05, y, big, fontsize=17, fontweight="bold", color=RED if big == "?" else INK, va="center")
    fig.text(0.22, y + 0.012, text, fontsize=10.2, va="center", linespacing=1.3)
    fig.text(0.72, y, source, fontsize=8.8, color="#999", va="center")
footer(fig, "classificador treinado com times fixos tira a dependência da redação do rótulo, "
            "mas cada time novo vira dado novo e retreino")
save(fig, os.path.join(THREAD, "4-treino.png"))

# 5) proposta: margem de erro por tamanho de amostra
fig = plt.figure(figsize=(10, 5.0))
header(fig, "Com 300 msgs rotuladas, a margem cai de ±13 para ±6 pontos",
       "margem de erro aproximada (95%) de uma taxa de acerto perto de 50%, por tamanho de amostra")
ax = fig.add_axes([0.08, 0.2, 0.62, 0.56])
ns = list(range(20, 801, 5))
margin = [1.96 * math.sqrt(0.25 / n) * 100 for n in ns]
ax.plot(ns, margin, color=BLUE, lw=2)
for n, color, label in [(54, RED, "hoje"), (300, GREEN, "proposta"), (500, GREEN, "")]:
    m = 1.96 * math.sqrt(0.25 / n) * 100
    ax.scatter([n], [m], color=color, zorder=3, s=36)
    ax.text(n + 18, m + 0.8, f"n={n}: ±{m:.1f} pp".replace(".", ",") + (f"  ({label})" if label else ""),
            fontsize=9.5, color=color, fontweight="bold")
ax.set_xlim(0, 820); ax.set_ylim(0, 24)
ax.set_xlabel("mensagens rotuladas no bench", fontsize=9.5, color="#555")
ax.set_ylabel("margem de erro (pontos percentuais)", fontsize=9.5, color="#555")
ax.grid(color="#eee", lw=0.8); ax.set_axisbelow(True); ax.spines["left"].set_visible(True)
fig.text(0.75, 0.72, "comparar nas mesmas msgs", fontsize=10.5, fontweight="bold")
for i, arm in enumerate(["julia com rótulo validado", "llm pequeno classificando", "mmbert treinado no nosso dado"]):
    fig.text(0.75, 0.62 - i * 0.09, f"{i + 1}. {arm}", fontsize=10)
footer(fig, "aproximação normal, 1,96 × √(0,25/n) · com acerto longe de 50% a margem fica menor")
save(fig, os.path.join(THREAD, "5-proposta.png"))
