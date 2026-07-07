# Mudanças Necessárias para Integrar Groq

## 📋 Checklist Rápido

```bash
# 1. Atualizar requirements.txt
# 2. Atualizar config.py
# 3. Atualizar .env
# 4. Substituir ai_tutor.py
# 5. Testar
```

---

## 1️⃣ Atualizar `backend/requirements.txt`

**Adicione esta linha:**

```txt
groq>=0.4.0
```

**Arquivo completo recomendado:**

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
groq>=0.4.0
```

---

## 2️⃣ Atualizar `backend/app/core/config.py`

**Adicione estas linhas:**

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
    GROQ_API_KEY: str | None = None  # ← ADICIONE ESTA LINHA
    AI_PROVIDER: str = "groq"  # ← ADICIONE ESTA LINHA (defini default como "groq")
    GROQ_MODEL: str = "llama-3.1-8b-instant"  # ← ADICIONE ESTA LINHA

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

settings = Settings()
```

---

## 3️⃣ Atualizar `backend/.env` (Local Development)

**Adicione estas variáveis:**

```env
# IA Configuration
AI_PROVIDER=groq
GROQ_API_KEY=gsk_YOUR_API_KEY_HERE
GROQ_MODEL=llama-3.1-8b-instant

# Opcional: manter Gemini como fallback
GEMINI_API_KEY=
```

**Como obter sua chave Groq:**

1. Acesse https://console.groq.com
2. Faça login (criar conta se necessário)
3. Clique em **API Keys** (no menu esquerdo)
4. Clique em **Create API Key**
5. Copie a chave (começa com `gsk_`)
6. Cole no .env como `GROQ_API_KEY=gsk_xxx`

---

## 4️⃣ Substituir `backend/app/infrastructure/services/ai_tutor.py`

**Opção A: Copiar arquivo completo**

Use o arquivo `groq_tutor_implementation.py` que foi enviado anteriormente.

**Opção B: Fazer merge com seu arquivo atual**

Se você tem modificações customizadas, mescle:

```python
# Adicione no topo do arquivo:
from groq import Groq
import logging

logger = logging.getLogger(__name__)

# Adicione a classe GroqTutorService (veja arquivo groq_tutor_implementation.py)

# Modifique a função get_tutor_service():
def get_tutor_service() -> BaseTutorService:
    # Preferência 1: Groq
    if settings.AI_PROVIDER == "groq" and settings.GROQ_API_KEY:
        try:
            return GroqTutorService()
        except Exception as e:
            logger.warning(f"Erro Groq: {e}. Tentando Gemini...")
    
    # Preferência 2: Gemini
    if settings.GEMINI_API_KEY:
        return GeminiTutorService()
    
    # Fallback: Mock
    return MockTutorService()
```

---

## 5️⃣ Testar a Integração

### Test Local

```bash
# 1. Navegar para backend
cd backend

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Iniciar servidor
uvicorn app.main:app --reload

# 4. Acessar documentação
# Abra http://127.0.0.1:8000/docs no navegador

# 5. Testar endpoint AI
POST http://127.0.0.1:8000/api/v1/ai/explain
{
  "question_id": "uuid-da-questao",
  "selected_option": "B"
}
```

### Test com Python

```python
# backend/test_groq.py

import asyncio
from sqlalchemy.orm import sessionmaker
from app.infrastructure.db.session import get_db, engine
from app.infrastructure.services.ai_tutor import get_tutor_service
from app.infrastructure.db.models.content import Question
import uuid

async def test_groq():
    """Teste rápido do Groq"""
    
    # Criar sessão
    SessionLocal = sessionmaker(bind=engine)
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
        justification_incorrect="Na árvore é um adjunto adverbial de lugar",
        subject="Morfologia",
        subsubject="Sujeito"
    )
    db.add(question)
    db.commit()
    
    # Testar serviço
    print("🧪 Testando GroqTutorService...")
    service = get_tutor_service()
    
    response = await service.explain(db, question.id, "B")
    
    print(f"✅ Resposta recebida:\n{response}")
    print(f"\n📊 Comprimento: {len(response)} caracteres")
    
    db.close()

# Executar teste
if __name__ == "__main__":
    asyncio.run(test_groq())
```

**Para rodar o teste:**

```bash
cd backend
python test_groq.py
```

---

## 6️⃣ Verificar Logs

Depois de iniciar o servidor, procure por:

```
✅ GroqTutorService inicializado com modelo: llama-3.1-8b-instant
✅ Groq respondeu em 0.45s para questão xxx
```

Se aparecer erro:

```
❌ Erro Groq: GROQ_API_KEY not provided
🔄 Usando fallback MockTutorService...
```

Significa que a chave Groq não está configurada. Verifique `.env`.

---

## 7️⃣ Monitorar Custos (Opcional)

Acesse https://console.groq.com/admin/usage para ver:
- Requisições utilizadas
- Tokens processados
- Estimativa de custos
- Período de faturamento

---

## 🔄 Rollback (Se Necessário)

Se quiser voltar para Gemini:

```env
# Mudar de:
AI_PROVIDER=groq

# Para:
AI_PROVIDER=gemini
```

O sistema vai usar Gemini automaticamente se `AI_PROVIDER=gemini`.

---

## 🆘 Troubleshooting

### Erro: `GROQ_API_KEY not found`

**Solução:**
```bash
# Verificar se .env existe
cat backend/.env

# Verificar se variável está configurada
echo $GROQ_API_KEY

# Recarregar terminal e tentar novamente
```

### Erro: `groq module not found`

**Solução:**
```bash
pip install groq>=0.4.0
# ou
pip install -r requirements.txt
```

### Respostas lentas do Groq

**Possíveis causas:**
- Modelo sobrecarregado (usar `llama-3.1-8b-instant` é mais rápido)
- Conexão lenta
- Prompt muito longo

**Solução:**
```python
# Reduzir max_tokens
max_tokens=512  # em vez de 1024
```

### Erro: `Rate limit exceeded`

**Significa:** Excedeu limite gratuito (5.000 req/mês)

**Solução:**
1. Upgrade para plano pago
2. Usar MockTutorService
3. Implementar cache das respostas

---

## 📊 Resumo das Mudanças

| Arquivo | Mudança | Linhas |
|---------|---------|--------|
| `requirements.txt` | Adicionar `groq>=0.4.0` | +1 |
| `config.py` | Adicionar 3 variáveis | +3 |
| `.env` | Adicionar chave Groq | +3 |
| `ai_tutor.py` | Substituir arquivo completo | +150 |
| **TOTAL** | - | **~160 linhas** |

---

## ✅ Ordem de Implementação Recomendada

1. **Dia 1**: Obter chave Groq + atualizar `requirements.txt` + `config.py`
2. **Dia 1**: Atualizar `.env` + substituir `ai_tutor.py`
3. **Dia 1**: Testar localmente (test_groq.py)
4. **Dia 2**: Deploy em staging
5. **Dia 3**: Testes com usuários
6. **Dia 4**: Deploy em produção

---

## 🎯 Próximos Passos

1. Seguir este guia passo a passo
2. Testar respostas do Groq
3. Monitorar performance (tempo de resposta)
4. Coletar feedback de usuários
5. Ajustar prompts se necessário

---

**Tempo estimado de implementação**: 30 minutos ⚡
**Dificuldade**: Fácil 🟢
**Benefício**: 10x mais rápido + 83% mais barato 💰

Good luck! 🚀
