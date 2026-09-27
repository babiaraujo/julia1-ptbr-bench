# Casos de teste em pt-BR para o Julia 1.
# Mensagens sintéticas geradas por IA (Claude), não são mensagens reais de aluno.
# Gabarito escrito antes de rodar o modelo. Contexto: atendimento de aluno
# em marketplace de bolsas de estudo (mensagens estilo WhatsApp).

TEAMS = {
    "financeiro": "Pagamento, boleto, cobrança, mensalidade, Pix ou cartão",
    "matricula": "Matrícula, envio de documentos, vestibular e inscrição no curso",
    "bolsa": "Valor da bolsa, desconto, preço do curso e comparação de ofertas",
    "acesso": "Login, senha, acesso ao portal do aluno ou ao aplicativo",
    "cancelamento": "Desistência, cancelamento da bolsa ou pedido de reembolso",
    "academico": "Dúvidas sobre o curso: grade, duração, modalidade, diploma e aulas",
}

# (mensagem, time correto, dificuldade)
ROUTING = [
    ("paguei o boleto ontem e ainda aparece como pendente", "financeiro", "easy"),
    ("fui cobrado duas vezes no cartão esse mês", "financeiro", "easy"),
    ("qual a chave pix pra pagar a primeira mensalidade?", "financeiro", "easy"),
    ("o boleto de outubro nao chegou no meu email", "financeiro", "easy"),
    ("quais documentos eu preciso mandar pra fazer a matrícula?", "matricula", "easy"),
    ("já mandei meu RG e o histórico, falta alguma coisa?", "matricula", "easy"),
    ("quando é a prova do vestibular de administração?", "matricula", "easy"),
    ("quanto fica a mensalidade de enfermagem com a bolsa?", "bolsa", "easy"),
    ("tem desconto maior pra psicologia noturno?", "bolsa", "easy"),
    ("vi que na outra faculdade tá mais barato, vcs cobrem?", "bolsa", "medium"),
    ("esqueci minha senha do portal do aluno", "acesso", "easy"),
    ("o app não abre, fica só carregando", "acesso", "easy"),
    ("não consigo entrar na plataforma, diz usuário inválido", "acesso", "easy"),
    ("quero cancelar minha bolsa", "cancelamento", "easy"),
    ("desisti do curso, como faço pra pegar meu dinheiro de volta?", "cancelamento", "easy"),
    ("o curso de direito é presencial ou EAD?", "academico", "easy"),
    ("quantos anos dura o curso de engenharia civil?", "academico", "easy"),
    ("o diploma do EAD vale igual ao presencial?", "academico", "easy"),
    # casos mais difíceis: gíria, erro de digitação, dois assuntos, negação
    ("mano o negocio de pagar ta dando erro no cartao", "financeiro", "medium"),
    ("n consigo logar e o boleto vence amanha, preciso da 2 via", "financeiro", "hard"),
    ("não quero cancelar não, só quero saber se consigo trocar pro noturno", "academico", "hard"),
    ("minha mãe perdeu o emprego, não vou conseguir continuar pagando", "cancelamento", "hard"),
    ("se eu mandar os documentos hoje ainda pego a bolsa de 60%?", "matricula", "hard"),
    ("to pensando em desistir pq achei caro, tem como baixar o valor?", "bolsa", "hard"),
]

URGENCY_LEVELS = [
    "Baixa: dúvida geral, sem prazo",
    "Média: precisa de resposta em alguns dias",
    "Alta: prazo vencendo hoje ou amanhã, ou aluno bloqueado",
]
# (mensagem, índice correto 0=baixa 1=média 2=alta)
URGENCY = [
    ("queria saber mais sobre o curso de nutrição, sem pressa", 0),
    ("vocês têm curso de gastronomia?", 0),
    ("o que é a nota de corte do vestibular?", 0),
    ("minha matrícula fecha sexta que vem, preciso mandar os documentos", 1),
    ("gostaria de ver a grade antes de decidir, até o fim do mês", 1),
    ("recebi um email estranho sobre renovação, podem verificar essa semana?", 1),
    ("o boleto vence HOJE e o link não funciona!!!", 2),
    ("a prova é amanhã e não recebi o local", 2),
    ("fui bloqueado do portal e tenho entrega de trabalho em 2 horas", 2),
    ("urgente: cobraram 3x no meu cartão agora", 2),
]

# (mensagem, pergunta, resposta correta True/False)
YES_NO = [
    ("quero fechar a matrícula hoje, me manda o link", "O aluno quer se matricular?", True),
    ("bora, pode garantir minha vaga em administração", "O aluno quer se matricular?", True),
    ("só estou pesquisando por enquanto, obrigado", "O aluno quer se matricular?", False),
    ("achei caro, não vou fazer não", "O aluno quer se matricular?", False),
    ("o atendimento de vocês é péssimo, ninguém responde", "A mensagem é uma reclamação?", True),
    ("adorei, vocês foram super rápidos", "A mensagem é uma reclamação?", False),
    ("nossa que ótimo, esperei só três semanas pra ter resposta", "A mensagem é uma reclamação?", True),
    ("qual o horário de atendimento?", "A mensagem é uma reclamação?", False),
    ("meu nome é Ana e meu cpf é 123.456.789-00", "A mensagem contém dados pessoais?", True),
    ("quanto custa o curso de pedagogia?", "A mensagem contém dados pessoais?", False),
    ("não tenho interesse, pode tirar meu número da lista", "O aluno pediu para não ser mais contatado?", True),
    ("pode me ligar amanhã depois das 18h", "O aluno pediu para não ser mais contatado?", False),
]

SENTIMENT = {
    "positivo": "Satisfeito, animado ou agradecido",
    "neutro": "Pergunta ou informação, sem emoção clara",
    "negativo": "Insatisfeito, irritado, frustrado ou preocupado",
}
SENTIMENT_CASES = [
    ("muito obrigada, consegui minha bolsa!!", "positivo"),
    ("amei o atendimento, recomendo", "positivo"),
    ("qual o endereço do campus centro?", "neutro"),
    ("a aula começa que dia?", "neutro"),
    ("to muito chateado, ninguém resolve meu problema", "negativo"),
    ("que palhaçada, cobraram errado de novo", "negativo"),
    ("parabéns pela demora, ótimo serviço 👏", "negativo"),  # sarcasmo
    ("não é que foi bom mesmo? achei que ia dar errado", "positivo"),
]
