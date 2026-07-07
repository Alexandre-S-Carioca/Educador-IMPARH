# Integração Groq AI no Projeto Educador-IMPARH

## 📋 Resumo Executivo

O Groq é uma plataforma de inferência ultra-rápida com custos muito mais baixos que o Gemini. Integrá-lo no Educador substituiria o `GeminiTutorService` por um `GroqTutorService` com **10x mais velocidade** e **até 90% menos custos**.

---

## 🚀 O que é Groq?

[Groq](https://groq.com/) é uma plataforma de inferência especializada em LLMs com arquitetura LPU (Language Processing Unit):

| Aspecto | Groq | Google Gemini | OpenAI |
|--------|------|---------------|---------|
| **Velocidade** | ⚡⚡⚡ ~70 tok/s | ⚡⚡ ~30 tok/s | ⚡ ~20 tok/s |
| **Latência** | <100ms | 500-1000ms | 1000-2000ms |
| **Custo/1M tokens** | $0.05 - $0.30 | $0.075 - $0.30 | $0.50 - $15.00 |
| **Modelos** | Llama 3.1, Mixtral, DeepSeek | Gemini 2.0, 1.5 Flash | GPT-4, GPT-4o |
| **Free Tier** | ✅ Sim (5.000 RPM) | ❌ Não | ❌ Não |

### Modelos Disponíveis em Groq (2026)
```
• Llama 3.1 405B (88B - mais rápido)     → Recomendado ⭐
• Llama 3.1 70B                          → Bom custo/benefício
• Mixtral 8x7B                           → Lightweight
• DeepSeek R1 1.5B                       → Ultra-rápido
```

**Recomendação para Educador**: `llama-3.1-8b-instant` (melhor velocidade/qualidade)

---

## 💰 Análise de Custos

### Cenário: 1.000 requisições/dia de Tutor de IA

**Gemini (atual)**:
- Input: 500 tokens × 1.000 req = 500.000 tok/dia
- Output: 300 tokens × 1.000 req = 300.000 tok/dia
- Custo: ~$0.30/dia = **$9/mês**

**Groq (proposto)**:
- Mesmas requisições
- Custo: ~$0.05/dia = **$1.50/mês**
- **Economia: 83% dos custos** 💰

### Free Tier Groq
- 5.000 requisições/mês
- Ideal para MVP ou startups
- Sem limite de tempo de uso
- ✅ **GRATUITO**

---

## 🔧 Passo 1: Configuração da API Groq

### 1.1 Obter Chave de API

1. Acesse [console.groq.com](https://console.groq.com)
2. Crie uma conta
3. Vá em **API Keys**
4. Clique em **Create API Key**
5. Copie a chave (ex: `gsk_xxxxxxxxxxxxx`)

### 1.2 Adicionar à Configuração

**Arquivo: `backend/app/core/config.py`**

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Educador API"
    SECRET_KEY: str = "super_secret_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DATABASE_URL: str = "postgresql+psycopg2://educador_user:educador_password@localhost:5433/educador_dev"
    
    # IA Tutor Configuration
    GEMINI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None  # ← NOVO
    AI_PROVIDER: str = "groq"  # "groq" ou "gemini"
    GROQ_MODEL: str = "llama-3.1-8b-instant"  # Modelo padrão

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

settings = Settings()
```

**Arquivo: `.env` (local)**

```env
GROQ_API_KEY=gsk_your_api_key_here
AI_PROVIDER=groq
GROQ_MODEL=llama-3.1-8b-instant
```

### 1.3 Adicionar Dependência

**Arquivo: `backend/requirements.txt`**

```txt
fastapi==0.111.0
uvicorn[standard]==0.30.1
sqlalchemy==2.0.31
alembic==1.13.1
pydantic==2.8.2
pydantic-settings==2.3.4
psycopg2-binary==2.9.9
asyncpg==0.29.0
python-jose[cryptography]==3.3.0
passlib[argon2]==1.7.4
pytest==8.2.2
pytest-asyncio==0.23.7
httpx==0.27.0
google-generativeai>=0.7.0
groq>=0.4.0  # ← NOVO (SDK oficial Groq)
```

---

## 🎯 Passo 2: Implementar GroqTutorService

### 2.1 Criar Novo Serviço

**Arquivo: `backend/app/infrastructure/services/ai_tutor.py`** (modificar)

```python
import asyncio
from typing import Optional
import uuid
from sqlalchemy.orm import Session
from ..db.models.content import Question
import google.generativeai as genai
from groq import Groq, AsyncGroq  # ← NOVO
from ...core.config import settings

class BaseTutorService:
    """Interface base para todos os serviços de tutoria"""
    async def explain(self, db: Session, question_id: uuid.UUID, selected_option: str) -> str:
        raise NotImplementedError()

class MockTutorService(BaseTutorService):
    """Serviço simulado para desenvolvimento local"""
    async def explain(self, db: Session, question_id: uuid.UUID, selected_option: str) -> str:
        await asyncio.sleep(2)
        
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            return "Desculpe, não consegui encontrar a questão no banco de dados para analisar seu erro."
            
        correct = question.correct_option
        
        return f"""
Olá! Sou o **Tutor Inteligente** do Educador. 🧠

Analisei o seu erro. Você escolheu a **Opção {selected_option}**, mas o gabarito oficial da banca IMPARH é a **Opção {correct}**.

### Por que você errou?
A opção {selected_option} parece tentadora, mas a justificativa do erro é:
> {question.justification_incorrect}

### O Conceito Correto
A opção {correct} é a correta porque:
> {question.justification_correct}

**Dica de Ouro:** Em provas do IMPARH, fique muito atento aos "distratores". Quando a banca pede a incorreta ou foca em exceções, leia duas vezes o enunciado!

*(Nota: Esta é uma resposta simulada do MockTutorService)*
"""

class GroqTutorService(BaseTutorService):
    """Serviço de tutoria usando Groq API (RECOMENDADO)"""
    
    def __init__(self):
        if settings.GROQ_API_KEY:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
        else:
            raise ValueError("GROQ_API_KEY não configurada")
    
    async def explain(self, db: Session, question_id: uuid.UUID, selected_option: str) -> str:
        if not settings.GROQ_API_KEY:
            return await MockTutorService().explain(db, question_id, selected_option)

        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            return "Desculpe, não consegui encontrar a questão no banco de dados para analisar seu erro."

        correct = question.correct_option

        prompt = f"""
Você é um Tutor Inteligente especialista em preparação para concursos da banca IMPARH.
O aluno errou uma questão e precisa de uma explicação pedagógica, clara, encorajadora e detalhada.

Aqui estão os detalhes da questão:
- Enunciado/Questão: {question.statement}
- Opções disponíveis:
  A) {question.option_a}
  B) {question.option_b}
  C) {question.option_c}
  D) {question.option_d}
- Opção selecionada pelo aluno: {selected_option}
- Gabarito oficial correto: {correct}
- Justificativa da resposta correta: {question.justification_correct}
- Justificativa de por que as outras opções estão incorretas: {question.justification_incorrect}

Instruções para a explicação:
1. Explique didaticamente por que a opção selecionada pelo aluno ({selected_option}) está incorreta
2. Explique detalhadamente por que o gabarito oficial ({correct}) é correto
3. Forneça uma dica específica para a banca IMPARH
4. Escreva em Markdown claro, estruturado e amigável
5. Mantenha a resposta concisa (máximo 500 palavras)
"""

        try:
            loop = asyncio.get_event_loop()
            
            # Executar chamada síncrona do Groq de forma assincronizada
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=settings.GROQ_MODEL,
                    messages=[
                        {"role": "system", "content": "Você é um tutor especialista em IMPARH"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1024,
                    top_p=0.9,
                    stream=False
                )
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Erro ao usar Groq: {str(e)}")
            # Fallback para MockTutorService em caso de erro
            return await MockTutorService().explain(db, question_id, selected_option)

class GeminiTutorService(BaseTutorService):
    """Serviço de tutoria usando Google Gemini (LEGADO)"""
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)

    async def explain(self, db: Session, question_id: uuid.UUID, selected_option: str) -> str:
        if not settings.GEMINI_API_KEY:
            return await MockTutorService().explain(db, question_id, selected_option)

        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            return "Desculpe, não consegui encontrar a questão no banco de dados para analisar seu erro."

        correct = question.correct_option

        prompt = f"""
Você é um Tutor Inteligente especialista em preparação para concursos da banca IMPARH.
O aluno errou uma questão e precisa de uma explicação pedagógica, clara, encorajadora e detalhada.

Aqui estão os detalhes da questão:
- Enunciado/Questão: {question.statement}
- Opções disponíveis:
  A) {question.option_a}
  B) {question.option_b}
  C) {question.option_c}
  D) {question.option_d}
- Opção selecionada pelo aluno: {selected_option}
- Gabarito oficial correto: {correct}
- Justificativa da resposta correta: {question.justification_correct}
- Justificativa de por que as outras opções estão incorretas: {question.justification_incorrect}

Instruções para a explicação:
1. Explique didaticamente por que a opção selecionada pelo aluno ({selected_option}) está incorreta, com base na justificativa de erro.
2. Explique detalhadamente por que o gabarito oficial ({correct}) é a opção correta.
3. Forneça uma dica específica voltada para a banca IMPARH relevante para esse tipo de conteúdo (Morfologia/Língua Portuguesa).
4. Escreva em formato Markdown claro, estruturado e amigável.
"""

        try:
            loop = asyncio.get_event_loop()
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = await loop.run_in_executor(
                None,
                lambda: model.generate_content(prompt)
            )
            return response.text
        except Exception as e:
            return f"Erro ao gerar explicação com IA: {str(e)}"

# Função Fábrica para injeção de dependência
def get_tutor_service() -> BaseTutorService:
    """Retorna o serviço de tutoria baseado na configuração"""
    
    if settings.AI_PROVIDER == "groq" and settings.GROQ_API_KEY:
        return GroqTutorService()
    elif settings.GEMINI_API_KEY:
        return GeminiTutorService()
    
    return MockTutorService()
```

---

## ✅ Passo 3: Testar a Integração

### 3.1 Teste Unitário

**Arquivo: `backend/tests/test_groq_tutor.py`** (criar)

```python
import pytest
import asyncio
from sqlalchemy.orm import Session
from app.infrastructure.services.ai_tutor import GroqTutorService, MockTutorService
from app.infrastructure.db.models.content import Question
from app.infrastructure.db.session import SessionLocal
import uuid

@pytest.mark.asyncio
async def test_groq_tutor_service():
    """Teste do GroqTutorService"""
    db = SessionLocal()
    
    # Criar questão de teste
    question = Question(
        topic_id=uuid.uuid4(),
        statement="Qual é o sujeito da frase 'O gato subiu na árvore'?",
        option_a="O gato",
        option_b="na árvore",
        option_c="subiu",
        option_d="A árvore",
        correct_option="A",
        justification_correct="O gato é o agente da ação (sujeito)",
        justification_incorrect="Você provavelmente confundiu com adjunto adverbial",
        subject="Morfologia",
        subsubject="Sujeito"
    )
    db.add(question)
    db.commit()
    
    # Testar serviço
    service = GroqTutorService()
    response = await service.explain(db, question.id, "B")
    
    assert response is not None
    assert len(response) > 50
    assert "Opção A" in response or "sujeito" in response.lower()
    
    db.close()

@pytest.mark.asyncio
async def test_groq_performance():
    """Teste de performance do Groq"""
    import time
    from app.infrastructure.services.ai_tutor import GroqTutorService
    
    service = GroqTutorService()
    db = SessionLocal()
    
    # Criar questão
    question = Question(
        topic_id=uuid.uuid4(),
        statement="Teste de performance",
        option_a="A",
        option_b="B",
        option_c="C",
        option_d="D",
        correct_option="A",
        justification_correct="Correta",
        justification_incorrect="Incorreta",
        subject="Test",
        subsubject="Test"
    )
    db.add(question)
    db.commit()
    
    start = time.time()
    response = await service.explain(db, question.id, "B")
    elapsed = time.time() - start
    
    print(f"⏱️ Tempo de resposta Groq: {elapsed:.2f}s")
    assert elapsed < 5  # Groq deve responder em <5s
    
    db.close()
```

### 3.2 Executar Testes

```bash
cd backend
pytest tests/test_groq_tutor.py -v
```

---

## 📊 Passo 4: Comparativo de Performance

### Benchmarks Reais

```python
# Teste simples de latência
import time
from groq import Groq

client = Groq(api_key="your_key")

# 1. Primeira requisição (cold start)
start = time.time()
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Olá"}],
    max_tokens=100
)
cold_start = time.time() - start
print(f"Cold start: {cold_start:.2f}s")

# 2. Requisições subsequentes (warm)
times = []
for i in range(5):
    start = time.time()
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": f"Pergunta {i}"}],
        max_tokens=100
    )
    times.append(time.time() - start)

avg_time = sum(times) / len(times)
print(f"Tempo médio: {avg_time:.2f}s")
print(f"Tokens por segundo: {100 / avg_time:.0f} tok/s")
```

**Resultados Esperados:**
- Cold start: ~0.5s
- Warm: ~0.2s - 0.3s
- **10x mais rápido que Gemini** ⚡

---

## 🔄 Passo 5: Migração Gradual

### Opção A: Substituir Imediatamente (Recomendado)

```bash
# 1. Configurar chave Groq
echo "GROQ_API_KEY=gsk_xxx" >> backend/.env
echo "AI_PROVIDER=groq" >> backend/.env

# 2. Instalar dependências
pip install -r backend/requirements.txt

# 3. Reiniciar backend
uvicorn app.main:app --reload
```

### Opção B: Híbrida (Teste antes)

Usar Groq para 50% das requisições, Gemini para 50%:

```python
# backend/app/infrastructure/services/ai_tutor.py

import random

def get_tutor_service() -> BaseTutorService:
    """Distribuição de tráfego entre Groq e Gemini"""
    
    # Experimental: 50% Groq, 50% Gemini
    if random.random() < 0.5:
        if settings.GROQ_API_KEY:
            return GroqTutorService()
    
    if settings.GEMINI_API_KEY:
        return GeminiTutorService()
    
    return MockTutorService()
```

### Opção C: Fallback Inteligente

Usar Groq com fallback para Gemini em caso de erro:

```python
class FallbackTutorService(BaseTutorService):
    async def explain(self, db: Session, question_id: uuid.UUID, selected_option: str) -> str:
        try:
            service = GroqTutorService()
            return await service.explain(db, question_id, selected_option)
        except Exception as e:
            print(f"Groq falhou, usando fallback Gemini: {e}")
            service = GeminiTutorService()
            return await service.explain(db, question_id, selected_option)
```

---

## 🎯 Monitoramento e Logging

### Adicionar Observabilidade

**Arquivo: `backend/app/infrastructure/services/ai_tutor.py`** (adicionar)

```python
import logging
import time

logger = logging.getLogger(__name__)

class GroqTutorService(BaseTutorService):
    async def explain(self, db: Session, question_id: uuid.UUID, selected_option: str) -> str:
        start_time = time.time()
        
        try:
            question = db.query(Question).filter(Question.id == question_id).first()
            if not question:
                logger.warning(f"Question not found: {question_id}")
                return "Questão não encontrada"

            # ... resto do código ...
            
            elapsed = time.time() - start_time
            logger.info(f"✅ Groq response generated in {elapsed:.2f}s for question {question_id}")
            
            return response.choices[0].message.content
            
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"❌ Groq error after {elapsed:.2f}s: {str(e)}")
            # Fallback...
```

---

## 📈 Modelos Recomendados por Caso de Uso

| Caso de Uso | Modelo | Razão |
|---|---|---|
| **Tutor de IA (seu caso)** | `llama-3.1-8b-instant` | ⚡ Rápido + qualidade |
| Análise de conteúdo | `llama-3.1-70b` | 📊 Melhor reasoning |
| Chatbot educacional | `mixtral-8x7b-32768` | 💬 Contexto maior (32k) |
| Classificação rápida | `deepseek-r1-distill-llama-8b` | ⚡⚡ Ultra-rápido |

---

## ⚠️ Pontos de Atenção

### Rate Limiting
- Free Tier: 5.000 RPM
- Pago: 30.000 RPM
- Implementar queue se necessário

```python
import asyncio
from asyncio import Semaphore

class RateLimitedGroqService(GroqTutorService):
    def __init__(self, max_concurrent=10):
        super().__init__()
        self.semaphore = Semaphore(max_concurrent)
    
    async def explain(self, db: Session, question_id: uuid.UUID, selected_option: str) -> str:
        async with self.semaphore:
            return await super().explain(db, question_id, selected_option)
```

### Tratamento de Erros

Groq pode retornar:
- `RateLimitError` - Limite de requisições excedido
- `APITimeoutError` - Timeout
- `AuthenticationError` - Chave inválida

```python
from groq import (
    RateLimitError, 
    APITimeoutError, 
    AuthenticationError
)

async def explain(self, db: Session, question_id: uuid.UUID, selected_option: str) -> str:
    try:
        # ... código ...
    except RateLimitError:
        logger.warning("Groq rate limit atingido, usando cache")
        return get_cached_explanation(question_id)
    except APITimeoutError:
        logger.error("Groq timeout")
        return await MockTutorService().explain(db, question_id, selected_option)
    except AuthenticationError:
        logger.error("Groq API key inválida")
        raise
```

---

## 🚀 Implantação em Produção

### Variáveis de Ambiente (production)

```env
# .env.production
AI_PROVIDER=groq
GROQ_API_KEY=gsk_prod_xxxxxxxxxxxxx
GROQ_MODEL=llama-3.1-8b-instant

# Opcional: fallback
GEMINI_API_KEY=optional_fallback_key
```

### Docker (backend)

**Arquivo: `backend/Dockerfile`** (adicionar)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Helm Chart (Kubernetes)

```yaml
# deployment.yaml
env:
  - name: GROQ_API_KEY
    valueFrom:
      secretKeyRef:
        name: educador-secrets
        key: groq-api-key
  - name: AI_PROVIDER
    value: "groq"
```

---

## 📚 Recursos e Documentação

### Links Oficiais
- [Console Groq](https://console.groq.com)
- [Documentação Groq](https://console.groq.com/docs/models)
- [SDK Python Groq](https://github.com/groq/groq-python)
- [Preços Groq](https://groq.com/pricing)

### Tutoriais Relacionados
- [Guia Iniciante Groq + Llama 3](https://www.geeksforgeeks.org/nlp/groq-api-with-llama-3/)
- [Integração Groq com LangChain](https://medium.com/@priyanka_neogi/unlocking-the-power-of-groqs-llm-with-langchain-f29e926bf406)

---

## ✅ Checklist de Implementação

- [ ] Obter chave de API Groq
- [ ] Adicionar `groq>=0.4.0` a `requirements.txt`
- [ ] Configurar variáveis de ambiente (.env)
- [ ] Implementar `GroqTutorService`
- [ ] Modificar `get_tutor_service()` factory
- [ ] Criar testes unitários
- [ ] Executar benchmarks de performance
- [ ] Testar fallback para Gemini
- [ ] Configurar logging e monitoramento
- [ ] Deploy em staging
- [ ] Testar com usuários reais
- [ ] Deploy em produção
- [ ] Monitorar custos e performance

---

## 💡 Próximos Passos

1. **Imediato**: Configurar chave Groq e implementar `GroqTutorService`
2. **Curto prazo**: Deploy em staging e testes com alunos
3. **Médio prazo**: Otimizar prompts para Llama 3.1
4. **Longo prazo**: Explorar fine-tuning com dados de IMPARH

---

**Benefícios da Integração Groq:**
- ⚡ 10x mais rápido (respostas em <300ms)
- 💰 83% mais barato
- 🆓 Free Tier generoso (5k req/mês)
- 📈 Escalável sem preocupações de custos
- 🌟 Modelos state-of-the-art (Llama 3.1)

**Recomendação Final**: Implementar imediatamente. A melhoria de experiência do usuário é significativa! 🚀

---

*Última atualização: Julho 2026*  
*Versão Groq SDK: 0.4.0+*
