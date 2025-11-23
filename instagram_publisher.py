"""
Módulo para publicação automática no Instagram
"""
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import os
import time
from datetime import datetime
from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD

class InstagramPublisher:
    def __init__(self):
        self.client = Client()
        self.session_file = './data/instagram_session.json'
        self.is_logged_in = False
    
    def login(self):
        """Faz login no Instagram"""
        try:
            # Tenta carregar sessão salva
            if os.path.exists(self.session_file):
                print("📱 Carregando sessão salva...")
                self.client.load_settings(self.session_file)
                self.client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
                
                try:
                    self.client.get_timeline_feed()
                    print("✅ Login bem-sucedido com sessão salva!")
                    self.is_logged_in = True
                    return True
                except LoginRequired:
                    print("⚠️  Sessão expirada, fazendo novo login...")
            
            # Faz novo login
            print("🔐 Fazendo login no Instagram...")
            self.client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            
            # Salva sessão
            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
            self.client.dump_settings(self.session_file)
            
            print("✅ Login realizado com sucesso!")
            self.is_logged_in = True
            return True
            
        except Exception as e:
            print(f"❌ Erro ao fazer login: {str(e)}")
            print("⚠️  Verifique suas credenciais no arquivo .env")
            return False
    
    def post_carousel(self, image_paths, caption):
        """
        Publica carrossel no Instagram
        
        Args:
            image_paths: Lista de caminhos das imagens
            caption: Legenda do post
        
        Returns:
            dict: Informações do post ou None se falhar
        """
        if not self.is_logged_in:
            print("❌ Não está logado no Instagram")
            return None
        
        try:
            print(f"📤 Publicando carrossel com {len(image_paths)} imagens...")
            
            # Limita a 10 imagens (máximo do Instagram)
            image_paths = image_paths[:10]
            
            # Publica carrossel
            media = self.client.album_upload(
                paths=image_paths,
                caption=caption
            )
            
            print(f"✅ Carrossel publicado com sucesso!")
            print(f"   ID: {media.pk}")
            print(f"   Link: https://www.instagram.com/p/{media.code}/")
            
            return {
                'id': media.pk,
                'code': media.code,
                'url': f"https://www.instagram.com/p/{media.code}/",
                'posted_at': datetime.now().isoformat(),
                'image_count': len(image_paths)
            }
            
        except Exception as e:
            print(f"❌ Erro ao publicar carrossel: {str(e)}")
            return None
    
    def post_story(self, image_path, caption=""):
        """Publica nos Stories"""
        if not self.is_logged_in:
            print("❌ Não está logado no Instagram")
            return None
        
        try:
            print("📤 Publicando story...")
            
            story = self.client.photo_upload_to_story(
                path=image_path,
                caption=caption
            )
            
            print(f"✅ Story publicado com sucesso!")
            return {
                'id': story.pk,
                'posted_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Erro ao publicar story: {str(e)}")
            return None
    
    def get_account_stats(self):
        """Retorna estatísticas da conta"""
        if not self.is_logged_in:
            return None
        
        try:
            user_info = self.client.user_info_by_username(INSTAGRAM_USERNAME)
            
            stats = {
                'followers': user_info.follower_count,
                'following': user_info.following_count,
                'posts': user_info.media_count,
                'username': user_info.username,
                'full_name': user_info.full_name
            }
            
            return stats
            
        except Exception as e:
            print(f"❌ Erro ao obter estatísticas: {str(e)}")
            return None
    
    def schedule_post(self, image_paths, caption, scheduled_time):
        """
        Agenda post para horário específico
        (Nota: Instagram não suporta agendamento nativo via API)
        Esta função apenas aguarda até o horário e posta
        """
        now = datetime.now()
        wait_seconds = (scheduled_time - now).total_seconds()
        
        if wait_seconds > 0:
            print(f"⏰ Post agendado para {scheduled_time.strftime('%d/%m/%Y %H:%M')}")
            print(f"   Aguardando {int(wait_seconds/60)} minutos...")
            time.sleep(wait_seconds)
        
        return self.post_carousel(image_paths, caption)


# Teste do publicador
if __name__ == "__main__":
    # Este é apenas um teste - não publicará nada sem as credenciais corretas
    
    publisher = InstagramPublisher()
    
    # Tenta fazer login
    if publisher.login():
        # Mostra estatísticas da conta
        stats = publisher.get_account_stats()
        if stats:
            print("\n📊 Estatísticas da conta:")
            print(f"   Usuário: @{stats['username']}")
            print(f"   Seguidores: {stats['followers']}")
            print(f"   Seguindo: {stats['following']}")
            print(f"   Posts: {stats['posts']}")
    else:
        print("\n⚠️  Configure suas credenciais no arquivo .env para testar a publicação")
        print("   Copie .env.example para .env e preencha os dados")
