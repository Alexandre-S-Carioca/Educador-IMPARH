import asyncio
import sys
import time
from pathlib import Path

# Adicionar backend ao path
sys.path.insert(0, str(Path(__file__).parent))

# Importar após configurar o path
from app.infrastructure.db.models.content import Question
from app.infrastructure.services.ai_tutor import get_tutor_service
from app.core.config import settings
import uuid


class MockDB:
    """Mock do banco de dados para evitar dependência do postgres/docker durante o teste da API"""
    def __init__(self, question):
        self.question = question

    def query(self, model):
        return self

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return self.question


async def test_groq_tutor():
    """
    Teste funcional do GroqTutorService usando MockDB
    """

    print("=" * 70)
    print("🧪 TESTE DO GROQ TUTOR SERVICE (MOCK DB)")
    print("=" * 70)
    print()

    # 1. Verificar configuração
    print("📋 VERIFICANDO CONFIGURAÇÃO:")
    print(f"  • AI_PROVIDER: {settings.AI_PROVIDER}")
    print(f"  • GROQ_API_KEY: {settings.GROQ_API_KEY[:15]}..." if settings.GROQ_API_KEY else "  • GROQ_API_KEY: ❌ NÃO CONFIGURADA")
    print(f"  • GROQ_MODEL: {settings.GROQ_MODEL}")
    print()

    # 2. Criar questão de teste
    print("📝 CRIANDO QUESTÃO DE TESTE...")
    question = Question(
        id=uuid.uuid4(),
        topic_id=uuid.uuid4(),
        statement="Qual é o sujeito da frase 'O gato subiu na árvore'?",
        option_a="O gato",
        option_b="na árvore",
        option_c="subiu",
        option_d="A árvore",
        correct_option="A",
        justification_correct="O gato é o agente da ação (sujeito). É aquele que realiza a ação de subir.",
        justification_incorrect="Na árvore é um adjunto adverbial de lugar, não o sujeito.",
        subject="Morfologia",
        subsubject="Análise Sintática",
        difficulty=1
    )
    db = MockDB(question)
    print(f"  ✅ Questão criada (em memória) com ID: {question.id}")
    print()

    # 3. Obter serviço de tutoria
    print("🤖 INICIALIZANDO SERVIÇO DE TUTORIA...")
    service = get_tutor_service()
    print(f"  ✅ Serviço: {service.__class__.__name__}")
    print()

    # 4. Testar explicação
    print("⏱️  ENVIANDO REQUISIÇÃO PARA O GROQ...")
    print("   (Aguarde a resposta do servidor...)")
    print()

    try:
        start_time = time.time()
        response = await service.explain(db, question.id, "B")
        elapsed = time.time() - start_time

        print("=" * 70)
        print("✅ RESPOSTA RECEBIDA!")
        print("=" * 70)
        print()
        print(response)
        print()
        print("=" * 70)
        print(f"📊 ESTATÍSTICAS:")
        print(f"  • Tempo de resposta: {elapsed:.2f} segundos")
        print(f"  • Comprimento: {len(response)} caracteres")
        print(f"  • Linhas: {len(response.split(chr(10)))} linhas")
        print("=" * 70)
        print()

        # 5. Validações
        print("✓ VALIDAÇÕES:")

        # Validar conteúdo
        if "Opção B" in response or "opção B" in response.lower():
            print("  ✅ Menciona a opção errada (B)")
        else:
            print("  ⚠️  Não menciona claramente a opção B")

        if "Opção A" in response or "opção A" in response.lower():
            print("  ✅ Menciona a opção correta (A)")
        else:
            print("  ⚠️  Não menciona claramente a opção A")

        if len(response) > 200:
            print("  ✅ Resposta tem tamanho apropriado")
        else:
            print("  ⚠️  Resposta muito curta")

        if elapsed < 3:
            print(f"  ✅ Resposta rápida ({elapsed:.2f}s < 3s)")
        else:
            print(f"  ⚠️  Resposta lenta ({elapsed:.2f}s)")

        print()
        print("🎉 TESTE COMPLETADO COM SUCESSO!")
        print()
        return True

    except Exception as e:
        print()
        print("❌ ERRO DURANTE O TESTE:")
        print(f"  {type(e).__name__}: {str(e)}")
        print()
        return False


async def main():
    """Executar todos os testes"""
    await test_groq_tutor()
    print()
    print("=" * 70)
    print("✨ TESTE FINALIZADO")
    print("=" * 70)
    print()


if __name__ == "__main__":
    print()
    print("🚀 Iniciando testes do Groq...")
    print()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print()
        print("⏹️  Teste cancelado pelo usuário")
        sys.exit(0)
    except Exception as e:
        print()
        print(f"❌ Erro fatal: {e}")
        sys.exit(1)
