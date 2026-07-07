"""
ARQUIVO DE TESTE: backend/test_groq.py

Copie este arquivo para a raiz do backend e execute:
    python test_groq.py

Isso vai testar se o Groq está funcionando corretamente.
"""

import asyncio
import sys
import time
from pathlib import Path

# Adicionar backend ao path
sys.path.insert(0, str(Path(__file__).parent))

# Importar após configurar o path
from sqlalchemy.orm import sessionmaker
from app.infrastructure.db.session import engine
from app.infrastructure.db.models.content import Question
from app.infrastructure.services.ai_tutor import get_tutor_service
from app.core.config import settings
import uuid


async def test_groq_tutor():
    """
    Teste funcional do GroqTutorService
    """

    print("=" * 70)
    print("🧪 TESTE DO GROQ TUTOR SERVICE")
    print("=" * 70)
    print()

    # 1. Verificar configuração
    print("📋 VERIFICANDO CONFIGURAÇÃO:")
    print(f"  • AI_PROVIDER: {settings.AI_PROVIDER}")
    print(f"  • GROQ_API_KEY: {settings.GROQ_API_KEY[:15]}..." if settings.GROQ_API_KEY else "  • GROQ_API_KEY: ❌ NÃO CONFIGURADA")
    print(f"  • GROQ_MODEL: {settings.GROQ_MODEL}")
    print()

    # 2. Criar sessão de banco de dados
    print("🔌 CONECTANDO AO BANCO DE DADOS...")
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        # 3. Criar questão de teste
        print("📝 CRIANDO QUESTÃO DE TESTE...")
        question = Question(
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
        db.add(question)
        db.commit()
        print(f"  ✅ Questão criada com ID: {question.id}")
        print()

        # 4. Obter serviço de tutoria
        print("🤖 INICIALIZANDO SERVIÇO DE TUTORIA...")
        service = get_tutor_service()
        print(f"  ✅ Serviço: {service.__class__.__name__}")
        print()

        # 5. Testar explicação
        print("⏱️  ENVIANDO REQUISIÇÃO PARA O GROQ...")
        print("   (Aguarde a resposta do servidor...)")
        print()

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

        # 6. Validações
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

        if "GROQ_API_KEY" in str(e):
            print("💡 DICA: Chave Groq não configurada. Configure em .env:")
            print("   GROQ_API_KEY=gsk_sua_chave_aqui")
        elif "rate limit" in str(e).lower():
            print("💡 DICA: Limite de requisições atingido (Free Tier: 5k/mês)")
            print("   Espere até o próximo período de faturamento")

        print()
        return False

    finally:
        db.close()


async def test_multiple_requests():
    """
    Teste com múltiplas requisições (simular carga)
    """
    print()
    print("=" * 70)
    print("🔥 TESTE DE MÚLTIPLAS REQUISIÇÕES (3x)")
    print("=" * 70)
    print()

    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        service = get_tutor_service()
        times = []

        for i in range(1, 4):
            # Criar questão diferente cada vez
            question = Question(
                topic_id=uuid.uuid4(),
                statement=f"Questão de teste {i}: Qual alternativa está correta?",
                option_a="Alternativa A",
                option_b="Alternativa B",
                option_c="Alternativa C",
                option_d="Alternativa D",
                correct_option="A",
                justification_correct=f"A é correta porque...",
                justification_incorrect=f"As outras não são...",
                subject="Teste",
                subsubject="Teste",
                difficulty=1
            )
            db.add(question)
            db.commit()

            print(f"📍 Requisição {i}/3...")
            start = time.time()
            response = await service.explain(db, question.id, "C")
            elapsed = time.time() - start
            times.append(elapsed)

            print(f"   ✅ Respondido em {elapsed:.2f}s ({len(response)} chars)")

        print()
        avg_time = sum(times) / len(times)
        print(f"📊 MÉDIA: {avg_time:.2f}s por requisição")
        print(f"   Min: {min(times):.2f}s | Max: {max(times):.2f}s")

        if avg_time < 1:
            print(f"   🚀 Excelente performance! (< 1s)")
        elif avg_time < 2:
            print(f"   ⚡ Boa performance (< 2s)")
        else:
            print(f"   🐢 Performance aceitável (< 3s)")

        print()

    finally:
        db.close()


async def main():
    """Executar todos os testes"""

    # Teste principal
    success = await test_groq_tutor()

    if success:
        # Teste secundário (múltiplas requisições)
        try:
            await test_multiple_requests()
        except Exception as e:
            print(f"⚠️  Teste de múltiplas requisições falhou: {e}")

    print()
    print("=" * 70)
    print("✨ TESTE FINALIZADO")
    print("=" * 70)
    print()
    print("📌 Próximos passos:")
    print("  1. Se passou: Deploy em staging")
    print("  2. Testar com usuários reais")
    print("  3. Monitorar em https://console.groq.com/admin/usage")
    print("  4. Deploy em produção")
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
