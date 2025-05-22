import requests
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from datetime import datetime
import logging
from django.core.exceptions import ValidationError
import os
import json

logger = logging.getLogger(__name__)

class N8NService:
    """
    Servicio que maneja la lógica de negocio relacionada con la integración con N8N.
    """
    def __init__(self):
        """Inicializa el servicio de N8N."""
        self.base_url = os.getenv('N8N_BASE_URL', 'http://localhost:5678')
        self.api_key = os.getenv('N8N_API_KEY')
        
        if not self.api_key:
            raise ValidationError("N8N API key no configurada")

    def _make_request(self, method, endpoint, data=None):
        """
        Realiza una petición a la API de N8N.
        
        Args:
            method (str): Método HTTP (GET, POST, etc.)
            endpoint (str): Endpoint de la API
            data (dict, optional): Datos a enviar en la petición
            
        Returns:
            dict: Respuesta de la API
            
        Raises:
            ValidationError: Si hay un error en la petición
        """
        try:
            headers = {
                'X-N8N-API-KEY': self.api_key,
                'Content-Type': 'application/json'
            }
            
            url = f"{self.base_url}{endpoint}"
            response = requests.request(
                method,
                url,
                headers=headers,
                json=data
            )
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValidationError(f"Error en la petición a N8N: {str(e)}")

    def trigger_workflow(self, workflow_id, data):
        """
        Dispara un workflow de N8N.
        
        Args:
            workflow_id (str): ID del workflow
            data (dict): Datos para el workflow
            
        Returns:
            dict: Respuesta del workflow
            
        Raises:
            ValidationError: Si hay un error al disparar el workflow
        """
        return self._make_request(
            'POST',
            f'/api/v1/workflows/{workflow_id}/trigger',
            data
        )

    def send_campaign_message(self, campaign_influencer_id, message):
        """
        Envía un mensaje de campaña a través de N8N.
        
        Args:
            campaign_influencer_id (int): ID de la relación campaña-influencer
            message (str): Contenido del mensaje
            
        Returns:
            dict: Respuesta del workflow
            
        Raises:
            ValidationError: Si hay un error al enviar el mensaje
        """
        workflow_id = os.getenv('N8N_CAMPAIGN_MESSAGE_WORKFLOW_ID')
        if not workflow_id:
            raise ValidationError("ID del workflow de mensajes no configurado")
            
        data = {
            'campaign_influencer_id': campaign_influencer_id,
            'message': message
        }
        
        return self.trigger_workflow(workflow_id, data)

    def process_influencer_data(self, username):
        """
        Procesa datos de un influencer a través de N8N.
        
        Args:
            username (str): Nombre de usuario del influencer
            
        Returns:
            dict: Datos procesados del influencer
            
        Raises:
            ValidationError: Si hay un error al procesar los datos
        """
        workflow_id = os.getenv('N8N_INFLUENCER_DATA_WORKFLOW_ID')
        if not workflow_id:
            raise ValidationError("ID del workflow de datos de influencer no configurado")
            
        data = {
            'username': username
        }
        
        return self.trigger_workflow(workflow_id, data)

    def get_workflow_status(self, execution_id):
        """
        Obtiene el estado de una ejecución de workflow.
        
        Args:
            execution_id (str): ID de la ejecución
            
        Returns:
            dict: Estado de la ejecución
            
        Raises:
            ValidationError: Si hay un error al obtener el estado
        """
        return self._make_request(
            'GET',
            f'/api/v1/executions/{execution_id}'
        )

    def send_to_hireflow_review(self, campaign_influencer):
        """Envía un influencer a revisión en Hireflow."""
        if not self.base_url or not self.api_key:
            logger.error("N8N configuration is missing")
            return False
            
        try:
            endpoint = f"/api/v1/workflows/{os.getenv('N8N_HIREFLOW_REVIEW_WORKFLOW_ID')}/trigger"
            
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
            
            response = requests.post(f"{self.base_url}{endpoint}", json=payload, timeout=30)
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