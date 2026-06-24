"""
Base de conhecimento fictício da Clínica Vida+.

Cada entrada é um documento que será dividido em chunks e indexado no Qdrant.
A estrutura é: título + conteúdo detalhado.
"""

# Cada item da lista é um documento independente.
# Documentos mais longos são divididos automaticamente no ingest.

KNOWLEDGE_DOCUMENTS = [

    # Informações Gerais ─────────────────────────────────────────────────────
    {
        "title": "Sobre a Clínica Vida+",
        "category": "geral",
        "content": """
A Clínica Vida+ é uma clínica médica multidisciplinar localizada em São Paulo, SP.
Fundada em 2010, atendemos mais de 50.000 pacientes por ano com foco em saúde preventiva e qualidade de vida.

Endereço: Rua das Flores, 1200 - Jardim Paulista, São Paulo - SP, CEP 01404-000
Telefone: (11) 3456-7890
WhatsApp: (11) 99876-5432
E-mail: contato@clinicavidamais.com.br
Site: www.clinicavidamais.com.br

Horário de funcionamento:
- Segunda a sexta: 07h00 às 20h00
- Sábado: 08h00 às 14h00
- Domingo e feriados: fechado

Estacionamento próprio com as 2 primeiras horas gratuitas para pacientes.
Acessibilidade: rampa de acesso, elevador e banheiros adaptados.
        """,
    },

    # Especialidades ─────────────────────────────────────────────────────────
    {
        "title": "Especialidades médicas disponíveis",
        "category": "especialidades",
        "content": """
A Clínica Vida+ oferece as seguintes especialidades médicas:

CARDIOLOGIA
- Dr. Ricardo Almeida (CRM 45.678)
- Dra. Patrícia Souza (CRM 52.341)
- Consultas: segunda, quarta e sexta
- Exames: eletrocardiograma, teste ergométrico, ecocardiograma

ORTOPEDIA
- Dr. Fernando Lima (CRM 38.902)
- Consultas: terça e quinta
- Especialidade: coluna vertebral, joelho e ombro

DERMATOLOGIA
- Dra. Ana Beatriz Costa (CRM 61.203)
- Consultas: segunda a sexta
- Procedimentos: biópsia, remoção de lesões, tratamento de acne

GINECOLOGIA E OBSTETRÍCIA
- Dra. Mariana Ferreira (CRM 44.567)
- Dra. Juliana Mendes (CRM 58.901)
- Consultas: segunda a sexta
- Pré-natal, papanicolau, ultrassonografia

PEDIATRIA
- Dr. Carlos Eduardo Nunes (CRM 33.456)
- Dra. Renata Oliveira (CRM 47.890)
- Consultas: segunda a sábado
- Atendimento de 0 a 14 anos

CLÍNICA GERAL / MEDICINA DE FAMÍLIA
- Dr. Marcos Rodrigues (CRM 29.012)
- Dra. Fernanda Castro (CRM 55.678)
- Consultas: todos os dias úteis
- Atestados, receitas, check-up geral

NEUROLOGIA
- Dr. Paulo Henrique Matos (CRM 41.234)
- Consultas: segunda e quinta
- Especialidade: cefaleia, epilepsia, distúrbios do sono

PSIQUIATRIA
- Dra. Camila Azevedo (CRM 63.456)
- Consultas: terça e sexta
- Atendimento adulto e adolescente

NUTRIÇÃO
- Nutricionista: Beatriz Santos (CRN 12.345)
- Consultas: segunda a quinta
- Planos alimentares, emagrecimento, doenças crônicas

FISIOTERAPIA
- Fis. Lucas Martins (CREFITO 54.321)
- Fis. Amanda Torres (CREFITO 67.890)
- Segunda a sábado
- RPG, pilates clínico, reabilitação pós-cirúrgica
        """,
    },

    # Agendamento ───────────────────────────────────────────────────────────
    {
        "title": "Como agendar consultas e exames",
        "category": "agendamento",
        "content": """
COMO AGENDAR NA CLÍNICA VIDA+

Canais de agendamento:
1. WhatsApp: (11) 99876-5432 (este canal)
2. Telefone: (11) 3456-7890
3. Site: www.clinicavidamais.com.br/agendamento
4. Presencialmente na recepção

Para agendar, informe:
- Nome completo do paciente
- Data de nascimento
- Especialidade desejada ou nome do médico
- Preferência de data e horário
- Convênio (se houver) ou informar que é particular

Prazo para agendamento:
- Consultas de rotina: disponibilidade em até 3 dias úteis
- Retornos: prioridade na agenda, em até 2 dias úteis
- Urgências: avaliação no mesmo dia (sujeito à disponibilidade)

Confirmação:
- Você receberá confirmação por WhatsApp 24h antes da consulta
- Responda SIM para confirmar ou NÃO para cancelar/remarcar

Cancelamento e remarcação:
- Cancele com pelo menos 24h de antecedência
- Cancelamentos tardios podem gerar taxa de 30% do valor da consulta
- Para remarcar, entre em contato pelo WhatsApp ou telefone

Documentos necessários:
- RG ou CPF
- Carteira do convênio (se houver)
- Pedido médico (para exames)
- Exames anteriores relacionados (se houver)
        """,
    },

    # Convênios ─────────────────────────────────────────────────────────────
    {
        "title": "Convênios aceitos",
        "category": "convenios",
        "content": """
CONVÊNIOS ACEITOS NA CLÍNICA VIDA+

Planos de saúde aceitos:
- Unimed (todas as modalidades)
- Bradesco Saúde
- SulAmérica Saúde
- Amil
- Porto Seguro Saúde
- NotreDame Intermédica
- Hapvida
- São Francisco Saúde
- Prevent Senior
- Golden Cross
- Cassi (Banco do Brasil)
- Geap (Servidores Federais)

IMPORTANTE:
- Verifique com seu plano se a Clínica Vida+ está na rede credenciada
- Alguns procedimentos podem requerer autorização prévia do convênio
- Exames de imagem de alta complexidade podem não estar cobertos por todos os planos
- Para conferir a cobertura do seu plano para uma especialidade específica,
  ligue para o número no verso do cartão do convênio

Atendimento particular:
- Aceitamos todos os pacientes, com ou sem convênio
- Formas de pagamento: dinheiro, cartão de débito, crédito (até 3x sem juros) e Pix
- Consulta particular: a partir de R$ 180,00 (valor varia por especialidade)
- Pacote de retorno: 50% de desconto na consulta de retorno em até 30 dias

Nota fiscal:
- Emitimos nota fiscal para todos os atendimentos
- Para pacientes que declaram IR, guarde os recibos para dedução
        """,
    },

    # Exames ────────────────────────────────────────────────────────────────
    {
        "title": "Exames laboratoriais e de imagem",
        "category": "exames",
        "content": """
EXAMES DISPONÍVEIS NA CLÍNICA VIDA+

LABORATÓRIO (coleta no local)
Horário de coleta: segunda a sexta, 07h00 às 17h00 / sábado, 07h00 às 11h00

Exames de sangue:
- Hemograma completo
- Glicemia de jejum e hemoglobina glicada
- Colesterol total e frações (HDL, LDL, VLDL)
- Triglicerídeos
- TSH, T3, T4 livre (tireoide)
- PSA (próstata)
- Vitamina D e B12
- Ferritina e ferro sérico
- Função renal (ureia, creatinina)
- Função hepática (TGO, TGP, GGT)
- PCR (proteína C reativa)
- Coagulograma

Preparo para exames de sangue:
- Jejum de 8 a 12 horas (água pode ser ingerida)
- Evitar atividade física intensa no dia anterior
- Informar medicamentos em uso

IMAGEM
- Ultrassonografia abdominal, pélvica e obstétrica
- Eletrocardiograma (ECG)
- Ecocardiograma
- Raio-X (convênio com clínica parceira, no mesmo endereço)
- Densitometria óssea

Resultados:
- Exames de sangue simples: 24 a 48h
- Exames complexos: 3 a 5 dias úteis
- Retirada: presencialmente ou pelo portal do paciente (www.clinicavidamais.com.br/resultados)
- Senha de acesso enviada por e-mail ou WhatsApp no ato da coleta
        """,
    },

    # Perguntas Frequentes ───────────────────────────────────────────────────
    {
        "title": "Perguntas frequentes dos pacientes",
        "category": "faq",
        "content": """
PERGUNTAS FREQUENTES — CLÍNICA VIDA+

P: Preciso de encaminhamento para consultar com especialista?
R: Não. Na Clínica Vida+, você pode agendar diretamente com qualquer especialista sem precisar de encaminhamento. Porém, alguns convênios exigem autorização prévia — verifique com seu plano.

P: Quanto tempo dura uma consulta?
R: Consultas de primeira vez duram em média 40 minutos. Retornos duram cerca de 20 minutos.

P: Posso levar acompanhante?
R: Sim. Crianças e idosos podem ter um acompanhante. Para pacientes adultos, o médico pode solicitar a saída do acompanhante em algum momento da consulta por questões de privacidade.

P: A clínica atende emergências?
R: Não somos pronto-socorro. Para emergências, procure o pronto-atendimento mais próximo ou ligue para o SAMU (192). Porém, atendemos urgências não emergenciais no mesmo dia, sujeito à disponibilidade.

P: Como funciona a consulta de retorno?
R: O retorno é a consulta de acompanhamento com o mesmo médico. Tem desconto de 50% se realizado em até 30 dias da consulta anterior.

P: Posso solicitar segunda opinião?
R: Sim. Você pode agendar com outro médico da mesma especialidade. Recomendamos trazer os laudos e exames anteriores.

P: A clínica emite atestado médico?
R: Sim. Atestados são emitidos pelos médicos quando clinicamente justificado. Atestados "a pedido" sem justificativa médica não são emitidos por questões éticas.

P: Como funciona o teleatendimento?
R: Oferecemos teleconsulta para retornos e algumas especialidades (nutrição, psiquiatria, clínica geral). Agendamento pelo mesmo canal. A consulta é feita por videochamada segura.

P: Posso pagar com dois cartões?
R: Sim, aceitamos pagamento em dois cartões desde que solicitado no caixa antes de iniciar o pagamento.

P: A clínica tem estacionamento?
R: Sim. Temos estacionamento próprio com as 2 primeiras horas gratuitas para pacientes. Após 2 horas, R$ 5,00 por hora adicional. Apresente o ticket na recepção para validar.
        """,
    },

    # Orientações pré-consulta ───────────────────────────────────────────────
    {
        "title": "Orientações antes da consulta",
        "category": "orientacoes",
        "content": """
ORIENTAÇÕES PARA ANTES DA SUA CONSULTA

Chegue com 15 minutos de antecedência para:
- Preencher ou atualizar o cadastro
- Apresentar documentos e carteirinha do convênio
- Realizar o pré-atendimento de enfermagem (aferição de pressão, peso, etc.)

Documentos obrigatórios:
- Documento de identidade com foto (RG ou CNH)
- CPF
- Carteirinha do plano de saúde (se houver)
- Pedido médico (obrigatório para exames)

O que trazer:
- Lista de medicamentos que usa atualmente (nome e dosagem)
- Exames anteriores relacionados ao motivo da consulta
- Relatórios ou laudos de outros médicos
- Anotar os sintomas, quando começaram e como evoluíram

Para consultas de nutrição:
- Trazer recordatório alimentar de 3 dias (o que comeu nos últimos 3 dias)
- Exames laboratoriais recentes (se houver)

Para consultas de cardiologia:
- ECGs anteriores, se houver
- Monitoramentos de pressão (se fizer em casa)
- Lista completa de medicamentos cardiovasculares

Para pediatria:
- Carteira de vacinação
- Curva de crescimento (se tiver)
- Relatar infecções ou doenças recentes da criança

POLÍTICA DE TOLERÂNCIA DE ATRASO:
Pacientes que chegarem com mais de 15 minutos de atraso podem ter o atendimento reagendado, dependendo da disponibilidade da agenda do médico. Recomendamos ligar previamente caso vá se atrasar.
        """,
    },

    # Programas e Serviços Especiais ─────────────────────────────────────────
    {
        "title": "Programas especiais e serviços diferenciados",
        "category": "programas",
        "content": """
PROGRAMAS ESPECIAIS DA CLÍNICA VIDA+

CHECK-UP VIDA+
Pacote completo de avaliação de saúde preventiva.
Inclui: consulta com clínico geral, hemograma completo, glicemia, colesterol,
função renal e hepática, TSH, ECG, pressão arterial, IMC e orientações.
Valor: R$ 490,00 (particular) | Duração: 1 dia (manhã)
Resultado: entregue em 5 dias com relatório médico detalhado

PROGRAMA GESTANTE VIDA+
Acompanhamento completo do pré-natal.
Inclui: consultas mensais com obstetra, ultrassonografias, exames laboratoriais
do pré-natal e suporte por WhatsApp com a equipe de obstetrícia.
Planos a partir de R$ 1.200,00 (particular)

PROGRAMA CRIANÇA SAUDÁVEL
Acompanhamento pediátrico do 0 ao 12 anos.
Inclui: consultas de puericultura nos marcos de desenvolvimento,
orientações de vacinação e nutrição infantil.
Desconto de 20% nas consultas para membros do programa.

TELECONSULTA
Disponível para: nutrição, psiquiatria, clínica geral e retornos de outras especialidades.
Funciona por videochamada segura.
Agendamento pelo WhatsApp ou site.
Valor: mesmo da consulta presencial.

VACINAS
Aplicamos vacinas para adultos e crianças (conforme prescrição médica).
Disponíveis: influenza, HPV, hepatite A e B, febre amarela, tétano,
pneumocócica, varicela, meningocócica, entre outras.
Consulte disponibilidade e valores pelo WhatsApp.

SAÚDE OCUPACIONAL
Exames admissionais, periódicos e demissionais para empresas.
ASO (Atestado de Saúde Ocupacional) emitido no mesmo dia.
Para empresas: entre em contato para tabela especial.
        """,
    },
]


def get_all_documents() -> list[dict]:
    """Retorna todos os documentos da base de conhecimento."""
    return KNOWLEDGE_DOCUMENTS


def get_documents_by_category(category: str) -> list[dict]:
    """Retorna documentos de uma categoria específica."""
    return [doc for doc in KNOWLEDGE_DOCUMENTS if doc["category"] == category]


def get_full_text(doc: dict) -> str:
    """Retorna o texto completo de um documento (título + conteúdo)."""
    return f"{doc['title']}\n\n{doc['content'].strip()}"