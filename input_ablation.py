# Testa se o erro vem do que é enviado junto com a mensagem (pergunta e rótulos),
# mantendo as mensagens pt-BR fixas. Variantes:
#   A: original (descrições pt, "matricula" e "academico" ambos citam "curso")
#   B: mensagem pt + pergunta e descrições em inglês
#   C: descrições pt reescritas sem palavra em comum entre times
#   D: sem pergunta (instructions vazio), descrições pt originais
# Atenção: C foi escrita depois de ver os erros, então tem viés a favor.
import sys
from collections import Counter

from julia import load_model

from cases_ptbr import ROUTING, SENTIMENT, SENTIMENT_CASES, TEAMS

# Cópia dos rótulos em inglês de controls.py (importar lá rodaria o script inteiro)
TEAMS_EN = {
    "financeiro": "Payments, bank slips, charges, monthly fees, Pix or card",
    "matricula": "Enrollment, document submission, entrance exam and course application",
    "bolsa": "Scholarship value, discounts, course price and offer comparison",
    "acesso": "Login, password, access to the student portal or app",
    "cancelamento": "Dropping out, scholarship cancellation or refund request",
    "academico": "Course questions: curriculum, duration, modality, diploma and classes",
}
SENT_DESC_EN = {"positivo": "Satisfied, excited or grateful",
                "neutro": "Question or information, no clear emotion",
                "negativo": "Dissatisfied, angry, frustrated or worried"}

engine = load_model(sys.argv[1], device="cpu", strict_encoding=True,
                    max_length=1024, head_length=512)

TEAMS_CLEAN = {
    "financeiro": "Pagamento, boleto, cobrança, Pix ou cartão",
    "matricula": "Envio de documentos, vestibular e prazo de inscrição",
    "bolsa": "Valor da bolsa, desconto e preço",
    "acesso": "Login, senha, portal ou aplicativo com erro",
    "cancelamento": "Desistir, cancelar ou pedir reembolso",
    "academico": "Grade, duração, modalidade EAD ou presencial, diploma e turno",
}
SENT_CLEAN = {
    "positivo": "Elogio, agradecimento ou alegria",
    "neutro": "Pergunta objetiva, sem elogio nem reclamação",
    "negativo": "Reclamação, raiva, ironia ou frustração",
}


def run(cases, instructions, criteria):
    hits, preds = 0, Counter()
    for message, gold in cases:
        answer = engine.predict(state=message, questions={"q": {
            "type": "choice", "instructions": instructions, "criteria": criteria}})
        pred = answer["answers"]["q"]["choice"]
        hits += pred == gold
        preds[pred] += 1
    return f"{hits}/{len(cases)}  previsões={dict(preds.most_common(3))}"


if __name__ == "__main__":
    routing = [(m, g) for m, g, _ in ROUTING]
    q_pt = "Qual time deve atender esta mensagem do aluno?"
    q_en = "Which team should handle this student message?"
    print("roteamento A original       ", run(routing, q_pt, TEAMS))
    print("roteamento B rótulos en     ", run(routing, q_en, TEAMS_EN))
    print("roteamento C rótulos limpos ", run(routing, q_pt, TEAMS_CLEAN))
    print("roteamento D sem pergunta   ", run(routing, "", TEAMS))

    q_s_pt, q_s_en = "Qual o sentimento do aluno?", "What is the student's sentiment?"
    print("sentimento A original       ", run(SENTIMENT_CASES, q_s_pt, SENTIMENT))
    print("sentimento B rótulos en     ", run(SENTIMENT_CASES, q_s_en, SENT_DESC_EN))
    print("sentimento C rótulos limpos ", run(SENTIMENT_CASES, q_s_pt, SENT_CLEAN))
