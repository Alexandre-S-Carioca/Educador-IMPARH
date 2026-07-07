#!/bin/bash

# ============================================================================
# SCRIPT DE SETUP GROQ AUTOMÁTICO
# ============================================================================
#
# Uso: bash setup-groq.sh "sua-chave-groq-aqui"
#
# Exemplo:
#   bash setup-groq.sh "gsk_xxxxxxxxxxxxx"
#
# ============================================================================

set -e  # Exit on error

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     🚀 SETUP AUTOMÁTICO GROQ - EDUCADOR-IMPARH            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Verificar argumentos
if [ -z "$1" ]; then
    echo -e "${YELLOW}❌ Erro: Chave Groq não fornecida${NC}"
    echo ""
    echo "Uso: bash setup-groq.sh \"sua-chave-groq-aqui\""
    echo ""
    echo "Como obter sua chave:"
    echo "  1. Acesse https://console.groq.com"
    echo "  2. Clique em 'API Keys'"
    echo "  3. Clique em 'Create API Key'"
    echo "  4. Copie a chave (começa com gsk_)"
    echo "  5. Execute: bash setup-groq.sh \"gsk_xxx\""
    echo ""
    exit 1
fi

GROQ_API_KEY=$1

# 1. Verificar se estamos no diretório correto
echo -e "${BLUE}[1/5]${NC} Verificando diretório..."
if [ ! -f "backend/requirements.txt" ]; then
    echo -e "${RED}❌ Erro: requirements.txt não encontrado em backend/${NC}"
    echo "Por favor, execute este script a partir da raiz do projeto"
    exit 1
fi
echo -e "${GREEN}✅ Diretório correto${NC}"
echo ""

# 2. Atualizar requirements.txt
echo -e "${BLUE}[2/5]${NC} Atualizando requirements.txt..."
if grep -q "groq" backend/requirements.txt; then
    echo -e "${YELLOW}⚠️  Groq já está em requirements.txt${NC}"
else
    echo "groq>=0.4.0" >> backend/requirements.txt
    echo -e "${GREEN}✅ Groq adicionado a requirements.txt${NC}"
fi
echo ""

# 3. Atualizar config.py
echo -e "${BLUE}[3/5]${NC} Atualizando config.py..."

# Fazer backup
cp backend/app/core/config.py backend/app/core/config.py.backup
echo -e "${GREEN}✅ Backup criado: config.py.backup${NC}"

# Verificar se variáveis já existem
if grep -q "GROQ_API_KEY" backend/app/core/config.py; then
    echo -e "${YELLOW}⚠️  GROQ_API_KEY já configurada em config.py${NC}"
else
    # Inserir antes da linha "model_config"
    sed -i '/model_config = /i\    GROQ_API_KEY: str | None = None\n    AI_PROVIDER: str = "groq"\n    GROQ_MODEL: str = "llama-3.1-8b-instant"' backend/app/core/config.py
    echo -e "${GREEN}✅ Variáveis Groq adicionadas a config.py${NC}"
fi
echo ""

# 4. Atualizar .env
echo -e "${BLUE}[4/5]${NC} Configurando .env..."

# Remover valores antigos se existirem
sed -i '/^GROQ_API_KEY=/d' backend/.env 2>/dev/null || true
sed -i '/^AI_PROVIDER=/d' backend/.env 2>/dev/null || true
sed -i '/^GROQ_MODEL=/d' backend/.env 2>/dev/null || true

# Adicionar novas variáveis
cat >> backend/.env << EOF

# IA Configuration - Groq (adicionado automaticamente)
AI_PROVIDER=groq
GROQ_API_KEY=$GROQ_API_KEY
GROQ_MODEL=llama-3.1-8b-instant
EOF

echo -e "${GREEN}✅ Variáveis configuradas em .env${NC}"
echo ""

# 5. Instalar dependências
echo -e "${BLUE}[5/5]${NC} Instalando dependências Python..."

cd backend

# Verificar se venv existe
if [ -d "venv" ]; then
    echo -e "${YELLOW}ℹ️  Ativando venv existente...${NC}"
    source venv/bin/activate
else
    echo -e "${YELLOW}ℹ️  Criando novo venv...${NC}"
    python3 -m venv venv
    source venv/bin/activate
fi

echo -e "${YELLOW}ℹ️  Instalando groq>=0.4.0...${NC}"
pip install groq>=0.4.0

echo -e "${GREEN}✅ Dependências instaladas${NC}"

cd ..
echo ""

# ============================================================================
# RESUMO
# ============================================================================

echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║ ✅ SETUP CONCLUÍDO COM SUCESSO!                           ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${BLUE}📋 Arquivos modificados:${NC}"
echo "  • backend/requirements.txt (adicionado groq)"
echo "  • backend/app/core/config.py (adicionadas 3 variáveis)"
echo "  • backend/.env (configuradas chaves Groq)"
echo ""

echo -e "${BLUE}📝 Próximos passos:${NC}"
echo ""
echo "1. Substituir o arquivo ai_tutor.py:"
echo "   cp groq_tutor_implementation.py backend/app/infrastructure/services/ai_tutor.py"
echo ""
echo "2. Iniciar o servidor:"
echo "   cd backend"
echo "   uvicorn app.main:app --reload"
echo ""
echo "3. Testar a integração:"
echo "   curl -X POST http://127.0.0.1:8000/api/v1/ai/explain \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"question_id\": \"xxx\", \"selected_option\": \"B\"}'"
echo ""
echo "4. Acessar documentação interativa:"
echo "   http://127.0.0.1:8000/docs"
echo ""

echo -e "${GREEN}✨ Groq está pronto! Agora é 10x mais rápido! ⚡${NC}"
echo ""
echo -e "${YELLOW}📊 Informações da sua conta:${NC}"
echo "  • API Key: ${GROQ_API_KEY:0:10}..."
echo "  • Modelo: llama-3.1-8b-instant"
echo "  • Free Tier: 5.000 req/mês"
echo ""
echo -e "${YELLOW}Monitor em: https://console.groq.com/admin/usage${NC}"
echo ""
