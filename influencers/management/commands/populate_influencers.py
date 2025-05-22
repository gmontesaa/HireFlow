from django.core.management.base import BaseCommand
from influencers.services.scraping_service import ScrapingService

class Command(BaseCommand):
    help = 'Pobla la base de datos con influencers colombianos'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando población de influencers colombianos...')
        
        try:
            service = ScrapingService()
            service.populate_colombian_influencers()
            self.stdout.write(self.style.SUCCESS('¡Influencers colombianos creados exitosamente!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al poblar influencers: {str(e)}')) 