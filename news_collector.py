"""
Módulo para coleta e análise de notícias médicas
"""
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os
from deep_translator import GoogleTranslator
from langdetect import detect
import re
from config import *

class NewsCollector:
    def __init__(self):
        self.translator = GoogleTranslator(source='auto', target='pt')
        self.posted_news = self.load_posted_news()
    
    def load_posted_news(self):
        """Carrega histórico de notícias já publicadas"""
        if os.path.exists(POSTED_NEWS_FILE):
            with open(POSTED_NEWS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_posted_news(self, news_id):
        """Salva ID de notícia publicada"""
        self.posted_news.append({
            'id': news_id,
            'posted_at': datetime.now().isoformat()
        })
        os.makedirs(os.path.dirname(POSTED_NEWS_FILE), exist_ok=True)
        with open(POSTED_NEWS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.posted_news, f, indent=2, ensure_ascii=False)
    
    def fetch_news_from_sources(self):
        """Coleta notícias de todas as fontes configuradas"""
        all_news = []
        
        for source_name, source_config in NEWS_SOURCES.items():
            try:
                print(f"📰 Coletando de {source_name}...")
                feed = feedparser.parse(source_config['url'])
                
                for entry in feed.entries[:15]:  # Limita a 15 mais recentes
                    news_item = self.process_entry(entry, source_config)
                    if news_item and not self.is_already_posted(news_item['id']):
                        all_news.append(news_item)
                        
            except Exception as e:
                print(f"❌ Erro ao coletar de {source_name}: {str(e)}")
                continue
        
        return all_news
    
    def process_entry(self, entry, source_config):
        """Processa uma entrada de feed RSS"""
        try:
            # Extrai informações básicas
            title = entry.get('title', '')
            summary = entry.get('summary', entry.get('description', ''))
            link = entry.get('link', '')
            published = entry.get('published', '')
            
            # Remove tags HTML do resumo
            summary_clean = BeautifulSoup(summary, 'html.parser').get_text()
            
            # Detecta idioma e traduz se necessário
            if source_config['lang'] == 'en':
                try:
                    title_pt = self.translator.translate(title)
                    summary_pt = self.translator.translate(summary_clean[:500])  # Limita tamanho
                except:
                    title_pt = title
                    summary_pt = summary_clean
            else:
                title_pt = title
                summary_pt = summary_clean
            
            # Calcula score de impacto
            impact_score = self.calculate_impact_score(title + ' ' + summary_clean)
            
            # Determina categoria
            category = self.determine_category(title_pt + ' ' + summary_pt)
            
            news_item = {
                'id': self.generate_id(link),
                'title': title_pt,
                'summary': summary_pt,
                'link': link,
                'published': published,
                'source': source_config['topics'][0],
                'category': category,
                'impact_score': impact_score,
                'collected_at': datetime.now().isoformat()
            }
            
            return news_item
            
        except Exception as e:
            print(f"❌ Erro ao processar entrada: {str(e)}")
            return None
    
    def generate_id(self, link):
        """Gera ID único para a notícia"""
        return str(hash(link))
    
    def is_already_posted(self, news_id):
        """Verifica se a notícia já foi publicada"""
        return any(item['id'] == news_id for item in self.posted_news)
    
    def calculate_impact_score(self, text):
        """
        Calcula score de impacto da notícia (0-10)
        Baseado em palavras-chave de relevância científica
        """
        text_lower = text.lower()
        score = 5  # Score base
        
        # Pontos por palavras de alto impacto
        for keyword in IMPACT_KEYWORDS['high']:
            if keyword.lower() in text_lower:
                score += 2
        
        # Pontos por palavras de médio impacto
        for keyword in IMPACT_KEYWORDS['medium']:
            if keyword.lower() in text_lower:
                score += 1
        
        # Remove pontos por palavras de baixo impacto
        for keyword in IMPACT_KEYWORDS['low']:
            if keyword.lower() in text_lower:
                score -= 1
        
        # Normaliza entre 0 e 10
        return min(max(score, 0), 10)
    
    def determine_category(self, text):
        """Determina a categoria médica da notícia"""
        text_lower = text.lower()
        
        categories_keywords = {
            'cardiologia': ['coração', 'cardíaco', 'cardiovascular', 'infarto', 'cardiopatia'],
            'hipertensão': ['hipertensão', 'pressão alta', 'hipertensivo'],
            'diabetes': ['diabetes', 'glicemia', 'insulina', 'diabético'],
            'obesidade': ['obesidade', 'obeso', 'sobrepeso', 'IMC', 'peso'],
            'fígado': ['fígado', 'hepática', 'hepatite', 'esteatose', 'cirrose']
        }
        
        for category, keywords in categories_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return category
        
        return 'geral'
    
    def get_top_news(self, min_score=MIN_IMPACT_SCORE, limit=10):
        """Retorna as notícias mais impactantes"""
        all_news = self.fetch_news_from_sources()
        
        # Filtra por score mínimo
        filtered_news = [n for n in all_news if n['impact_score'] >= min_score]
        
        # Ordena por impacto (decrescente) e data (recente primeiro)
        sorted_news = sorted(
            filtered_news, 
            key=lambda x: (x['impact_score'], x['collected_at']),
            reverse=True
        )
        
        return sorted_news[:limit]
    
    def format_for_carousel(self, news_item):
        """Formata notícia para estrutura de carrossel"""
        
        # Divide o resumo em partes menores para múltiplos slides
        summary_parts = self.split_text(news_item['summary'], max_chars=300)
        
        carousel_data = {
            'id': news_item['id'],
            'category': news_item['category'],
            'impact_score': news_item['impact_score'],
            'slides': []
        }
        
        # Slide 1: Título e categoria
        carousel_data['slides'].append({
            'type': 'cover',
            'title': news_item['title'],
            'category': news_item['category'].upper(),
            'impact': f"Relevância: {news_item['impact_score']}/10"
        })
        
        # Slides 2-N: Conteúdo dividido
        for i, part in enumerate(summary_parts, start=2):
            carousel_data['slides'].append({
                'type': 'content',
                'number': i,
                'text': part
            })
        
        # Último slide: CTA e fonte
        carousel_data['slides'].append({
            'type': 'cta',
            'text': 'Leia o artigo completo',
            'link': news_item['link'],
            'source': news_item['source']
        })
        
        return carousel_data
    
    def split_text(self, text, max_chars=300):
        """Divide texto em partes menores respeitando sentenças"""
        sentences = re.split(r'[.!?]\s+', text)
        parts = []
        current_part = ""
        
        for sentence in sentences:
            if len(current_part) + len(sentence) < max_chars:
                current_part += sentence + ". "
            else:
                if current_part:
                    parts.append(current_part.strip())
                current_part = sentence + ". "
        
        if current_part:
            parts.append(current_part.strip())
        
        return parts[:8]  # Limita a 8 slides de conteúdo


# Exemplo de uso
if __name__ == "__main__":
    collector = NewsCollector()
    top_news = collector.get_top_news(limit=5)
    
    print(f"\n📊 Encontradas {len(top_news)} notícias relevantes:\n")
    
    for news in top_news:
        print(f"📰 {news['title']}")
        print(f"   Categoria: {news['category']} | Impacto: {news['impact_score']}/10")
        print(f"   Link: {news['link']}\n")
