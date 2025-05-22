from django.core.exceptions import ValidationError
from django.utils import timezone
from ..models import Campaign, CampaignInfluencer

class MessageService:
    """
    Servicio que maneja la lógica de negocio relacionada con los mensajes.
    """
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

    @staticmethod
    def send_message_to_influencer(campaign_influencer_id, message):
        """
        Envía un mensaje a un influencer de una campaña.
        
        Args:
            campaign_influencer_id (int): ID de la relación campaña-influencer
            message (str): Contenido del mensaje
            
        Returns:
            CampaignInfluencer: Instancia actualizada de la relación
            
        Raises:
            ValidationError: Si no se puede enviar el mensaje
        """
        try:
            campaign_influencer = CampaignInfluencer.objects.get(id=campaign_influencer_id)
            
            if campaign_influencer.status not in ['review_approved', 'message_sent']:
                raise ValidationError("No se puede enviar un mensaje en el estado actual")
            
            # Aquí se implementaría la lógica real de envío de mensajes
            # Por ahora solo actualizamos el estado
            campaign_influencer.status = 'message_sent'
            campaign_influencer.message_sent_date = timezone.now()
            campaign_influencer.save()
            
            return campaign_influencer
        except Exception as e:
            raise ValidationError(f"Error al enviar el mensaje: {str(e)}")

    @staticmethod
    def get_pending_messages(company_id=None):
        """
        Obtiene los mensajes pendientes de envío.
        
        Args:
            company_id (int, optional): ID de la empresa para filtrar
            
        Returns:
            QuerySet: Conjunto de relaciones campaña-influencer con mensajes pendientes
        """
        queryset = CampaignInfluencer.objects.filter(
            status='review_approved'
        ).select_related('campaign', 'influencer')
        
        if company_id:
            queryset = queryset.filter(campaign__company_id=company_id)
            
        return queryset

    @staticmethod
    def get_sent_messages(company_id=None, days=30):
        """
        Obtiene los mensajes enviados en los últimos días.
        
        Args:
            company_id (int, optional): ID de la empresa para filtrar
            days (int): Número de días hacia atrás para buscar
            
        Returns:
            QuerySet: Conjunto de relaciones campaña-influencer con mensajes enviados
        """
        date_limit = timezone.now() - timezone.timedelta(days=days)
        queryset = CampaignInfluencer.objects.filter(
            status='message_sent',
            message_sent_date__gte=date_limit
        ).select_related('campaign', 'influencer')
        
        if company_id:
            queryset = queryset.filter(campaign__company_id=company_id)
            
        return queryset

    @staticmethod
    def get_message_stats(company_id=None):
        """
        Obtiene estadísticas de mensajes.
        
        Args:
            company_id (int, optional): ID de la empresa para filtrar
            
        Returns:
            dict: Diccionario con estadísticas de mensajes
        """
        queryset = CampaignInfluencer.objects.filter(status__in=['message_sent', 'accepted', 'rejected'])
        
        if company_id:
            queryset = queryset.filter(campaign__company_id=company_id)
            
        return {
            'total_messages': queryset.filter(status='message_sent').count(),
            'accepted_messages': queryset.filter(status='accepted').count(),
            'rejected_messages': queryset.filter(status='rejected').count(),
            'acceptance_rate': (
                queryset.filter(status='accepted').count() /
                queryset.filter(status__in=['accepted', 'rejected']).count() * 100
            ) if queryset.filter(status__in=['accepted', 'rejected']).exists() else 0,
        } 