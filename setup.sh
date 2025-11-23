#!/bin/bash

# Script de setup automático para Medical News Bot
# Execute: bash setup.sh

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║           🏥 MEDICAL NEWS BOT - SETUP                     ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verifica Python
echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 não encontrado!${NC}"
    echo "   Instale Python 3.8+ e tente novamente"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION encontrado${NC}"

# Verifica pip
echo ""
echo "🔍 Verificando pip..."
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip não encontrado!${NC}"
    echo "   Instalando pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
fi
echo -e "${GREEN}✅ pip encontrado${NC}"

# Cria ambiente virtual (recomendado)
echo ""
echo "🔧 Criando ambiente virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Ambiente virtual criado${NC}"
else
    echo -e "${YELLOW}⚠️  Ambiente virtual já existe${NC}"
fi

# Ativa ambiente virtual
echo ""
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instala dependências
echo ""
echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependências instaladas com sucesso${NC}"
else
    echo -e "${RED}❌ Erro ao instalar dependências${NC}"
    exit 1
fi

# Cria diretórios necessários
echo ""
echo "📁 Criando diretórios..."
mkdir -p data logs generated_images
echo -e "${GREEN}✅ Diretórios criados${NC}"

# Cria arquivo .env se não existir
echo ""
if [ ! -f ".env" ]; then
    echo "📝 Criando arquivo de configuração..."
    cp .env.example .env
    echo -e "${GREEN}✅ Arquivo .env criado${NC}"
    echo -e "${YELLOW}⚠️  IMPORTANTE: Edite o arquivo .env com suas credenciais!${NC}"
else
    echo -e "${YELLOW}⚠️  Arquivo .env já existe (não sobrescrito)${NC}"
fi

# Verifica se credenciais foram configuradas
echo ""
if grep -q "seu_usuario" .env; then
    echo -e "${YELLOW}⚠️  ATENÇÃO: Configure suas credenciais no arquivo .env${NC}"
    echo ""
    echo "   Execute:"
    echo "   nano .env"
    echo ""
    echo "   E substitua:"
    echo "   - seu_usuario → seu usuário do Instagram"
    echo "   - sua_senha → sua senha do Instagram"
else
    echo -e "${GREEN}✅ Credenciais configuradas${NC}"
fi

# Testa instalação
echo ""
echo "🧪 Testando instalação..."
python3 -c "
import feedparser
import requests
from PIL import Image
from instagrapi import Client
from deep_translator import GoogleTranslator
print('✅ Todos os módulos importados com sucesso!')
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Teste de importação passou!${NC}"
else
    echo -e "${RED}❌ Erro ao importar módulos${NC}"
    exit 1
fi

# Resumo final
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                    SETUP CONCLUÍDO! ✅                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Próximos passos:"
echo ""
echo "1. Configure suas credenciais:"
echo "   ${YELLOW}nano .env${NC}"
echo ""
echo "2. Teste o bot:"
echo "   ${GREEN}source venv/bin/activate${NC}"
echo "   ${GREEN}python main.py --stats${NC}"
echo ""
echo "3. Faça uma publicação teste:"
echo "   ${GREEN}python main.py --now${NC}"
echo ""
echo "4. Execute em modo automático:"
echo "   ${GREEN}python main.py${NC}"
echo ""
echo "📚 Documentação completa: README.md"
echo ""
echo "🆘 Precisa de ajuda? Abra uma issue no GitHub"
echo ""
