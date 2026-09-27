# Renderiza os logs de assets/terminal/*.log como PNG com cara de janela de terminal.
# O conteúdo é o log real, só convertido de ANSI para HTML e fotografado pelo Chrome headless.
# Uso: python render_terminal.py
import html
import os
import re
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TERMINAL = os.path.join(HERE, "assets", "terminal")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ANSI = re.compile(r"\x1b\[([0-9;]*)m")
COLORS = {"31": "#ff6b6b", "32": "#5fd38d", "33": "#f2c14e", "34": "#6ea8fe", "36": "#56c8d8"}

# Recortes: (arquivo, título da janela, filtro de linhas). None = log inteiro.
SHOTS = [
    ("01-ambiente", "ambiente e hash dos pesos", None),
    ("02-casos-ptbr", "run_ptbr.py: roteamento caso a caso",
     lambda lines: lines[:25] + ["\x1b[2m  ... (urgência, sim/não e sentimento omitidos, estão no log completo) ...\x1b[0m"] + lines[-9:]),
    ("03-variacao-rotulos", "input_ablation.py: mesmas msgs, rótulos diferentes", None),
    ("04-msgs-novas", "holdout.py: msgs novas, 4 redações de rótulo", None),
    ("05-reproducao-oficial", "reproduce_typed.py: teste oficial do modelo",
     lambda lines: [l for l in lines if l.strip() != '"by_type": {']),
]


def to_html(line):
    out, open_spans, pos = [], 0, 0
    for match in ANSI.finditer(line):
        out.append(html.escape(line[pos:match.start()]))
        pos = match.end()
        codes = match.group(1).split(";") if match.group(1) else ["0"]
        if codes == ["0"]:
            out.append("</span>" * open_spans); open_spans = 0
            continue
        style = []
        for code in codes:
            if code == "1": style.append("font-weight:700")
            elif code == "2": style.append("color:#7d8590")
            elif code in COLORS: style.append(f"color:{COLORS[code]}")
        out.append(f'<span style="{";".join(style)}">'); open_spans += 1
    out.append(html.escape(line[pos:]))
    out.append("</span>" * open_spans)
    return "".join(out)


def wrap(line, width=140):
    # quebra linhas longas (sem perder conteúdo); linhas com cor são curtas e passam inteiras
    plain = ANSI.sub("", line)
    if len(plain) <= width:
        return [line]
    return [plain[i:i + width] if i == 0 else "  " + plain[i:i + width] for i in range(0, len(plain), width)]


def render(name, title, pick):
    with open(os.path.join(TERMINAL, f"{name}.log"), encoding="utf-8") as handle:
        lines = handle.read().rstrip("\n").split("\n")
    lines = pick(lines) if pick else lines
    lines = [part for line in lines for part in wrap(line)]
    body = "\n".join(to_html(line) for line in lines)
    height = 70 + 19 * len(lines) + 30
    page = f"""<!doctype html><meta charset="utf-8"><style>
body{{margin:0;background:#e9ebee;padding:24px;}}
.win{{background:#0d1117;border-radius:9px;box-shadow:0 8px 24px rgba(0,0,0,.18);width:1180px;overflow:hidden}}
.bar{{background:#1f242c;height:34px;display:flex;align-items:center;padding:0 14px;gap:8px}}
.dot{{width:12px;height:12px;border-radius:50%}}
.t{{color:#9da7b3;font:13px -apple-system,Helvetica,Arial;margin-left:14px}}
pre{{margin:0;padding:16px 18px 20px;color:#e6edf3;font:13px/19px Menlo,'SF Mono',monospace;white-space:pre}}
</style><div class="win"><div class="bar"><span class="dot" style="background:#ff5f57"></span>
<span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span>
<span class="t">julia1-ptbr-bench · {html.escape(title)}</span></div><pre>{body}</pre></div>"""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(page)
    out = os.path.join(TERMINAL, f"{name}.png")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", f"--window-size=1228,{height + 48}",
                    f"--screenshot={out}", f"file://{tmp.name}"],
                   check=True, capture_output=True)
    os.unlink(tmp.name)
    print(out)


for shot in SHOTS:
    render(*shot)
