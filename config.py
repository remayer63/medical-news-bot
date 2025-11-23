"""
Configurações do Bot de Notícias Médicas
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ==================== CREDENCIAIS ====================
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# ==================== FONTES DE NOTÍCIAS (RSS FEEDS) ====================
NEWS_SOURCES = {
    'pubmed_cardiology': {
        'url': 'https://pubmed.ncbi.nlm.nih.gov/rss/search/1P9cPSIHAJhZJAhgHfYSEq2Iq4Jg1XcxjCEgv80Tuk8CRVh8_u/?limit=15&utm_campaign=pubmed-2&fc=20210806090202',
        'topics': ['cardiologia', 'doenças cardiovasculares'],
        'lang': 'en'
    },
    'pubmed_diabetes': {
        'url': 'https://pubmed.ncbi.nlm.nih.gov/rss/search/1C8ixB7MmYaLgODNPMY-ydYtL9T-7tMCE2nFBXPuqVcK_Q6KNj/?limit=15&utm_campaign=pubmed-2&fc=20210806090202',
        'topics': ['diabetes mellitus', 'diabetes tipo 2'],
        'lang': 'en'
    },
    'pubmed_hypertension': {
        'url': 'https://pubmed.ncbi.nlm.nih.gov/rss/search/1z7YkJmXHgL5V6cImzJQzFKvvLCq4HqCyvYPwvKJYzK7gCv4Uz/?limit=15&utm_campaign=pubmed-2&fc=20210806090202',
        'topics': ['hipertensão arterial', 'pressão alta'],
        'lang': 'en'
    },
    'pubmed_obesity': {
        'url': 'https://pubmed.ncbi.nlm.nih.gov/rss/search/18t3nKVe3qPHzYYG8GtlFXR2qV_eXhJYy6Pj0XqCQ7VqEQcXJT/?limit=15&utm_campaign=pubmed-2&fc=20210806090202',
        'topics': ['obesidade', 'sobrepeso'],
        'lang': 'en'
    },
    'pubmed_liver': {
        'url': 'https://pubmed.ncbi.nlm.nih.gov/rss/search/1HK-R9LqJ4vZqYx_VqE1XYzF_wVGqLqCxVqE1qVqE1XY/?limit=15&utm_campaign=pubmed-2&fc=20210806090202',
        'topics': ['doença hepática esteatótica', 'esteatose hepática', 'fígado gorduroso'],
        'lang': 'en'
    },
    # Fontes brasileiras (RSS genéricos - você pode personalizar)
    'scielo_brazil': {
        'url': 'https://www.scielo.br/rss.php?pid=0066-782X',  # Arquivos Brasileiros de Cardiologia
        'topics': ['cardiologia brasileira'],
        'lang': 'pt'
    }
}

# ==================== TÓPICOS MÉDICOS ====================
MEDICAL_TOPICS = [
    'cardiologia',
    'hipertensão arterial sistêmica',
    'obesidade',
    'diabetes mellitus',
    'doença hepática esteatótica',
    'síndrome metabólica',
    'prevenção cardiovascular'
]

# ==================== HORÁRIOS DE POSTAGEM ====================
# Formato: (dia_da_semana, hora, minuto)
# 0 = Segunda, 1 = Terça, 2 = Quarta, 3 = Quinta, 4 = Sexta, 5 = Sábado, 6 = Domingo
POSTING_SCHEDULE = [
    (1, 13, 0),   # Terça, 13h - MELHOR HORÁRIO
    (2, 11, 0),   # Quarta, 11h
    (3, 15, 0),   # Quinta, 15h
    (0, 17, 0),   # Segunda, 17h
]

# ==================== CONFIGURAÇÕES DE DESIGN ====================
CAROUSEL_SETTINGS = {
    'width': 1080,
    'height': 1350,  # Proporção 4:5 (ideal para Instagram)
    'slides': 10,     # Máximo de 10 slides por carrossel
    'colors': {
        'primary': '#2C5F7C',      # Azul médico
        'secondary': '#4A90A4',    # Azul claro
        'accent': '#E74C3C',       # Vermelho para alertas
        'background': '#F8F9FA',   # Branco suave
        'text': '#2C3E50',         # Cinza escuro
    },
    'fonts': {
        'title': 'Arial Bold',
        'body': 'Arial',
        'size_title': 60,
        'size_body': 40,
        'size_small': 30,
    }
}

# ==================== CRITÉRIOS DE IMPACTO ====================
IMPACT_KEYWORDS = {
    'high': ['breakthrough', 'descoberta', 'revolucionário', 'primeiro', 'novo tratamento', 
             'cura', 'previne', 'reduz risco', 'metanálise', 'ensaio clínico randomizado'],
    'medium': ['estudo', 'pesquisa', 'associação', 'correlação', 'evidência', 
               'recomendação', 'diretriz', 'consenso'],
    'low': ['revisão', 'relato de caso', 'observacional', 'preliminar']
}

# Score mínimo para publicação (0-10)
MIN_IMPACT_SCORE = 5

# ==================== HASHTAGS ====================
HASHTAGS = {
    'cardiologia': ['#cardiologia', '#saúdecardiovascular', '#coração', '#cardiologista'],
    'hipertensão': ['#hipertensao', '#pressaoalta', '#saúdecardiovascular'],
    'diabetes': ['#diabetes', '#diabetesmelito', '#glicemia', '#insulina'],
    'obesidade': ['#obesidade', '#emagrecimento', '#saúde', '#nutrição'],
    'fígado': ['#fígado', '#esteatosehepática', '#saúdehepática'],
    'geral': ['#medicina', '#saúde', '#prevencao', '#bemestar', '#medicinadequalidade', 
              '#educacaoemsaude', '#saúdepública', '#ciênciamedica']
}

# ==================== CONFIGURAÇÕES DE API ====================
# Usando APIs gratuitas para análise de texto e tradução
TRANSLATION_SERVICE = 'deep-translator'  # Gratuito e ilimitado

# ==================== LOGS E ARMAZENAMENTO ====================
DATA_DIR = './data'
LOGS_DIR = './logs'
IMAGES_DIR = './generated_images'
POSTED_NEWS_FILE = './data/posted_news.json'
