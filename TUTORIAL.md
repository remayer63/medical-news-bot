# 📚 Tutorial Completo - Do Zero ao Bot Funcionando

Este tutorial te guiará passo a passo, mesmo se você nunca programou antes.

## 📋 O que você vai aprender

1. Como instalar Python
2. Como configurar o bot
3. Como fazer sua primeira publicação
4. Como manter o bot rodando 24/7
5. Dicas para maximizar engajamento

---

## 🚀 PARTE 1: Preparação do Ambiente

### Passo 1: Instale o Python

#### Windows

1. Acesse: https://www.python.org/downloads/
2. Baixe Python 3.11 (ou mais recente)
3. **IMPORTANTE:** Marque "Add Python to PATH"
4. Clique em "Install Now"
5. Aguarde instalação

**Verificar instalação:**
```cmd
python --version
```

Deve mostrar: `Python 3.11.x`

#### Mac

```bash
# Instale Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instale Python
brew install python@3.11
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.11 python3-pip python3-venv
```

### Passo 2: Baixe o Bot

#### Opção A: Com Git (Recomendado)

```bash
git clone https://github.com/seu-usuario/medical-news-bot.git
cd medical-news-bot
```

#### Opção B: Download Manual

1. Baixe o ZIP do GitHub
2. Extraia para uma pasta (ex: `C:\medical-bot`)
3. Abra terminal/CMD nessa pasta

---

## ⚙️ PARTE 2: Configuração

### Passo 3: Execute o Setup Automático

#### Linux/Mac

```bash
chmod +x setup.sh
bash setup.sh
```

#### Windows

```cmd
pip install -r requirements.txt
mkdir data logs generated_images
copy .env.example .env
```

### Passo 4: Configure Suas Credenciais

Abra o arquivo `.env` e edite:

```env
INSTAGRAM_USERNAME=seu_usuario_real
INSTAGRAM_PASSWORD=sua_senha_real

POSTS_PER_WEEK=4
MIN_IMPACT_SCORE=7
```

**⚠️ IMPORTANTE:**
- Use uma conta específica para o bot (não sua pessoal)
- Nunca compartilhe este arquivo
- Guarde um backup das credenciais

### Passo 5: Teste a Conexão

```bash
python main.py --stats
```

**Saída esperada:**
```
📊 Estatísticas da conta:
   Usuário: @seu_usuario
   Seguidores: 150
   Seguindo: 200
   Posts: 5
```

Se aparecer erro de login:
1. Verifique usuário/senha
2. Desative autenticação de dois fatores temporariamente
3. Tente fazer login pelo navegador antes

---

## 🎯 PARTE 3: Primeira Publicação

### Passo 6: Publicação Teste

```bash
python main.py --now
```

**O que acontece:**

1. 📰 Bot coleta notícias do PubMed
2. 🔍 Filtra as mais relevantes (score > 7)
3. 🌐 Traduz para português
4. 🎨 Gera carrossel (10 imagens)
5. 📤 Publica no Instagram

**Tempo estimado:** 2-5 minutos

### Passo 7: Verifique no Instagram

1. Abra Instagram no celular/navegador
2. Vá ao perfil do bot
3. Veja o carrossel publicado
4. Teste deslizar entre slides

**Checklist de qualidade:**
- ✅ Texto legível?
- ✅ Cores apropriadas?
- ✅ Informação correta?
- ✅ Link na legenda?

---

## 🔄 PARTE 4: Modo Automático

### Passo 8: Execute em Modo Agendado

```bash
python main.py
```

**O que acontece:**
- Bot fica rodando continuamente
- Publica automaticamente nos horários:
  - Terça, 13h
  - Quarta, 11h
  - Quinta, 15h
  - Segunda, 17h

**Como parar:**
- Pressione `Ctrl+C`

### Passo 9: Rodar 24/7 (Servidor)

#### Opção A: Screen (Linux/Mac)

```bash
# Inicia sessão
screen -S medbot

# Dentro do screen, execute:
python main.py

# Saia sem parar (mantém rodando)
# Pressione: Ctrl+A depois D

# Para voltar:
screen -r medbot
```

#### Opção B: nohup (Linux/Mac)

```bash
nohup python main.py > bot.log 2>&1 &

# Verifica se está rodando
ps aux | grep main.py

# Ver logs
tail -f bot.log
```

#### Opção C: Serviço systemd (Linux - Avançado)

Crie `/etc/systemd/system/medbot.service`:

```ini
[Unit]
Description=Medical News Bot
After=network.target

[Service]
Type=simple
User=seu_usuario
WorkingDirectory=/caminho/para/medical-news-bot
ExecStart=/caminho/para/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable medbot
sudo systemctl start medbot
sudo systemctl status medbot
```

#### Opção D: Windows (Task Scheduler)

1. Abra "Agendador de Tarefas"
2. Criar Tarefa Básica
3. Nome: "Medical News Bot"
4. Acionador: "Quando o computador iniciar"
5. Ação: "Iniciar programa"
6. Programa: `C:\Python311\python.exe`
7. Argumentos: `C:\medical-bot\main.py`
8. OK

---

## 🎨 PARTE 5: Personalização

### Mudar Cores

Edite `config.py`, linha ~80:

```python
'colors': {
    'primary': '#2C5F7C',      # Mude para sua cor
    'secondary': '#4A90A4',
    'accent': '#E74C3C',
    'background': '#F8F9FA',
    'text': '#2C3E50',
}
```

**Ferramentas para escolher cores:**
- https://coolors.co/
- https://colorhunt.co/

### Adicionar Logo

1. Salve logo como `logo.png` (1000x1000 px)
2. Edite `carousel_generator.py`
3. Adicione no slide de capa:

```python
# No método create_cover_slide, adicione:
logo = Image.open('logo.png')
logo = logo.resize((200, 200))
img.paste(logo, (440, 100), logo)
```

### Mudar Hashtags

Edite `config.py`, linha ~120:

```python
HASHTAGS = {
    'cardiologia': ['#cardiologia', '#suas', '#hashtags'],
    'diabetes': ['#diabetes', '#suas', '#hashtags'],
    'geral': ['#medicina', '#saude', '#suas', '#hashtags']
}
```

---

## 📊 PARTE 6: Maximizando Engajamento

### Estratégias Comprovadas

#### 1. Poste Consistentemente
- ✅ 4 vezes por semana (mínimo)
- ✅ Sempre nos mesmos horários
- ❌ Não fique semanas sem postar

#### 2. Use Stories
```bash
# Adicione no main.py para stories automáticos:
# (Requer implementação adicional)
```

#### 3. Responda Comentários
- Primeiras 2 horas são críticas
- Use respostas personalizadas
- Faça perguntas de volta

#### 4. Analise Métricas

Crie `analytics.py`:

```python
from instagram_publisher import InstagramPublisher

pub = InstagramPublisher()
pub.login()

# Ver insights do último post
media = pub.client.user_medias(pub.client.user_id, 1)[0]
insights = pub.client.insights_media(media.pk)

print(f"Alcance: {insights.reach}")
print(f"Impressões: {insights.impressions}")
print(f"Engajamento: {insights.engagement}")
```

#### 5. A/B Testing

Teste diferentes:
- Horários de postagem
- Estilos de imagem
- Tamanhos de texto
- Cores

### Métricas para Acompanhar

| Métrica | Meta | Como Melhorar |
|---------|------|---------------|
| Taxa de Engajamento | 3-5% | Poste conteúdo mais relevante |
| Crescimento Mensal | 5-10% | Use hashtags estratégicas |
| Alcance | 20-30% | Poste nos melhores horários |
| Salvamentos | Alto | Crie conteúdo "guardável" |

---

## 🐛 PARTE 7: Problemas Comuns

### "ModuleNotFoundError"

```bash
# Reinstale dependências
pip install -r requirements.txt --force-reinstall
```

### "Login Failed"

1. Verifique credenciais no `.env`
2. Tente login manual no Instagram
3. Desative 2FA temporariamente
4. Use senha de aplicativo se 2FA estiver ativo

### "Rate Limit Exceeded"

Instagram limita ações:
- Reduza frequência de posts
- Aguarde 24 horas
- Não use múltiplos bots na mesma conta

### Bot para sozinho

```bash
# Veja os logs
tail -f bot.log

# Verifique erros
grep "ERROR" bot.log

# Reinicie
pkill -f main.py
python main.py
```

### Imagens não aparecem

```bash
# Teste geração de imagem
python -c "
from carousel_generator import CarouselGenerator
gen = CarouselGenerator()
print('✅ Gerador OK')
"
```

---

## 🎓 PARTE 8: Próximos Passos

### Nível Intermediário

1. **Adicione Analytics Dashboard**
   - Use Streamlit para visualizar métricas
   - Gráficos de crescimento
   - Análise de hashtags

2. **Integre ChatGPT**
   - Resumos mais inteligentes
   - Legendas criativas
   - Resposta a comentários

3. **Multi-plataforma**
   - Publique também no TikTok
   - Sincronize com Facebook
   - LinkedIn para conteúdo profissional

### Nível Avançado

1. **Machine Learning**
   - Preveja melhores horários
   - Classifique relevância automaticamente
   - Detecte tendências

2. **Automação Completa**
   - Resposta automática a DMs
   - Análise de sentimento em comentários
   - Geração de vídeos curtos

3. **Monetização**
   - Afiliados de produtos médicos
   - Consultoria
   - Cursos online

---

## 📞 Suporte

### Canais de Ajuda

- 📧 Email: suporte@example.com
- 💬 Discord: [Link do servidor]
- 🐛 GitHub Issues: [Link dos issues]
- 📚 Wiki: [Link da wiki]

### Comunidade

Junte-se à comunidade:
- Compartilhe resultados
- Troque experiências
- Sugira melhorias

---

## ✅ Checklist Final

Antes de deixar rodando em produção:

- [ ] Python instalado e testado
- [ ] Dependências instaladas
- [ ] Arquivo .env configurado
- [ ] Login no Instagram funcionando
- [ ] Publicação teste realizada com sucesso
- [ ] Cores e design ajustados
- [ ] Hashtags personalizadas
- [ ] Bot rodando em modo agendado
- [ ] Servidor/computador configurado para rodar 24/7
- [ ] Backup das configurações feito
- [ ] Logs sendo monitorados

---

**🎉 Parabéns! Seu bot está pronto para funcionar!**

Se seguiu todos os passos, você agora tem um bot totalmente funcional que:
- ✅ Coleta notícias médicas automaticamente
- ✅ Traduz e formata conteúdo
- ✅ Cria carrosséis profissionais
- ✅ Publica nos melhores horários
- ✅ Roda 24/7 sem intervenção

**Próximo desafio:** Alcançar 10.000 seguidores! 🚀

---

*Última atualização: Novembro 2024*
*Versão do tutorial: 1.0*
