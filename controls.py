# Controles: separa efeito do idioma e do formato das opções.
# Mesmos casos de roteamento e sentimento, em 4 variantes:
# pt descrição longa, pt rótulo curto, en descrição longa, en rótulo curto.
import sys

from julia import load_model

from cases_ptbr import ROUTING, SENTIMENT_CASES, TEAMS, SENTIMENT

ROUTING_EN = [
    "I paid the bank slip yesterday and it still shows as pending",
    "I was charged twice on my card this month",
    "what is the Pix key to pay the first monthly fee?",
    "the October bank slip did not arrive in my email",
    "which documents do I need to send to enroll?",
    "I already sent my ID and transcript, is anything missing?",
    "when is the entrance exam for business administration?",
    "how much is the nursing monthly fee with the scholarship?",
    "is there a bigger discount for evening psychology?",
    "I saw it's cheaper at another college, can you match it?",
    "I forgot my student portal password",
    "the app won't open, it just keeps loading",
    "I can't log in to the platform, it says invalid user",
    "I want to cancel my scholarship",
    "I gave up on the course, how do I get my money back?",
    "is the law degree in person or online?",
    "how many years does the civil engineering degree take?",
    "is the online diploma worth the same as the in-person one?",
    "dude the payment thing keeps failing on my card",
    "can't log in and the slip is due tomorrow, I need a new copy",
    "I don't want to cancel, I just want to know if I can switch to evening classes",
    "my mom lost her job, I won't be able to keep paying",
    "if I send the documents today can I still get the 60% scholarship?",
    "thinking about quitting because it's expensive, can you lower the price?",
]
TEAMS_EN = {
    "financeiro": "Payments, bank slips, charges, monthly fees, Pix or card",
    "matricula": "Enrollment, document submission, entrance exam and course application",
    "bolsa": "Scholarship value, discounts, course price and offer comparison",
    "acesso": "Login, password, access to the student portal or app",
    "cancelamento": "Dropping out, scholarship cancellation or refund request",
    "academico": "Course questions: curriculum, duration, modality, diploma and classes",
}
SHORT_PT = {"financeiro": "Financeiro", "matricula": "Matrícula", "bolsa": "Bolsa e desconto",
            "acesso": "Acesso e login", "cancelamento": "Cancelamento", "academico": "Dúvida sobre o curso"}
SHORT_EN = {"financeiro": "Billing", "matricula": "Enrollment", "bolsa": "Scholarship and discount",
            "acesso": "Account access", "cancelamento": "Cancellation", "academico": "Course information"}

SENT_EN = [
    "thank you so much, I got my scholarship!!",
    "loved the service, I recommend it",
    "what is the address of the downtown campus?",
    "what day do classes start?",
    "I'm really upset, nobody solves my problem",
    "what a joke, they charged me wrong again",
    "congrats on the delay, great service 👏",
    "wasn't it actually good? I thought it would go wrong",
]
SENT_DESC_EN = {"positivo": "Satisfied, excited or grateful",
                "neutro": "Question or information, no clear emotion",
                "negativo": "Dissatisfied, angry, frustrated or worried"}
SENT_SHORT_PT = {"positivo": "Positivo", "neutro": "Neutro", "negativo": "Negativo"}
SENT_SHORT_EN = {"positivo": "Positive", "neutro": "Neutral", "negativo": "Negative"}


if __name__ == "__main__":
    engine = load_model(sys.argv[1], device="cpu", strict_encoding=True,
                        max_length=1024, head_length=512)


    def accuracy(messages, golds, instructions, criteria):
        hits = 0
        for message, gold in zip(messages, golds):
            answer = engine.predict(state=message, questions={"q": {
                "type": "choice", "instructions": instructions, "criteria": criteria}})
            hits += answer["answers"]["q"]["choice"] == gold
        return f"{hits}/{len(messages)}"


    pt_msgs = [m for m, _, _ in ROUTING]
    golds = [g for _, g, _ in ROUTING]
    q_pt, q_en = "Qual time deve atender esta mensagem do aluno?", "Which team should handle this student message?"
    print("routing pt desc ", accuracy(pt_msgs, golds, q_pt, TEAMS))
    print("routing pt short", accuracy(pt_msgs, golds, q_pt, SHORT_PT))
    print("routing en desc ", accuracy(ROUTING_EN, golds, q_en, TEAMS_EN))
    print("routing en short", accuracy(ROUTING_EN, golds, q_en, SHORT_EN))

    s_pt = [m for m, _ in SENTIMENT_CASES]
    s_gold = [g for _, g in SENTIMENT_CASES]
    print("sentiment pt desc ", accuracy(s_pt, s_gold, "Qual o sentimento do aluno?", SENTIMENT))
    print("sentiment pt short", accuracy(s_pt, s_gold, "Qual o sentimento do aluno?", SENT_SHORT_PT))
    print("sentiment en desc ", accuracy(SENT_EN, s_gold, "What is the student's sentiment?", SENT_DESC_EN))
    print("sentiment en short", accuracy(SENT_EN, s_gold, "What is the student's sentiment?", SENT_SHORT_EN))
