import asyncio
from typing import Optional
import uuid
from sqlalchemy.orm import Session
from ..db.models.content import Question
import google.generativeai as genai
from ...core.config import settings

class BaseTutorService:
    async def explain(self, db: Session, question_id: uuid.UUID, selected_option: str) -> str:
        raise NotImplementedError()

class MockTutorService(BaseTutorService):
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

*(Nota: Esta é uma resposta simulada do MockTutorService. Quando a Gemini API for ativada, eu lerei o contexto completo e gerarei um texto dinâmico para você!)*
"""

class GeminiTutorService(BaseTutorService):
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)

    async def explain(self, db: Session, question_id: uuid.UUID, selected_option: str) -> str:
        if not settings.GEMINI_API_KEY:
            # Fallback para o MockTutorService se a chave não estiver configurada
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
            return f"Erro ao gerar explicação com IA: {str(e)}\n\n*(Nota: Ocorreu uma falha de conexão com a API do Gemini)*"

# Função Fábrica para injeção de dependência
def get_tutor_service() -> BaseTutorService:
    if settings.GEMINI_API_KEY:
        return GeminiTutorService()
    return MockTutorService()
