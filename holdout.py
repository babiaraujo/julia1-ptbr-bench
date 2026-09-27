# Mensagens novas (não vistas) para checar se os rótulos limpos generalizam.
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
    q = "Qual time deve atender esta mensagem do aluno?"
    print("holdout roteamento original ", run(HOLDOUT, q, TEAMS))
    print("holdout roteamento limpo    ", run(HOLDOUT, q, TEAMS_CLEAN))
    print("holdout sentimento original ", run(SENT_HOLDOUT, "Qual o sentimento do aluno?", SENTIMENT))
    print("holdout sentimento limpo    ", run(SENT_HOLDOUT, "Qual o sentimento do aluno?", SENT_CLEAN))
