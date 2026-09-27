# Gera o PNG com os resultados do teste do Julia 1 em pt-BR.
import os

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
RED, GRAY, GREEN, INK = "#d1495b", "#b8b8b8", "#2e8b70", "#2b2b2b"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "julia1-ptbr-resultados.png")

fig = plt.figure(figsize=(12, 6.4))
gs = fig.add_gridspec(3, 3, height_ratios=[0.2, 0.24, 1], hspace=0.55, wspace=0.35,
                      left=0.05, right=0.97, top=0.94, bottom=0.1)

axt = fig.add_subplot(gs[0, :]); axt.axis("off")
axt.text(0, 0.95, "Julia 1 em pt-BR: no roteamento, o rótulo decide mais que o modelo",
         fontsize=16, fontweight="bold", va="top")
axt.text(0, 0.1, "SupersonicLabs/Julia-1 no Hugging Face · CPU local · mensagens de aluno escritas à mão · 27/09/2026",
         fontsize=9.5, color="#777", va="top")

axk = fig.add_subplot(gs[1, :]); axk.axis("off")
kpis = [("3 → 12", "acertos em 16 msgs novas\nsó reescrevendo o rótulo", GREEN),
        ("13 de 16", "foram pra matrícula\ncom o rótulo original", RED),
        ("≤ 3 de 8", "no sentimento\ncom qualquer rótulo", RED),
        ("18 ms", "mediana por decisão\nna CPU", INK)]
for i, (value, label, color) in enumerate(kpis):
    axk.text(i * 0.255, 1.0, value, fontsize=21, fontweight="bold", color=color, va="top")
    axk.text(i * 0.255, 0.28, label, fontsize=8.8, color="#777", va="top")


def paired(ax, title, groups, original, rewritten, totals):
    x = range(len(groups)); w = 0.36
    for offset, values, color, name in ((-w / 2, original, GRAY, "rótulo original"),
                                        (w / 2, rewritten, GREEN, "rótulo reescrito")):
        pct = [v / t * 100 for v, t in zip(values, totals)]
        bars = ax.bar([i + offset for i in x], pct, w, color=color, label=name)
        for bar, v, t in zip(bars, values, totals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2, f"{v}/{t}",
                    ha="center", fontsize=9.5, fontweight="bold", color=INK)
    ax.set_xticks(list(x), groups, fontsize=9.5)
    ax.set_ylim(0, 105); ax.set_yticks([0, 50, 100], ["0%", "50%", "100%"], fontsize=8.5)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="y", color="#eee", lw=0.8); ax.set_axisbelow(True)
    ax.set_title(title, fontsize=11.5, fontweight="bold", pad=12, loc="left")


ax1 = fig.add_subplot(gs[2, 0])
paired(ax1, "Roteamento em 6 times", ["msgs do 1º teste", "msgs novas"], [12, 3], [20, 12], [24, 16])
ax1.legend(frameon=False, fontsize=8.5, loc="upper left", bbox_to_anchor=(0, 1.02), ncol=1)

ax2 = fig.add_subplot(gs[2, 1])
paired(ax2, "Sentimento (3 classes)", ["msgs do 1º teste", "msgs novas"], [2, 3], [3, 2], [8, 6])

ax3 = fig.add_subplot(gs[2, 2]); ax3.axis("off")
ax3.set_title("Teste oficial deles bateu exato", fontsize=11.5, fontweight="bold", pad=12, loc="left")
rows = [("", "rodei aqui", "README"), ("choice", "426/600", "426/600"),
        ("score", "542/800", "542/800"), ("sim/não", "483/600", "483/600")]
for r, (a, b, c) in enumerate(rows):
    y = 0.88 - r * 0.2
    weight = "bold" if r == 0 else "normal"
    color = "#888" if r == 0 else INK
    ax3.text(0.0, y, a, fontsize=10.5, color="#555", va="center", transform=ax3.transAxes)
    ax3.text(0.36, y, b, fontsize=10.5, fontweight=weight, color=color, va="center", transform=ax3.transAxes)
    ax3.text(0.7, y, c, fontsize=10.5, fontweight=weight, color=color, va="center", transform=ax3.transAxes)
    if r == 0:
        ax3.plot([0, 1], [y - 0.1, y - 0.1], color="#ddd", lw=0.8, transform=ax3.transAxes)
ax3.text(0.0, 0.02, "instalação correta, os erros são do modelo", fontsize=9, color="#777", transform=ax3.transAxes)

fig.text(0.05, 0.015,
         "Metodologia: gabarito escrito antes de rodar · msgs novas escritas depois da troca de rótulo · "
         "amostra pequena (n=54), leitura indicativa · strict encoding, 1.024 tokens, PyTorch 2.14 FP32",
         fontsize=7.6, color="#999")
fig.savefig(OUT, dpi=200, bbox_inches="tight", facecolor="white")
print(OUT)
