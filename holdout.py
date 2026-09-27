# Mensagens novas (não vistas), com as 4 redações de rótulo.
# Gabarito escrito antes de rodar.
import sys
from julia import load_model
from cases_ptbr import TEAMS
from input_ablation import TEAMS_CLEAN, SENTIMENT, SENT_CLEAN, run

HOLDOUT = [
    ("o pix que eu fiz não caiu ainda", "financeiro"),
    ("dá pra parcelar a matrícula no cartão?", "financeiro"),
    ("minha fatura veio com valor diferente do combinado", "financeiro"),
    ("preciso autenticar o diploma do ensino médio pra enviar?", "matricula"),
    ("até quando posso fazer a inscrição do vestibular?", "matricula"),
    ("mandei a foto do comprovante de residência, chegou?", "matricula"),
    ("qual a porcentagem de desconto em fisioterapia?", "bolsa"),
    ("essa bolsa vale pro curso todo ou só primeiro semestre?", "bolsa"),
    ("o código de verificação não chega no meu celular", "acesso"),
    ("minha conta foi bloqueada depois de errar a senha", "acesso"),
    ("quero desistir da vaga e receber o que paguei", "cancelamento"),
    ("como faço pra trancar e não pagar mais?", "cancelamento"),
    ("administração tem aula sábado?", "academico"),
    ("o curso de TI tem estágio obrigatório?", "academico"),
    ("quantas horas por semana de aula tem no EAD?", "academico"),
    ("o curso é reconhecido pelo MEC?", "academico"),
]
SENT_HOLDOUT = [
    ("valeu demais pela ajuda, vcs são top", "positivo"),
    ("fiquei muito feliz com o desconto", "positivo"),
    ("qual o telefone da secretaria?", "neutro"),
    ("preciso levar documento original no dia?", "neutro"),
    ("já é a terceira vez que peço e nada", "negativo"),
    ("to decepcionado, prometeram uma coisa e fizeram outra", "negativo"),
]
if __name__ == "__main__":
    import controls
    from input_ablation import SENT_DESC_EN, TEAMS_EN
    q_pt, q_en = "Qual time deve atender esta mensagem do aluno?", "Which team should handle this student message?"
    qs_pt, qs_en = "Qual o sentimento do aluno?", "What is the student's sentiment?"
    print("holdout roteamento original  ", run(HOLDOUT, q_pt, TEAMS))
    print("holdout roteamento curto pt  ", run(HOLDOUT, q_pt, controls.SHORT_PT))
    print("holdout roteamento ingles    ", run(HOLDOUT, q_en, TEAMS_EN))
    print("holdout roteamento reescrito ", run(HOLDOUT, q_pt, TEAMS_CLEAN))
    print("holdout sentimento original  ", run(SENT_HOLDOUT, qs_pt, SENTIMENT))
    print("holdout sentimento curto pt  ", run(SENT_HOLDOUT, qs_pt, controls.SENT_SHORT_PT))
    print("holdout sentimento ingles    ", run(SENT_HOLDOUT, qs_en, SENT_DESC_EN))
    print("holdout sentimento reescrito ", run(SENT_HOLDOUT, qs_pt, SENT_CLEAN))
