"""
Módulo para geração de imagens de carrossel
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
from config import CAROUSEL_SETTINGS, IMAGES_DIR, HASHTAGS
import textwrap

class CarouselGenerator:
    def __init__(self):
        self.width = CAROUSEL_SETTINGS['width']
        self.height = CAROUSEL_SETTINGS['height']
        self.colors = CAROUSEL_SETTINGS['colors']
        self.fonts = CAROUSEL_SETTINGS['fonts']
        
        # Cria diretório para imagens
        os.makedirs(IMAGES_DIR, exist_ok=True)
    
    def create_carousel(self, carousel_data):
        """Cria todas as imagens do carrossel"""
        image_paths = []
        
        for i, slide in enumerate(carousel_data['slides'], start=1):
            if slide['type'] == 'cover':
                img_path = self.create_cover_slide(slide, carousel_data, i)
            elif slide['type'] == 'content':
                img_path = self.create_content_slide(slide, carousel_data, i)
            elif slide['type'] == 'cta':
                img_path = self.create_cta_slide(slide, carousel_data, i)
            
            if img_path:
                image_paths.append(img_path)
        
        return image_paths
    
    def create_cover_slide(self, slide, carousel_data, slide_num):
        """Cria slide de capa"""
        img = Image.new('RGB', (self.width, self.height), self.colors['background'])
        draw = ImageDraw.Draw(img)
        
        # Barra superior decorativa
        draw.rectangle([(0, 0), (self.width, 200)], fill=self.colors['primary'])
        
        # Categoria
        category_y = 50
        category_text = f"📌 {slide['category']}"
        self.draw_text_centered(
            draw, category_text, category_y, 
            size=40, color='white', bold=True
        )
        
        # Título (centralizado e quebrado em linhas)
        title_y = 400
        title_lines = textwrap.wrap(slide['title'], width=30)
        
        for i, line in enumerate(title_lines[:4]):  # Máximo 4 linhas
            y_pos = title_y + (i * 80)
            self.draw_text_centered(
                draw, line, y_pos,
                size=self.fonts['size_title'], 
                color=self.colors['text'],
                bold=True
            )
        
        # Badge de relevância
        impact_y = self.height - 300
        impact_bg_coords = [
            (self.width//2 - 200, impact_y - 20),
            (self.width//2 + 200, impact_y + 50)
        ]
        draw.rounded_rectangle(
            impact_bg_coords, 
            radius=25,
            fill=self.colors['accent']
        )
        self.draw_text_centered(
            draw, slide['impact'], impact_y,
            size=35, color='white', bold=True
        )
        
        # Indicador de slides
        self.draw_slide_indicator(draw, slide_num, len(carousel_data['slides']))
        
        # Salva imagem
        filename = f"{IMAGES_DIR}/slide_{carousel_data['id']}_{slide_num:02d}.jpg"
        img.save(filename, quality=95, optimize=True)
        return filename
    
    def create_content_slide(self, slide, carousel_data, slide_num):
        """Cria slide de conteúdo"""
        img = Image.new('RGB', (self.width, self.height), self.colors['background'])
        draw = ImageDraw.Draw(img)
        
        # Cabeçalho simples
        draw.rectangle([(0, 0), (self.width, 150)], fill=self.colors['secondary'])
        
        header_text = f"📄 Slide {slide['number']}"
        self.draw_text_centered(
            draw, header_text, 60,
            size=45, color='white', bold=True
        )
        
        # Conteúdo de texto
        text_y = 250
        margin = 80
        max_width = self.width - (2 * margin)
        
        # Quebra o texto em linhas
        text_lines = self.wrap_text_to_width(
            slide['text'], 
            max_width, 
            size=self.fonts['size_body']
        )
        
        for i, line in enumerate(text_lines):
            y_pos = text_y + (i * 60)
            if y_pos < self.height - 200:  # Garante que não sai da imagem
                draw.text(
                    (margin, y_pos),
                    line,
                    fill=self.colors['text'],
                    font=self.get_font(size=self.fonts['size_body'])
                )
        
        # Indicador de slides
        self.draw_slide_indicator(draw, slide_num, len(carousel_data['slides']))
        
        # Salva imagem
        filename = f"{IMAGES_DIR}/slide_{carousel_data['id']}_{slide_num:02d}.jpg"
        img.save(filename, quality=95, optimize=True)
        return filename
    
    def create_cta_slide(self, slide, carousel_data, slide_num):
        """Cria slide de chamada para ação (CTA)"""
        img = Image.new('RGB', (self.width, self.height), self.colors['primary'])
        draw = ImageDraw.Draw(img)
        
        # Gradiente simulado com retângulos
        for i in range(10):
            alpha = int(255 * (1 - i/10))
            y_start = i * (self.height // 10)
            y_end = (i + 1) * (self.height // 10)
            # Usa tom mais claro progressivamente
            draw.rectangle(
                [(0, y_start), (self.width, y_end)],
                fill=self.colors['primary']
            )
        
        # Ícone/Emoji grande
        emoji_y = 300
        self.draw_text_centered(
            draw, "🔬", emoji_y,
            size=120, color='white'
        )
        
        # Texto CTA
        cta_y = 550
        self.draw_text_centered(
            draw, slide['text'], cta_y,
            size=55, color='white', bold=True
        )
        
        # Link (encurtado visualmente)
        link_y = 700
        link_display = "🔗 Link na bio ou DM"
        self.draw_text_centered(
            draw, link_display, link_y,
            size=35, color='white'
        )
        
        # Fonte
        source_y = 900
        source_text = f"Fonte: {slide['source']}"
        self.draw_text_centered(
            draw, source_text, source_y,
            size=28, color='white'
        )
        
        # Call to action adicional
        cta2_y = 1100
        self.draw_text_centered(
            draw, "💬 Comente sua opinião!", cta2_y,
            size=38, color='white', bold=True
        )
        
        # Indicador de slides
        self.draw_slide_indicator(draw, slide_num, len(carousel_data['slides']), color='white')
        
        # Salva imagem
        filename = f"{IMAGES_DIR}/slide_{carousel_data['id']}_{slide_num:02d}.jpg"
        img.save(filename, quality=95, optimize=True)
        return filename
    
    def draw_text_centered(self, draw, text, y, size=40, color='black', bold=False):
        """Desenha texto centralizado horizontalmente"""
        font = self.get_font(size=size, bold=bold)
        
        # Calcula largura do texto
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        
        x = (self.width - text_width) // 2
        draw.text((x, y), text, fill=color, font=font)
    
    def draw_slide_indicator(self, draw, current, total, color=None):
        """Desenha indicador de slide (bolinhas)"""
        if color is None:
            color = self.colors['text']
        
        indicator_y = self.height - 80
        dot_radius = 8
        dot_spacing = 30
        total_width = (total * dot_spacing)
        start_x = (self.width - total_width) // 2
        
        for i in range(1, total + 1):
            x = start_x + (i * dot_spacing)
            
            if i == current:
                # Bolinha preenchida (slide atual)
                draw.ellipse(
                    [(x - dot_radius, indicator_y - dot_radius),
                     (x + dot_radius, indicator_y + dot_radius)],
                    fill=color
                )
            else:
                # Bolinha vazia
                draw.ellipse(
                    [(x - dot_radius, indicator_y - dot_radius),
                     (x + dot_radius, indicator_y + dot_radius)],
                    outline=color,
                    width=2
                )
    
    def get_font(self, size=40, bold=False):
        """Retorna fonte (usa padrão se personalizada não disponível)"""
        try:
            # Tenta carregar fonte personalizada
            if bold:
                return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
            else:
                return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except:
            # Fallback para fonte padrão
            return ImageFont.load_default()
    
    def wrap_text_to_width(self, text, max_width, size=40):
        """Quebra texto para caber na largura especificada"""
        font = self.get_font(size=size)
        
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            
            # Cria imagem temporária para medir texto
            temp_img = Image.new('RGB', (1, 1))
            temp_draw = ImageDraw.Draw(temp_img)
            bbox = temp_draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def generate_caption(self, news_item, carousel_data):
        """Gera legenda para o post"""
        
        # Resumo curto
        caption = f"📰 {news_item['title']}\n\n"
        caption += f"🔬 {news_item['summary'][:200]}...\n\n"
        
        # CTA
        caption += "👉 Deslize para ler mais detalhes!\n"
        caption += "💬 O que você achou dessa notícia?\n\n"
        
        # Hashtags baseadas na categoria
        category_hashtags = HASHTAGS.get(carousel_data['category'], [])
        general_hashtags = HASHTAGS['geral']
        
        all_hashtags = category_hashtags[:4] + general_hashtags[:6]
        caption += ' '.join(all_hashtags)
        
        # Link (Instagram não permite clique, mas fica na bio)
        caption += f"\n\n🔗 Link completo: {news_item['link']}"
        
        return caption


# Teste do gerador
if __name__ == "__main__":
    # Dados de teste
    test_carousel = {
        'id': 'test123',
        'category': 'cardiologia',
        'impact_score': 9,
        'slides': [
            {
                'type': 'cover',
                'title': 'Nova Pesquisa Revela Prevenção para Doenças Cardiovasculares',
                'category': 'CARDIOLOGIA',
                'impact': 'Relevância: 9/10'
            },
            {
                'type': 'content',
                'number': 2,
                'text': 'Estudo publicado no Journal of Cardiology demonstra que a combinação de exercícios aeróbicos moderados com dieta mediterrânea pode reduzir em até 40% o risco de doenças cardiovasculares em pacientes com hipertensão.'
            },
            {
                'type': 'content',
                'number': 3,
                'text': 'A pesquisa acompanhou 2.500 pacientes durante 5 anos e mostrou resultados consistentes em diferentes grupos demográficos.'
            },
            {
                'type': 'cta',
                'text': 'Leia o artigo completo',
                'link': 'https://example.com',
                'source': 'PubMed Cardiology'
            }
        ]
    }
    
    generator = CarouselGenerator()
    images = generator.create_carousel(test_carousel)
    
    print(f"✅ Carrossel gerado com {len(images)} imagens:")
    for img in images:
        print(f"   - {img}")
