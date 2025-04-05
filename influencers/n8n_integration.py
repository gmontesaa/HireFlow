import requests
import json
from django.conf import settings

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