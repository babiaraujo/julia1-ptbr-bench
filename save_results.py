# Consolida todos os resultados do teste do Julia 1 em julia1_ptbr_results.json.
# Uso: python save_results.py .julia/Julia-1
import glob
import json
import os
from datetime import datetime, timezone

import controls
import holdout
import input_ablation as ab
from cases_ptbr import ROUTING, SENTIMENT, SENTIMENT_CASES, TEAMS

engine = ab.engine  # modelo já carregado pelo input_ablation


def evaluate(cases, instructions, criteria):
    rows = []
    for message, gold in cases:
        answer = engine.predict(state=message, questions={"q": {
            "type": "choice", "instructions": instructions, "criteria": criteria}})["answers"]["q"]
        rows.append(dict(message=message, gold=gold, pred=answer["choice"],
                         confidence=round(answer["max_probability"], 4)))
    correct = sum(r["pred"] == r["gold"] for r in rows)
    return dict(correct=correct, total=len(rows), accuracy=round(correct / len(rows), 4), cases=rows)


routing = [(m, g) for m, g, _ in ROUTING]
routing_en = list(zip(controls.ROUTING_EN, [g for _, g in routing]))
sentiment_en = list(zip(controls.SENT_EN, [g for _, g in SENTIMENT_CASES]))
q_pt, q_en = "Qual time deve atender esta mensagem do aluno?", "Which team should handle this student message?"
qs_pt, qs_en = "Qual o sentimento do aluno?", "What is the student's sentiment?"

label_variants = {
    "routing": {
        "original_pt": evaluate(routing, q_pt, TEAMS),
        "short_pt": evaluate(routing, q_pt, controls.SHORT_PT),
        "labels_en_msg_pt": evaluate(routing, q_en, ab.TEAMS_EN),
        "clean_pt": evaluate(routing, q_pt, ab.TEAMS_CLEAN),
        "no_question_pt": evaluate(routing, "", TEAMS),
        "translated_en": evaluate(routing_en, q_en, controls.TEAMS_EN),
        "translated_en_short": evaluate(routing_en, q_en, controls.SHORT_EN),
    },
    "sentiment": {
        "original_pt": evaluate(SENTIMENT_CASES, qs_pt, SENTIMENT),
        "short_pt": evaluate(SENTIMENT_CASES, qs_pt, controls.SENT_SHORT_PT),
        "labels_en_msg_pt": evaluate(SENTIMENT_CASES, qs_en, ab.SENT_DESC_EN),
        "clean_pt": evaluate(SENTIMENT_CASES, qs_pt, ab.SENT_CLEAN),
        "translated_en": evaluate(sentiment_en, qs_en, controls.SENT_DESC_EN),
        "translated_en_short": evaluate(sentiment_en, qs_en, controls.SENT_SHORT_EN),
    },
}
holdout_results = {
    "routing_original": evaluate(holdout.HOLDOUT, q_pt, TEAMS),
    "routing_short_pt": evaluate(holdout.HOLDOUT, q_pt, controls.SHORT_PT),
    "routing_question_labels_en": evaluate(holdout.HOLDOUT, q_en, ab.TEAMS_EN),
    "routing_clean": evaluate(holdout.HOLDOUT, q_pt, ab.TEAMS_CLEAN),
    "sentiment_original": evaluate(holdout.SENT_HOLDOUT, qs_pt, SENTIMENT),
    "sentiment_short_pt": evaluate(holdout.SENT_HOLDOUT, qs_pt, controls.SENT_SHORT_PT),
    "sentiment_question_labels_en": evaluate(holdout.SENT_HOLDOUT, qs_en, ab.SENT_DESC_EN),
    "sentiment_clean": evaluate(holdout.SENT_HOLDOUT, qs_pt, ab.SENT_CLEAN),
}

with open("results_ptbr.json") as handle:
    first_test = json.load(handle)
latest = max(glob.glob(".julia/typed-cpu*/results.json"), key=os.path.getmtime)
with open(latest) as handle:
    reproduction = json.load(handle)

report = {
    "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "model": "SupersonicLabs/Julia-1",
    "weights_sha256": reproduction.get("weights_sha256"),
    "runtime": dict(device="cpu", strict_encoding=True, max_length=1024, head_length=512,
                    torch=reproduction.get("torch"), transformers=reproduction.get("transformers")),
    "labels": dict(routing_original=TEAMS, routing_clean=ab.TEAMS_CLEAN,
                   sentiment_original=SENTIMENT, sentiment_clean=ab.SENT_CLEAN),
    "notes": [
        "Gabarito escrito antes de rodar.",
        "Rótulos 'clean' foram escritos depois de ver os erros; o holdout foi escrito depois, pela mesma pessoa, então é indício e não prova.",
        "Rótulos 'en' são tradução direta dos originais, escritos antes de ver erros; a pergunta também vai em inglês.",
        "Amostra pequena (54 mensagens pt-BR), leitura indicativa.",
    ],
    "first_test_ptbr": first_test,
    "label_variants": label_variants,
    "holdout": holdout_results,
    "official_reproduction": dict(
        source=latest,
        by_type=reproduction["original_criteria"]["by_type"],
        readme_cpu_fp32={"choice": "426/600", "score": "542/800", "noul": "483/600"},
    ),
}
with open("julia1_ptbr_results.json", "w") as handle:
    json.dump(report, handle, ensure_ascii=False, indent=2)

print("salvo em julia1_ptbr_results.json")
for group, variants in [("roteamento", label_variants["routing"]), ("sentimento", label_variants["sentiment"]),
                        ("holdout", holdout_results)]:
    for name, result in variants.items():
        print(f"{group:<11} {name:<20} {result['correct']}/{result['total']}")
