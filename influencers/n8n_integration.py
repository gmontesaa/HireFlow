import requests
import json
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

class N8NIntegration:
    def __init__(self):
        self.base_url = getattr(settings, 'N8N_BASE_URL', 'http://localhost:5678')
        self.webhook_token = getattr(settings, 'N8N_WEBHOOK_TOKEN', 'your-webhook-token')

    def calculate_engagement_rate(self, platform, username, posts_data):
        """
        Envía datos a n8n para calcular la tasa de engagement
        """
        webhook_url = f"{self.base_url}/webhook/{self.webhook_token}"
        
        data = {
            'platform': platform,
            'username': username,
            'posts_data': posts_data
        }
        
        try:
            response = requests.post(webhook_url, json=data)
            response.raise_for_status()
            return response.json().get('engagement_rate', 0.0)
        except Exception as e:
            print(f"Error al calcular engagement rate: {str(e)}")
            return 0.0

    def update_influencer_metrics(self, influencer_id, metrics):
        """
        Envía métricas actualizadas a n8n para procesamiento
        """
        webhook_url = f"{self.base_url}/webhook/update-metrics/{self.webhook_token}"
        
        data = {
            'influencer_id': influencer_id,
            'metrics': metrics
        }
        
        try:
            response = requests.post(webhook_url, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error al actualizar métricas: {str(e)}")
            return None

    def get_campaign_analytics(self, campaign_id):
        """
        Obtiene análisis detallado de la campaña desde n8n
        """
        webhook_url = f"{self.base_url}/webhook/campaign-analytics/{self.webhook_token}"
        
        data = {
            'campaign_id': campaign_id
        }
        
        try:
            response = requests.post(webhook_url, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error al obtener análisis de campaña: {str(e)}")
            return None

    def send_to_hireflow_review(self, campaign_influencer):
        """
        Envía los datos del influencer a Hireflow para revisión
        """
        webhook_url = f"{self.base_url}/webhook/hireflow-review/{self.webhook_token}"
        
        data = {
            'campaign_id': campaign_influencer.campaign.id,
            'campaign_name': campaign_influencer.campaign.name,
            'influencer_id': campaign_influencer.influencer.id,
            'influencer_name': campaign_influencer.influencer.name,
            'influencer_username': campaign_influencer.influencer.username,
            'platform': campaign_influencer.influencer.platform,
            'followers': campaign_influencer.influencer.followers,
            'engagement_rate': campaign_influencer.influencer.engagement_rate,
            'price_per_post': str(campaign_influencer.influencer.price_per_post)
        }
        
        try:
            response = requests.post(webhook_url, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error al enviar a revisión de Hireflow: {str(e)}")
            return None

    def send_message_to_influencer(self, campaign_influencer):
        """
        Envía un mensaje automático al influencer usando Selenium
        """
        if campaign_influencer.status != 'review_approved':
            return False

        driver = webdriver.Chrome(executable_path=settings.SELENIUM_DRIVER_PATH)
        driver.implicitly_wait(10)

        try:
            # Iniciar sesión en Instagram
            driver.get('https://www.instagram.com/accounts/login/')
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            # Aquí deberías usar credenciales seguras almacenadas en variables de entorno
            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")
            username_input.send_keys(settings.INSTAGRAM_USERNAME)
            password_input.send_keys(settings.INSTAGRAM_PASSWORD)
            password_input.submit()

            # Esperar a que se cargue la página principal
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "svg[aria-label='Direct']"))
            )

            # Ir al perfil del influencer
            driver.get(f'https://www.instagram.com/{campaign_influencer.influencer.username}/')
            
            # Hacer clic en el botón de mensaje
            message_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[class*='_acan'][class*='_acap']"))
            )
            message_button.click()

            # Esperar a que aparezca el campo de mensaje
            message_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[placeholder*='Mensaje']"))
            )

            # Construir y enviar el mensaje
            message = self._build_campaign_message(campaign_influencer)
            message_input.send_keys(message)
            message_input.submit()

            # Actualizar el estado del CampaignInfluencer
            campaign_influencer.status = 'message_sent'
            campaign_influencer.message_sent_date = datetime.now()
            campaign_influencer.save()

            return True

        except Exception as e:
            print(f"Error al enviar mensaje al influencer: {str(e)}")
            return False

        finally:
            driver.quit()

    def _build_campaign_message(self, campaign_influencer):
        """
        Construye el mensaje personalizado para el influencer
        """
        return f"""¡Hola @{campaign_influencer.influencer.username}!

Esperamos que estés teniendo un excelente día. Somos {campaign_influencer.campaign.company.get_full_name()} y nos gustaría invitarte a participar en nuestra campaña "{campaign_influencer.campaign.name}".

Detalles de la campaña:
- Duración: {campaign_influencer.campaign.start_date.strftime('%d/%m/%Y')} - {campaign_influencer.campaign.end_date.strftime('%d/%m/%Y')}
- Presupuesto por publicación: ${campaign_influencer.influencer.price_per_post}

{campaign_influencer.campaign.description}

¿Te gustaría conocer más detalles sobre esta oportunidad?

¡Esperamos tu respuesta!
Saludos cordiales.""" 