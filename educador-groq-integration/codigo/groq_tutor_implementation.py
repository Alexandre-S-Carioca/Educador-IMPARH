# ============================================================================
# ARQUIVO: backend/app/infrastructure/services/ai_tutor.py (VERSÃO GROQ)
# ============================================================================
#
# Este arquivo contém os serviços de tutoria com suporte a Groq (recomendado)
# e Gemini (fallback). Copie este conteúdo para substituir seu ai_tutor.py
#
# Requisitos:
# - pip install groq>=0.4.0
# - Configurar GROQ_API_KEY no .env
#
# ============================================================================

import asyncio
import logging
import time
from typing import Optional
import uuid
from sqlalchemy.orm import Session
from ..db.models.content import Question

# Importações de IA
import google.generativeai as genai
from groq import Groq
from groq.types.chat.chat_completion import ChatCompletion

from ...core.config import settings

# Configurar logging
logger = logging.getLogger(__name__)


class BaseTutorService:
    """Interface base para todos os serviços de tutoria"""
    async def explain(self, db: Session, question_id: uuid.UUID, selected_option: str) -> str:
        raise NotImplementedError()


class MockTutorService(BaseTutorService):
    """
    Serviço simulado para desenvolvimento local (sem custos)
    Ideal para testes e desenvolvimento sem chaves de API
    """
    async def explain(self, db: Session, question_id: uuid.UUID, selected_option: str) -> str:
        # Simulando tempo de processamento de IA (2 segundos)
        await asyncio.sleep(2)

        # Buscamos a questão para contextualizar o Mock
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

*(Nota: Esta é uma resposta simulada do MockTutorService. Quando a Groq API for ativada, eu lerei o contexto completo e gerarei um texto dinâmico para você!)*
"""


class GroqTutorService(BaseTutorService):
    """
    Serviço de tutoria usando Groq API - RECOMENDADO ⭐

    Características:
    - 10x mais rápido que Gemini
    - 83% mais barato
    - Free Tier: 5.000 req/mês sem cartão de crédito
    - Modelos: Llama 3.1, Mixtral, DeepSeek

    Setup:
    1. Acesse https://console.groq.com
    2. Crie uma API key
    3. Configure no .env: GROQ_API_KEY=gsk_xxx
    """

    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY não configurada! "
                "Configure a variável de ambiente ou fallback para MockTutorService"
            )

        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
        logger.info(f"✅ GroqTutorService inicializado com modelo: {self.model}")

    async def explain(self, db: Session, question_id: uuid.UUID, selected_option: str) -> str:
        """
        Gera explicação didática de por que o aluno errou

        Args:
            db: Sessão do banco de dados
            question_id: ID da questão
            selected_option: Opção selecionada pelo aluno (A/B/C/D)

        Returns:
            Explicação em Markdown
        """
        start_time = time.time()

        try:
            # Buscar questão
            question = db.query(Question).filter(Question.id == question_id).first()
            if not question:
                logger.warning(f"❌ Questão não encontrada: {question_id}")
                return "Desculpe, não consegui encontrar a questão no banco de dados para analisar seu erro."

            correct = question.correct_option

            # Construir prompt
            prompt = f"""Você é um Tutor Inteligente especialista em preparação para concursos da banca IMPARH.
O aluno errou uma questão e precisa de uma explicação pedagógica, clara, encorajadora e detalhada.

QUESTÃO:
{question.statement}

OPÇÕES:
A) {question.option_a}
B) {question.option_b}
C) {question.option_c}
D) {question.option_d}

RESPOSTA DO ALUNO: {selected_option}
GABARITO CORRETO: {correct}

JUSTIFICATIVA CORRETA:
{question.justification_correct}

JUSTIFICATIVA DO ERRO:
{question.justification_incorrect}

INSTRUÇÕES:
1. Explique didaticamente por que a opção {selected_option} está incorreta
2. Explique detalhadamente por que a opção {correct} é correta
3. Forneça uma dica específica para evitar esse erro em provas IMPARH
4. Mantenha um tom amigável e encorajador
5. Use Markdown para estruturar a resposta
6. Máximo 500 palavras"""

            # Chamar Groq API
            loop = asyncio.get_event_loop()

            response: ChatCompletion = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "Você é um tutor especialista em IMPARH, pedagógico e encorajador."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=1024,
                    top_p=0.9,
                    stream=False
                )
            )

            elapsed = time.time() - start_time
            logger.info(f"✅ Groq respondeu em {elapsed:.2f}s para questão {question_id}")

            return response.choices[0].message.content

        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"❌ Erro Groq após {elapsed:.2f}s: {str(e)}")
            logger.info("🔄 Usando fallback MockTutorService...")

            # Fallback para Mock em caso de erro
            return await MockTutorService().explain(db, question_id, selected_option)


class GeminiTutorService(BaseTutorService):
    """
    Serviço de tutoria usando Google Gemini API (LEGADO)

    Use este apenas se não tiver acesso a Groq.
    Mais lento e mais caro que Groq.
    """
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
        else:
            raise ValueError("GEMINI_API_KEY não configurada")

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
            logger.info(f"✅ Gemini respondeu para questão {question_id}")
            return response.text
        except Exception as e:
            logger.error(f"❌ Erro Gemini: {str(e)}")
            return f"Erro ao gerar explicação com IA: {str(e)}\n\n*(Nota: Ocorreu uma falha de conexão com a API)*"


def get_tutor_service() -> BaseTutorService:
    """
    Factory function que retorna o serviço de tutoria correto
    baseado na configuração de ambiente.

    Ordem de preferência:
    1. Groq (recomendado)
    2. Gemini (fallback)
    3. Mock (desenvolvimento)

    Configurações no .env:
    - AI_PROVIDER=groq|gemini
    - GROQ_API_KEY=gsk_xxx
    - GROQ_MODEL=llama-3.1-8b-instant
    - GEMINI_API_KEY=xxx (opcional)
    """

    # Preferência 1: Groq
    if settings.AI_PROVIDER == "groq" and settings.GROQ_API_KEY:
        try:
            logger.info("🚀 Usando GroqTutorService")
            return GroqTutorService()
        except Exception as e:
            logger.warning(f"⚠️ Erro ao inicializar Groq: {e}. Tentando Gemini...")

    # Preferência 2: Gemini
    if settings.GEMINI_API_KEY:
        try:
            logger.info("🚀 Usando GeminiTutorService")
            return GeminiTutorService()
        except Exception as e:
            logger.warning(f"⚠️ Erro ao inicializar Gemini: {e}. Usando MockTutorService...")

    # Fallback: Mock (sempre funciona)
    logger.warning("⚠️ Nenhuma chave de API configurada. Usando MockTutorService (sem custos, mas sem IA real)")
    return MockTutorService()
