# Atendente WhatsApp — Clínica Vida+
 
> Atendente virtual para WhatsApp da Clínica Vida+, usando Evolution API + RAG + Claude.
> Responde perguntas sobre agendamentos, convênios, exames e especialidades de forma automática, segura e com memória de conversa.
 
---
 
## Sobre o projeto
 
Atendente automático para clínica médica via WhatsApp. O bot:
- Responde perguntas com base em uma base de conhecimento estruturada (RAG)
- Mantém memória de conversa por sessão
- Protege contra prompt injection e abuso (rate limiting)
- Integra com o WhatsApp real via Evolution API (open source)
 
---
 
## Funcionalidades
 
- Atendimento via WhatsApp com respostas em linguagem natural
- Memória de conversa por sessão (30 min de inatividade)
- RAG sobre base de conhecimento estruturada da clínica
- Rate limiting, sanitização e detecção de prompt injection
- Base de conhecimento com especialidades, convênios, exames e FAQ
- Testes unitários com cobertura de segurança e memória
 
---
 
## Stack
 
| Camada | Tecnologia |
|--------|-----------|
| WhatsApp | Evolution API v2 (Docker) |
| Webhook | FastAPI (async) |
| Memória | Dict em memória (Redis-ready) |
| Embedding | OpenAI text-embedding-3-small |
| Vector Store | Qdrant |
| LLM | Anthropic Claude Haiku |
 
---
 
## Como rodar
 
### Pré-requisitos:
- Python 3.11+
- Docker Desktop
- Chaves: OpenAI e Anthropic
- Número de WhatsApp para o bot (chip de teste recomendado)
 
### Instalação
 
```bash
git clone https://github.com/FernandaAndradedev-hash/Assistente-de-Whatsapp-com-IA
cd Assistente-de-Whatsapp-com-IA
python -m venv .venv && .venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```
 
### Subindo os serviços
 
```bash
docker-compose up -d
cd src
python ingest_knowledge.py
uvicorn api:app --reload --port 8000
```
 
### Conectando o WhatsApp
 
```bash
curl -X POST http://localhost:8080/instance/create \
  -H "apikey: SUA-CHAVE" \
  -H "Content-Type: application/json" \
  -d '{"instanceName": "clinica-vida-mais", "qrcode": true}'
```
 
---
 
## Testes
 
```bash
pytest tests/ -v
```
 
---
 
## Estrutura
 
````
Assistente-de-Whatsapp-com-IA/
├── src/
│   ├── config.py           # Configurações
│   ├── validators.py       # Segurança e rate limiting
│   ├── knowledge_base.py   # Base de conhecimento da clínica
│   ├── ingest_knowledge.py # Indexação no Qdrant
│   ├── retriever.py        # Busca semântica
│   ├── memory.py           # Histórico de conversa
│   ├── agent.py            # Orquestração LLM
│   └── api.py              # Webhook FastAPI
├── tests/
├── docker-compose.yml
└── docs-guide/             # Guia completo de construção
````

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.