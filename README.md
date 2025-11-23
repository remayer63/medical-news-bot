# 🏥 Medical News Bot - Instagram Automation

Bot automatizado para publicação de notícias médicas no Instagram em formato de carrossel.

## 📋 Características

✅ **100% Gratuito** - Usa apenas recursos open-source  
✅ **Multi-plataforma** - Compatível com Instagram, TikTok e Facebook  
✅ **Tradução Automática** - Converte notícias em inglês para português  
✅ **Design Profissional** - Carrosséis otimizados para engajamento  
✅ **Agendamento Inteligente** - Publica nos melhores horários  
✅ **Filtro de Relevância** - Apenas notícias de alto impacto  

## 🎯 Áreas Médicas Cobertas

- 🫀 Cardiologia
- 💉 Hipertensão Arterial Sistêmica
- ⚖️ Obesidade
- 🩺 Diabetes Mellitus
- 🔬 Doença Hepática Esteatótica

## 📅 Estratégia de Publicação

### Frequência Semanal
- **4 posts de carrossel** por semana
- **2 stories** por dia (opcional)

### Melhores Horários (Baseado em Pesquisas 2024-2025)
| Dia | Horário | Motivo |
|-----|---------|--------|
| Terça | 13h | **MELHOR** - Pico de engajamento médico |
| Quarta | 11h | Alto engajamento profissional |
| Quinta | 15h | Boa interação pós-almoço |
| Segunda | 17h | Fim do expediente |

### Por que esses horários?
- ✅ Profissionais da saúde estão ativos
- ✅ Pacientes buscam informações
- ✅ Algoritmo favorece consistência

## 🚀 Instalação

### 1. Pré-requisitos

```bash
# Python 3.8 ou superior
python --version

# Git (opcional)
git --version
```

### 2. Clone ou Baixe o Projeto

```bash
# Opção 1: Com Git
git clone https://github.com/seu-usuario/medical-news-bot.git
cd medical-news-bot

# Opção 2: Baixe o ZIP e extraia
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

**Pacotes instalados:**
- `feedparser` - Leitura de RSS feeds
- `instagrapi` - API do Instagram
- `Pillow` - Criação de imagens
- `deep-translator` - Tradução gratuita
- `schedule` - Agendamento de tarefas
- `beautifulsoup4` - Parsing de HTML

### 4. Configure as Credenciais

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite com suas credenciais
nano .env  # ou use seu editor favorito
```

**Conteúdo do .env:**
```env
INSTAGRAM_USERNAME=seu_usuario_instagram
INSTAGRAM_PASSWORD=sua_senha_instagram

# Opcional: ajustar configurações
POSTS_PER_WEEK=4
MIN_IMPACT_SCORE=7
```

⚠️ **IMPORTANTE:**
- Use uma conta específica para o bot
- Ative autenticação de dois fatores no Instagram
- Guarde o arquivo `.env` em segredo (nunca compartilhe)

### 5. Teste a Instalação

```bash
# Testa login e mostra estatísticas
python main.py --stats
```

## 📖 Como Usar

### Modo 1: Execução Agendada (Recomendado)

```bash
# Inicia o bot em modo automático
python main.py
```

O bot ficará rodando e publicará automaticamente nos horários configurados.

**Saída esperada:**
```
🤖 Bot em execução (Ctrl+C para parar)...

📅 Próxima publicação: 23/11/2024 13:00
```

### Modo 2: Teste Imediato

```bash
# Publica uma vez agora (para testes)
python main.py --now
```

Use este modo para:
- ✅ Testar se tudo está funcionando
- ✅ Ver como ficam os carrosséis
- ✅ Ajustar cores e textos

### Modo 3: Ver Estatísticas

```bash
# Mostra informações da conta
python main.py --stats
```

### Modo 4: Rodar em Servidor 24/7

Para manter o bot rodando mesmo após fechar o terminal:

```bash
# Linux/Mac - Com screen
screen -S medical-bot
python main.py
# Ctrl+A depois D para sair (mantém rodando)

# Para voltar:
screen -r medical-bot

# Ou com nohup
nohup python main.py > bot.log 2>&1 &
```

## 🎨 Personalização

### Alterar Cores do Design

Edite `config.py`:

```python
CAROUSEL_SETTINGS = {
    'colors': {
        'primary': '#2C5F7C',      # Cor principal (cabeçalho)
        'secondary': '#4A90A4',    # Cor secundária
        'accent': '#E74C3C',       # Cor de destaque
        'background': '#F8F9FA',   # Fundo
        'text': '#2C3E50',         # Cor do texto
    }
}
```

### Adicionar Novas Fontes de Notícias

Edite `config.py`:

```python
NEWS_SOURCES = {
    'nova_fonte': {
        'url': 'https://site.com/rss',
        'topics': ['tópico médico'],
        'lang': 'pt'  # ou 'en'
    }
}
```

### Mudar Horários de Publicação

Edite `config.py`:

```python
POSTING_SCHEDULE = [
    (1, 13, 0),   # (dia_semana, hora, minuto)
    (2, 11, 0),   # 0=Segunda, 1=Terça, etc.
]
```

### Customizar Hashtags

Edite `config.py`:

```python
HASHTAGS = {
    'cardiologia': ['#cardiologia', '#coração', '#suashashtags'],
    'geral': ['#medicina', '#saude', '#suashashtags']
}
```

## 🔧 Solução de Problemas

### Erro: "Login failed"

**Causas comuns:**
1. Usuário/senha incorretos
2. Instagram bloqueou login por segurança
3. Autenticação de dois fatores ativada

**Soluções:**
```bash
# 1. Verifique credenciais no .env
cat .env

# 2. Tente fazer login manualmente no navegador
# 3. Desative 2FA temporariamente ou use app password

# 4. Aguarde 24h se Instagram bloqueou
```

### Erro: "No module named 'X'"

```bash
# Reinstale dependências
pip install -r requirements.txt --upgrade
```

### Erro: "Rate limit exceeded"

Instagram tem limites de postagens:
- **Máximo:** ~25 posts por dia
- **Recomendado:** 4-7 posts por semana

Solução: Ajuste `POSTING_SCHEDULE` para menos postagens.

### Imagens não aparecem corretamente

```bash
# Verifique se Pillow instalou corretamente
python -c "from PIL import Image; print('OK')"

# Reinstale Pillow
pip uninstall Pillow
pip install Pillow
```

### Bot para de funcionar

```bash
# Verifique logs
tail -f bot.log

# Reinicie o bot
python main.py
```

## 📊 Métricas de Sucesso

### O que Acompanhar

1. **Taxa de Engajamento**
   - Meta: 3-5% (curtidas + comentários / seguidores)

2. **Crescimento de Seguidores**
   - Meta: 5-10% ao mês (com conteúdo de qualidade)

3. **Alcance**
   - Meta: 20-30% dos seguidores veem cada post

4. **Salvamentos**
   - Métrica importante: indica conteúdo valioso

### Como Melhorar Resultados

✅ **Consistência** - Poste regularmente (4x/semana)  
✅ **Horários** - Siga os horários recomendados  
✅ **Qualidade** - Priorize notícias relevantes (score alto)  
✅ **Interação** - Responda comentários rapidamente  
✅ **Stories** - Use para engajamento diário  
✅ **CTA** - Sempre peça interação ("comente", "salve")  

## 🌐 Adaptação para Outras Plataformas

### TikTok

1. Converta carrosséis em vídeos curtos (15-60s)
2. Use `tiktokapipy` ou `TikTokApi`
3. Adicione narração com TTS

### Facebook

```python
# Instale SDK do Facebook
pip install facebook-sdk

# Use mesmo código, apenas mude o publisher
from facebook import GraphAPI
```

### LinkedIn (Profissional)

```python
# Mais apropriado para conteúdo médico profissional
pip install python-linkedin-v2
```

## 🔒 Segurança e Compliance

### Boas Práticas

✅ **Nunca compartilhe** o arquivo `.env`  
✅ **Use conta secundária** para testes  
✅ **Revise conteúdo** antes de publicar  
✅ **Cite fontes** sempre (PubMed, etc.)  
✅ **Aviso médico:** "Este conteúdo é informativo"  

### Compliance Médico

⚠️ **IMPORTANTE:**
- Não dê diagnósticos individuais
- Não substitua consulta médica
- Cite fontes científicas
- Use disclaimers apropriados

**Exemplo de disclaimer:**
```
⚠️ Este conteúdo é apenas informativo.
Consulte sempre um médico para diagnóstico e tratamento.
```

## 🤝 Contribuindo

Melhorias são bem-vindas! 

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é open-source sob a licença MIT.

## 🆘 Suporte

- **Issues:** Abra uma issue no GitHub
- **Email:** seu-email@example.com
- **Documentação:** Este README

## 🎯 Roadmap

### Versão 1.0 (Atual)
- ✅ Coleta de notícias RSS
- ✅ Tradução automática
- ✅ Geração de carrosséis
- ✅ Publicação no Instagram
- ✅ Agendamento inteligente

### Versão 1.1 (Próxima)
- 🔄 Suporte a TikTok
- 🔄 Analytics dashboard
- 🔄 IA para resumos melhores (GPT)
- 🔄 Geração de vídeos curtos

### Versão 2.0 (Futuro)
- 🔄 Interface web
- 🔄 Multi-contas
- 🔄 A/B testing automático
- 🔄 Resposta automática a comentários

## 📚 Recursos Adicionais

### Fontes de Notícias Médicas

- [PubMed](https://pubmed.ncbi.nlm.nih.gov/) - Base principal
- [SciELO](https://scielo.org/) - Artigos em português
- [The Lancet](https://www.thelancet.com/) - Jornal médico de prestígio
- [NEJM](https://www.nejm.org/) - New England Journal of Medicine

### Ferramentas de Design

- [Canva](https://www.canva.com/) - Templates prontos
- [Coolors](https://coolors.co/) - Paletas de cores
- [Font Squirrel](https://www.fontsquirrel.com/) - Fontes gratuitas

### Aprendizado

- [Instagram Best Practices](https://business.instagram.com/)
- [Medical Social Media Guide](https://www.ama-assn.org/)
- [Python Documentation](https://docs.python.org/)

---

**Desenvolvido com ❤️ para profissionais da saúde**

*Última atualização: Novembro 2024*
