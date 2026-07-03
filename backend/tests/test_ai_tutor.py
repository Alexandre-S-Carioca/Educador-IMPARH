import pytest
from unittest.mock import MagicMock, patch
from app.infrastructure.services.ai_tutor import GeminiTutorService, MockTutorService, get_tutor_service
from app.infrastructure.db.models.content import Question
from app.core.config import settings

@pytest.mark.asyncio
@patch("google.generativeai.GenerativeModel")
async def test_gemini_tutor_service_explain(mock_genai_model, db):
    # Configura o mock do modelo Gemini
    mock_model_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Esta é uma explicação simulada pelo modelo Gemini real nos testes."
    mock_model_instance.generate_content.return_value = mock_response
    mock_genai_model.return_value = mock_model_instance

    # Criar estruturas necessárias no DB SQLite de testes para satisfazer FKeys
    from app.infrastructure.db.models.course import Course, Module, Unit, Topic
    
    course = Course(name="Curso de Teste")
    db.add(course)
    db.commit()
    
    module = Module(course_id=course.id, title="Módulo de Teste")
    db.add(module)
    db.commit()
    
    unit = Unit(module_id=module.id, title="Unidade de Teste")
    db.add(unit)
    db.commit()
    
    topic = Topic(unit_id=unit.id, title="Tópico de Teste")
    db.add(topic)
    db.commit()
    
    question = Question(
        topic_id=topic.id,
        statement="Questão de teste?",
        option_a="A",
        option_b="B",
        option_c="C",
        option_d="D",
        correct_option="A",
        justification_correct="Justificativa correta",
        justification_incorrect="Justificativa incorreta",
        subject="Português",
        subsubject="Morfologia"
    )
    db.add(question)
    db.commit()

    # Injetamos temporariamente a chave de API nas configurações
    original_key = settings.GEMINI_API_KEY
    settings.GEMINI_API_KEY = "test_api_key"

    try:
        service = GeminiTutorService()
        explanation = await service.explain(db, question.id, "B")
        
        assert "Esta é uma explicação simulada pelo modelo Gemini real" in explanation
        mock_genai_model.assert_called_once_with("gemini-1.5-flash")
        mock_model_instance.generate_content.assert_called_once()
    finally:
        # Restaura os valores e limpa o banco de testes
        settings.GEMINI_API_KEY = original_key
        db.delete(question)
        db.delete(topic)
        db.delete(unit)
        db.delete(module)
        db.delete(course)
        db.commit()

def test_get_tutor_service_with_or_without_key():
    original_key = settings.GEMINI_API_KEY
    
    # Sem chave -> Retorna o MockTutorService
    settings.GEMINI_API_KEY = None
    service = get_tutor_service()
    assert isinstance(service, MockTutorService)
    
    # Com chave -> Retorna o GeminiTutorService
    settings.GEMINI_API_KEY = "dummy_key"
    service = get_tutor_service()
    assert isinstance(service, GeminiTutorService)
    
    settings.GEMINI_API_KEY = original_key
