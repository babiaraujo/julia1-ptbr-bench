# Roda o Julia 1 nos casos pt-BR e grava resultados em results_ptbr.json.
# Uso: python run_ptbr.py /caminho/para/Julia-1
import json
import statistics
import sys
import time

from julia import load_model

from cases_ptbr import (ROUTING, SENTIMENT, SENTIMENT_CASES, TEAMS, URGENCY,
                        URGENCY_LEVELS, YES_NO)

engine = load_model(sys.argv[1], device="cpu", strict_encoding=True,
                    max_length=1024, head_length=512)
latencies = []


def ask(state, question):
    start = time.perf_counter()
    answer = engine.predict(state=state, questions={"q": question})["answers"]["q"]
    latencies.append((time.perf_counter() - start) * 1000)
    return answer


def argmax(probabilities):
    return max(probabilities, key=probabilities.get)


def show(task, message, gold, pred, conf):
    mark = "\033[32mOK \033[0m" if pred == gold else "\033[31mERR\033[0m"
    print(f"{mark} {task:<10} {conf:5.2f}  esperado={gold!s:<12} modelo={pred!s:<12} {message}", flush=True)


report = {}

# 1) Roteamento em 6 times, na ordem original e com as opções invertidas
routing_rows = []
reversed_teams = dict(reversed(list(TEAMS.items())))
for message, gold, level in ROUTING:
    question = "Qual time deve atender esta mensagem do aluno?"
    forward = ask(message, {"type": "choice", "instructions": question, "criteria": TEAMS})
    backward = ask(message, {"type": "choice", "instructions": question, "criteria": reversed_teams})
    routing_rows.append(dict(message=message, gold=gold, level=level,
                             pred=forward["choice"], conf=round(forward["max_probability"], 3),
                             pred_reversed=backward["choice"]))
    show("roteamento", message, gold, forward["choice"], forward["max_probability"])
report["routing"] = routing_rows

# 2) Urgência em escala ordenada
urgency_rows = []
for message, gold in URGENCY:
    answer = ask(message, {"type": "score", "instructions": "Qual a urgência desta mensagem?",
                           "criteria": URGENCY_LEVELS})
    urgency_rows.append(dict(message=message, gold=gold,
                             pred=int(argmax(answer["probabilities"])),
                             expected=round(answer["score"], 2)))
    show("urgência", message, gold, urgency_rows[-1]["pred"], answer["max_probability"])
report["urgency"] = urgency_rows

# 3) Sim ou não, com rótulo literal e com descrição em português
yes_no_rows = []
for message, question, gold in YES_NO:
    literal = ask(message, {"type": "noul", "instructions": question})
    described = ask(message, {"type": "noul", "instructions": question,
                              "criteria": {"false": "Não", "true": "Sim"}})
    yes_no_rows.append(dict(message=message, question=question, gold=gold,
                            p_true_literal=round(literal["noul"], 3),
                            p_true_ptbr=round(described["noul"], 3)))
    show("sim/não", f"{message}  [{question}]", gold, described["noul"] > 0.5, described["noul"])
report["yes_no"] = yes_no_rows

# 4) Sentimento
sentiment_rows = []
for message, gold in SENTIMENT_CASES:
    answer = ask(message, {"type": "choice", "instructions": "Qual o sentimento do aluno?",
                           "criteria": SENTIMENT})
    sentiment_rows.append(dict(message=message, gold=gold, pred=answer["choice"],
                               conf=round(answer["max_probability"], 3)))
    show("sentimento", message, gold, answer["choice"], answer["max_probability"])
report["sentiment"] = sentiment_rows

report["latency_ms"] = dict(n=len(latencies), median=round(statistics.median(latencies), 1),
                            p95=round(sorted(latencies)[int(0.95 * len(latencies)) - 1], 1))

with open("results_ptbr.json", "w") as handle:
    json.dump(report, handle, ensure_ascii=False, indent=1)


def score(rows, ok):
    hits = sum(ok(row) for row in rows)
    return f"{hits}/{len(rows)}"


print("routing        ", score(routing_rows, lambda r: r["pred"] == r["gold"]))
print("routing easy   ", score([r for r in routing_rows if r["level"] == "easy"], lambda r: r["pred"] == r["gold"]))
print("routing med+hrd", score([r for r in routing_rows if r["level"] != "easy"], lambda r: r["pred"] == r["gold"]))
print("routing stable ", score(routing_rows, lambda r: r["pred"] == r["pred_reversed"]))
print("urgency        ", score(urgency_rows, lambda r: r["pred"] == r["gold"]))
print("yes/no literal ", score(yes_no_rows, lambda r: (r["p_true_literal"] > 0.5) == r["gold"]))
print("yes/no Sim/Não ", score(yes_no_rows, lambda r: (r["p_true_ptbr"] > 0.5) == r["gold"]))
print("sentiment      ", score(sentiment_rows, lambda r: r["pred"] == r["gold"]))
print("latency        ", report["latency_ms"])
