# 🌐 Hospedagem Gratuita 24/7 para o Bot

Guia completo para manter seu bot rodando gratuitamente sem precisar deixar seu computador ligado.

---

## 🎯 Opções de Hospedagem Gratuita

### 1. 🟢 Render (RECOMENDADO)

**Vantagens:**
- ✅ Totalmente gratuito
- ✅ Deploy automático do GitHub
- ✅ SSL gratuito
- ✅ Logs e monitoramento
- ✅ Reinicialização automática

**Limites do plano gratuito:**
- 750 horas/mês (suficiente)
- App hiberna após 15 min de inatividade (ok para bot agendado)

#### Passo a Passo - Render

1. **Criar conta:**
   - Acesse: https://render.com
   - Cadastre-se com GitHub

2. **Preparar projeto:**
   
   Crie `render.yaml` na raiz:
   ```yaml
   services:
     - type: web
       name: medical-news-bot
       env: python
       buildCommand: "pip install -r requirements.txt"
       startCommand: "python main.py"
       envVars:
         - key: INSTAGRAM_USERNAME
           sync: false
         - key: INSTAGRAM_PASSWORD
           sync: false
   ```

   Adicione ao `requirements.txt`:
   ```
   gunicorn==21.2.0
   ```

3. **Deploy:**
   - New → Web Service
   - Connect GitHub repository
   - Configure environment variables
   - Deploy!

---

### 2. 🔵 Railway

**Vantagens:**
- ✅ $5 de crédito grátis/mês
- ✅ Interface simples
- ✅ Logs detalhados
- ✅ Variáveis de ambiente seguras

**Limites:**
- $5/mês gratuito
- Suficiente para bot leve

#### Passo a Passo - Railway

1. **Criar conta:**
   - Acesse: https://railway.app
   - Login com GitHub

2. **Deploy:**
   - New Project → Deploy from GitHub
   - Selecione repositório
   - Adicione variáveis de ambiente
   - Deploy automático

3. **Configure variáveis:**
   ```
   INSTAGRAM_USERNAME=seu_usuario
   INSTAGRAM_PASSWORD=sua_senha
   ```

---

### 3. 🟣 Fly.io

**Vantagens:**
- ✅ 3 VMs gratuitas
- ✅ 160GB tráfego/mês
- ✅ Bom para Python

#### Passo a Passo - Fly.io

1. **Instalar CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login e deploy:**
   ```bash
   fly auth login
   fly launch
   fly deploy
   ```

3. **Configurar secrets:**
   ```bash
   fly secrets set INSTAGRAM_USERNAME=seu_usuario
   fly secrets set INSTAGRAM_PASSWORD=sua_senha
   ```

---

### 4. 🟡 PythonAnywhere (Especializado em Python)

**Vantagens:**
- ✅ Focado em Python
- ✅ Fácil de usar
- ✅ Tarefas agendadas

**Limites gratuitos:**
- 1 app web
- Tarefas agendadas limitadas

#### Passo a Passo - PythonAnywhere

1. **Criar conta:**
   - https://www.pythonanywhere.com
   - Plano Beginner (gratuito)

2. **Upload de código:**
   - Files → Upload
   - Ou clone do GitHub

3. **Configurar tarefa agendada:**
   - Tasks → Create
   - Horário: Diário
   - Comando: `python3 /home/usuario/medical-news-bot/main.py --now`

---

### 5. ⚫ Heroku (Limitado)

**⚠️ Nota:** Heroku não tem mais plano gratuito desde 2022, mas incluído para referência.

**Alternativa:** Use Render ou Railway em vez do Heroku.

---

## 🔧 Configuração para Hospedagem

### Criar Procfile

Para Heroku/Railway/Render:

```
worker: python main.py
```

### Criar runtime.txt

```
python-3.11.5
```

### Ajustar main.py para Cloud

Adicione no início de `main.py`:

```python
import os

# Configuração para cloud
IS_CLOUD = os.getenv('IS_CLOUD', 'false').lower() == 'true'

if IS_CLOUD:
    # Ajusta timezone para horário de Brasília
    os.environ['TZ'] = 'America/Sao_Paulo'
    
    # Usa variáveis de ambiente
    from config import *
```

### Variáveis de Ambiente

**Obrigatórias:**
```
INSTAGRAM_USERNAME=seu_usuario
INSTAGRAM_PASSWORD=sua_senha
IS_CLOUD=true
```

**Opcionais:**
```
POSTS_PER_WEEK=4
MIN_IMPACT_SCORE=7
TZ=America/Sao_Paulo
```

---

## 🚀 Deploy Automático com GitHub

### 1. Criar Repositório GitHub

```bash
# Inicializa Git
git init

# Adiciona arquivos
git add .

# Commit
git commit -m "Initial commit"

# Cria repositório no GitHub e conecta
git remote add origin https://github.com/seu-usuario/medical-news-bot.git
git branch -M main
git push -u origin main
```

### 2. Configurar GitHub Actions (CI/CD)

Crie `.github/workflows/deploy.yml`:

```yaml
name: Deploy Bot

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 */6 * * *'  # Roda a cada 6 horas

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run bot
      env:
        INSTAGRAM_USERNAME: ${{ secrets.INSTAGRAM_USERNAME }}
        INSTAGRAM_PASSWORD: ${{ secrets.INSTAGRAM_PASSWORD }}
      run: |
        python main.py --now
```

**Configure secrets no GitHub:**
- Settings → Secrets → New repository secret
- Adicione `INSTAGRAM_USERNAME` e `INSTAGRAM_PASSWORD`

---

## 📊 Monitoramento

### 1. Logs

**Render:**
- Dashboard → Logs (tempo real)

**Railway:**
- Project → Deployments → Logs

**Fly.io:**
```bash
fly logs
```

### 2. Uptime Monitoring

Use **UptimeRobot** (gratuito):
1. Cadastre-se: https://uptimerobot.com
2. Add New Monitor
3. URL: seu-app.render.com/health (crie endpoint)
4. Receba alertas se bot cair

### 3. Health Check Endpoint

Adicione em `main.py`:

```python
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/health')
def health():
    return {'status': 'running', 'bot': 'medical-news'}

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# Inicia Flask em thread separada
threading.Thread(target=run_flask, daemon=True).start()
```

Adicione ao `requirements.txt`:
```
Flask==3.0.0
```

---

## 💾 Armazenamento de Dados

### Problema: Arquivos Temporários

Hospedagens gratuitas não mantêm arquivos entre deploys.

### Soluções:

#### 1. PostgreSQL (Render)

```bash
# Adicione ao requirements.txt
psycopg2-binary==2.9.9

# Conecte no dashboard Render
# Use DATABASE_URL do environment
```

#### 2. MongoDB Atlas (Gratuito)

```bash
# Adicione ao requirements.txt
pymongo==4.6.0

# Crie conta em mongodb.com
# Cluster gratuito: 512MB
```

#### 3. AWS S3 (Gratuito 12 meses)

```bash
# Adicione ao requirements.txt
boto3==1.34.0

# 5GB gratuito
```

#### 4. Supabase (PostgreSQL + Storage)

- 500MB database
- 1GB storage
- Gratuito para sempre

---

## 🔒 Segurança

### Boas Práticas

**NUNCA commite:**
- `.env` com credenciais
- `instagram_session.json`
- Logs com dados sensíveis

**Adicione ao .gitignore:**
```
.env
*.json
data/
logs/
generated_images/
```

**Use GitHub Secrets:**
- Nunca coloque senhas no código
- Use variáveis de ambiente
- Configure secrets no repositório

---

## 🔄 Rotina de Manutenção

### Semanal
- [ ] Verificar logs de erro
- [ ] Checar se bot postou
- [ ] Ver métricas de engajamento

### Mensal
- [ ] Atualizar dependências
- [ ] Revisar estratégia de conteúdo
- [ ] Backup de dados importantes

### Comandos Úteis

```bash
# Ver logs (Render)
render logs -f

# Reiniciar bot (Railway)
railway restart

# Status (Fly.io)
fly status

# Atualizar código
git add .
git commit -m "Update"
git push
```

---

## 💡 Dicas de Otimização

### 1. Reduzir Uso de Recursos

**Cache de RSS feeds:**
```python
import time
from functools import lru_cache

@lru_cache(maxsize=100)
def fetch_cached_news(url):
    return feedparser.parse(url)
```

### 2. Async para Múltiplas Requisições

```python
import asyncio
import aiohttp

async def fetch_all_news():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_news(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

### 3. Compressão de Imagens

```python
# Adicione em carousel_generator.py
img.save(filename, quality=85, optimize=True)  # Reduz tamanho
```

---

## 🆘 Troubleshooting

### Bot não posta

**1. Verificar logs:**
```bash
# Procure por erros
grep "ERROR" logs/bot.log
```

**2. Testar localmente:**
```bash
python main.py --now
```

**3. Verificar credenciais:**
- Instagram bloqueou?
- Senha mudou?
- 2FA ativado?

### Deploy falha

**1. Verificar requirements.txt:**
```bash
pip freeze > requirements.txt
```

**2. Testar build local:**
```bash
pip install -r requirements.txt
python main.py
```

**3. Ver logs de build:**
- Render/Railway dashboard

### Memória insuficiente

**Soluções:**
1. Limpar imagens antigas mais agressivamente
2. Processar posts um por vez
3. Usar hosting com mais RAM (considerar upgrade)

---

## 📈 Comparação de Plataformas

| Plataforma | Custo | RAM | Facilidade | Melhor Para |
|------------|-------|-----|------------|-------------|
| Render | Grátis | 512MB | ⭐⭐⭐⭐⭐ | Iniciantes |
| Railway | $5/mês* | 1GB | ⭐⭐⭐⭐ | Intermediário |
| Fly.io | Grátis | 256MB | ⭐⭐⭐ | Avançado |
| PythonAnywhere | Grátis | 512MB | ⭐⭐⭐⭐⭐ | Python puro |
| GitHub Actions | Grátis | 7GB | ⭐⭐⭐ | CI/CD |

*Tem créditos gratuitos

---

## ✅ Checklist de Deploy

- [ ] Código testado localmente
- [ ] `.gitignore` configurado
- [ ] Variáveis de ambiente definidas
- [ ] Procfile criado
- [ ] runtime.txt configurado
- [ ] requirements.txt atualizado
- [ ] GitHub repositório criado
- [ ] Plataforma escolhida
- [ ] Deploy realizado
- [ ] Logs verificados
- [ ] Primeiro post teste funcionou
- [ ] Monitoramento configurado
- [ ] Backups configurados

---

## 🎓 Recursos Adicionais

**Documentações:**
- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Fly.io Docs](https://fly.io/docs)

**Comunidades:**
- [r/selfhosted](https://reddit.com/r/selfhosted)
- [Dev.to](https://dev.to)
- Discord de cada plataforma

---

**🚀 Agora seu bot pode rodar 24/7 sem custo!**

Escolha uma plataforma acima e siga o tutorial. Em menos de 1 hora você terá o bot rodando na nuvem.

---

*Última atualização: Novembro 2024*
