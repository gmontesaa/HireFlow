import requests
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class N8NService:
    def __init__(self):
        self.base_url = settings.N8N_BASE_URL
        self.webhook_token = settings.N8N_WEBHOOK_TOKEN
        
        if not self.base_url or not self.webhook_token:
            logger.warning("N8N configuration is missing")
    
    def send_to_hireflow_review(self, campaign_influencer):
        """Envía un influencer a revisión en Hireflow."""
        if not self.base_url or not self.webhook_token:
            logger.error("N8N configuration is missing")
            return False
            
        try:
            webhook_url = f"{self.base_url}/webhook/{self.webhook_token}"
            
            payload = {
                'campaign_id': campaign_influencer.campaign.id,
                'campaign_name': campaign_influencer.campaign.name,
                'influencer_id': campaign_influencer.influencer.id,
                'influencer_name': campaign_influencer.influencer.name,
                'influencer_username': campaign_influencer.influencer.username,
                'followers': campaign_influencer.influencer.followers,
                'engagement_rate': campaign_influencer.influencer.engagement_rate,
                'price_per_post': campaign_influencer.influencer.price_per_post,
                'categories': [cat.name for cat in campaign_influencer.influencer.categories.all()],
                'platform': campaign_influencer.influencer.platform,
                'location': campaign_influencer.influencer.location
            }
            
            response = requests.post(webhook_url, json=payload, timeout=30)
            response.raise_for_status()
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al enviar a Hireflow: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error inesperado al enviar a Hireflow: {str(e)}")
            return False
    
    def send_message_to_influencer(self, campaign_influencer):
        """Envía un mensaje al influencer a través de Instagram."""
        if campaign_influencer.status != 'review_approved':
            logger.warning(f"El influencer {campaign_influencer.influencer.username} no está aprobado para enviar mensaje")
            return False
            
        if not settings.INSTAGRAM_USERNAME or not settings.INSTAGRAM_PASSWORD:
            logger.error("Credenciales de Instagram no configuradas")
            return False
        
        driver = None
        try:
            driver = webdriver.Chrome(executable_path=settings.SELENIUM_DRIVER_PATH)
            if settings.SELENIUM_HEADLESS:
                driver.set_window_size(1920, 1080)
            
            # Iniciar sesión en Instagram
            driver.get('https://www.instagram.com/accounts/login/')
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")
            
            username_input.send_keys(settings.INSTAGRAM_USERNAME)
            password_input.send_keys(settings.INSTAGRAM_PASSWORD)
            
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Esperar a que se cargue el feed
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//svg[@aria-label='Direct']"))
            )
            
            # Ir al perfil del influencer
            driver.get(f"https://www.instagram.com/{campaign_influencer.influencer.username}/")
            
            # Hacer clic en el botón de mensaje
            message_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Mensaje')]"))
            )
            message_button.click()
            
            # Esperar a que se cargue el chat
            message_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Mensaje...']"))
            )
            
            # Enviar mensaje
            message = self._build_campaign_message(campaign_influencer)
            message_input.send_keys(message)
            
            send_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            send_button.click()
            
            # Actualizar estado
            campaign_influencer.status = 'message_sent'
            campaign_influencer.message_sent_date = datetime.now()
            campaign_influencer.save()
            
            return True
            
        except TimeoutException as e:
            logger.error(f"Timeout al enviar mensaje: {str(e)}")
            return False
        except WebDriverException as e:
            logger.error(f"Error de Selenium al enviar mensaje: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error inesperado al enviar mensaje: {str(e)}")
            return False
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    def _build_campaign_message(self, campaign_influencer):
        """Construye el mensaje personalizado para el influencer."""
        return f"""¡Hola {campaign_influencer.influencer.name}! 👋

Nos encantaría que te unas a nuestra campaña "{campaign_influencer.campaign.name}".

Detalles de la campaña:
- Duración: {campaign_influencer.campaign.start_date.strftime('%d/%m/%Y')} - {campaign_influencer.campaign.end_date.strftime('%d/%m/%Y')}
- Presupuesto: ${campaign_influencer.campaign.budget}
- Descripción: {campaign_influencer.campaign.description}

¿Te gustaría participar? ¡Esperamos tu respuesta! 😊""" 