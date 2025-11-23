"""
Script principal do Bot de Notícias Médicas para Instagram
"""
import schedule
import time
from datetime import datetime, timedelta
import sys
import os

from news_collector import NewsCollector
from carousel_generator import CarouselGenerator
from instagram_publisher import InstagramPublisher
from config import POSTING_SCHEDULE, MIN_IMPACT_SCORE

class MedicalNewsBot:
    def __init__(self):
        print("🤖 Inicializando Medical News Bot...")
        self.collector = NewsCollector()
        self.generator = CarouselGenerator()
        self.publisher = InstagramPublisher()
        
        # Tenta fazer login
        if not self.publisher.login():
            print("❌ Não foi possível fazer login no Instagram")
            print("   Configure suas credenciais no arquivo .env")
            sys.exit(1)
        
        print("✅ Bot inicializado com sucesso!\n")
    
    def process_and_post(self):
        """Processa notícias e publica no Instagram"""
        print(f"\n{'='*60}")
        print(f"🕐 Iniciando processamento: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # 1. Coleta notícias
        print("📰 Coletando notícias...")
        top_news = self.collector.get_top_news(
            min_score=MIN_IMPACT_SCORE,
            limit=1  # Pega apenas a melhor notícia
        )
        
        if not top_news:
            print("⚠️  Nenhuma notícia relevante encontrada neste momento")
            print(f"   Tentando novamente em {self.get_next_schedule()}\n")
            return
        
        news_item = top_news[0]
        print(f"✅ Notícia selecionada: {news_item['title'][:60]}...")
        print(f"   Categoria: {news_item['category']} | Score: {news_item['impact_score']}/10\n")
        
        # 2. Formata para carrossel
        print("📋 Formatando carrossel...")
        carousel_data = self.collector.format_for_carousel(news_item)
        print(f"   {len(carousel_data['slides'])} slides criados\n")
        
        # 3. Gera imagens
        print("🎨 Gerando imagens...")
        image_paths = self.generator.create_carousel(carousel_data)
        print(f"   {len(image_paths)} imagens geradas\n")
        
        # 4. Gera legenda
        print("✍️  Gerando legenda...")
        caption = self.generator.generate_caption(news_item, carousel_data)
        print(f"   Legenda: {len(caption)} caracteres\n")
        
        # 5. Publica no Instagram
        print("📤 Publicando no Instagram...")
        result = self.publisher.post_carousel(image_paths, caption)
        
        if result:
            print(f"\n🎉 Publicação concluída com sucesso!")
            print(f"   URL: {result['url']}")
            print(f"   ID: {result['id']}")
            
            # Marca como publicada
            self.collector.save_posted_news(news_item['id'])
            
            # Limpa imagens antigas (opcional)
            self.cleanup_old_images(image_paths)
            
            # Mostra estatísticas
            stats = self.publisher.get_account_stats()
            if stats:
                print(f"\n📊 Estatísticas atualizadas:")
                print(f"   Seguidores: {stats['followers']}")
                print(f"   Posts totais: {stats['posts']}")
        else:
            print("\n❌ Falha na publicação")
        
        print(f"\n⏰ Próxima publicação: {self.get_next_schedule()}")
        print(f"{'='*60}\n")
    
    def cleanup_old_images(self, keep_images):
        """Remove imagens antigas para economizar espaço"""
        from config import IMAGES_DIR
        
        try:
            for filename in os.listdir(IMAGES_DIR):
                filepath = os.path.join(IMAGES_DIR, filename)
                if filepath not in keep_images and filename.endswith('.jpg'):
                    os.remove(filepath)
            print("🧹 Imagens antigas removidas")
        except Exception as e:
            print(f"⚠️  Erro ao limpar imagens: {str(e)}")
    
    def get_next_schedule(self):
        """Retorna próximo horário agendado"""
        now = datetime.now()
        next_times = []
        
        for day, hour, minute in POSTING_SCHEDULE:
            # Calcula próxima ocorrência
            days_ahead = (day - now.weekday()) % 7
            if days_ahead == 0:
                # Mesmo dia - verifica se horário já passou
                scheduled_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                if scheduled_time <= now:
                    days_ahead = 7  # Próxima semana
            
            next_time = now + timedelta(days=days_ahead)
            next_time = next_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
            next_times.append(next_time)
        
        next_schedule = min(next_times)
        return next_schedule.strftime('%d/%m/%Y %H:%M')
    
    def setup_schedule(self):
        """Configura agendamento automático"""
        print("📅 Configurando agendamentos...")
        
        weekdays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        
        for day, hour, minute in POSTING_SCHEDULE:
            time_str = f"{hour:02d}:{minute:02d}"
            day_name = weekdays[day]
            
            # Mapeia dia da semana para função do schedule
            day_func = [
                schedule.every().monday,
                schedule.every().tuesday,
                schedule.every().wednesday,
                schedule.every().thursday,
                schedule.every().friday,
                schedule.every().saturday,
                schedule.every().sunday
            ][day]
            
            day_func.at(time_str).do(self.process_and_post)
            print(f"   ✅ {day_name} às {time_str}")
        
        print(f"\n⏰ Próxima publicação: {self.get_next_schedule()}\n")
    
    def run_now(self):
        """Executa imediatamente (para testes)"""
        print("🚀 Modo teste: Executando agora...\n")
        self.process_and_post()
    
    def run_scheduled(self):
        """Executa em modo agendado"""
        self.setup_schedule()
        
        print("🤖 Bot em execução (Ctrl+C para parar)...\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Verifica a cada minuto
        except KeyboardInterrupt:
            print("\n\n👋 Bot encerrado pelo usuário")
            sys.exit(0)


def main():
    """Função principal"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║           🏥 MEDICAL NEWS BOT - INSTAGRAM 📱              ║
    ║                                                           ║
    ║      Automação de Notícias Médicas em Carrossel         ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Verifica argumentos de linha de comando
    if len(sys.argv) > 1:
        if sys.argv[1] == '--now':
            # Modo teste: executa imediatamente
            bot = MedicalNewsBot()
            bot.run_now()
            return
        elif sys.argv[1] == '--stats':
            # Apenas mostra estatísticas
            bot = MedicalNewsBot()
            stats = bot.publisher.get_account_stats()
            if stats:
                print("\n📊 Estatísticas da Conta:")
                print(f"   Usuário: @{stats['username']}")
                print(f"   Nome: {stats['full_name']}")
                print(f"   Seguidores: {stats['followers']}")
                print(f"   Seguindo: {stats['following']}")
                print(f"   Posts: {stats['posts']}\n")
            return
        elif sys.argv[1] == '--help':
            print("""
Uso: python main.py [opção]

Opções:
  (nenhuma)    Executa em modo agendado (padrão)
  --now        Executa uma vez imediatamente (para testes)
  --stats      Mostra estatísticas da conta
  --help       Mostra esta mensagem
  
Exemplos:
  python main.py              # Roda em modo agendado
  python main.py --now        # Testa publicação agora
  python main.py --stats      # Vê estatísticas da conta
            """)
            return
    
    # Modo padrão: agendado
    bot = MedicalNewsBot()
    bot.run_scheduled()


if __name__ == "__main__":
    main()
