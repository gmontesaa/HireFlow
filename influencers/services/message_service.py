from django.utils import timezone
from ..models import Campaign, CampaignInfluencer

class MessageService:
    @staticmethod
    def generate_campaign_message(campaign_influencer):
        """
        Genera un mensaje personalizado para el influencer.
        """
        campaign = campaign_influencer.campaign
        influencer = campaign_influencer.influencer
        
        # Calcular días restantes
        days_remaining = (campaign.end_date - timezone.now().date()).days
        
        # Construir el mensaje
        message = f"""¡Hola {influencer.name}! 👋

Nos encantaría que te unas a nuestra campaña "{campaign.name}".

📅 Duración: {campaign.start_date.strftime('%d/%m/%Y')} - {campaign.end_date.strftime('%d/%m/%Y')}
💰 Presupuesto: ${campaign.budget}
📝 Descripción: {campaign.description}

⏳ Quedan {days_remaining} días para participar.

¿Te gustaría ser parte de esta campaña? ¡Esperamos tu respuesta! 😊

Para más información, puedes visitar tu perfil en nuestra plataforma:
{influencer.get_absolute_url()}"""
        
        return message
    
    @staticmethod
    def get_instagram_direct_link(username):
        """
        Genera el enlace directo al chat de Instagram del influencer.
        """
        return f"https://www.instagram.com/direct/t/{username}/"
    
    @staticmethod
    def get_message_context(campaign_influencer):
        """
        Obtiene el contexto completo para el envío de mensajes.
        """
        message = MessageService.generate_campaign_message(campaign_influencer)
        instagram_link = MessageService.get_instagram_direct_link(
            campaign_influencer.influencer.username
        )
        
        return {
            'message': message,
            'instagram_link': instagram_link,
            'influencer': campaign_influencer.influencer,
            'campaign': campaign_influencer.campaign,
            'status': campaign_influencer.status,
            'message_sent_date': campaign_influencer.message_sent_date
        } 