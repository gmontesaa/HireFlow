from django.core.management.base import BaseCommand
from influencers.models import Influencer

class Command(BaseCommand):
    help = 'Carga influencers iniciales en la base de datos'

    def handle(self, *args, **kwargs):
        # Eliminar influencers existentes
        Influencer.objects.all().delete()
        
        # Datos de influencers
        influencers_data = [
            {
                'name': 'Gary Vaynerchuk',
                'username': 'garyvee',
                'platform': 'instagram',
                'category': 'business',
                'followers': 10000000,
                'engagement_rate': 3.5,
                'description': 'Empresario, autor y orador motivacional especializado en marketing digital y redes sociales.',
                'price_per_post': 50000,
                'contact_email': 'contact@garyvaynerchuk.com',
                'instagram_url': 'https://www.instagram.com/garyvee/',
                'is_available': True
            },
            {
                'name': 'Tony Robbins',
                'username': 'tonyrobbins',
                'platform': 'instagram',
                'category': 'motivation',
                'followers': 5000000,
                'engagement_rate': 4.2,
                'description': 'Coach de vida y autor bestseller, experto en desarrollo personal y profesional.',
                'price_per_post': 45000,
                'contact_email': 'contact@tonyrobbins.com',
                'instagram_url': 'https://www.instagram.com/tonyrobbins/',
                'is_available': True
            },
            {
                'name': 'Mel Robbins',
                'username': 'melrobbins',
                'platform': 'instagram',
                'category': 'motivation',
                'followers': 3000000,
                'engagement_rate': 5.1,
                'description': 'Autora y presentadora, experta en productividad y desarrollo personal.',
                'price_per_post': 35000,
                'contact_email': 'contact@melrobbins.com',
                'instagram_url': 'https://www.instagram.com/melrobbins/',
                'is_available': True
            },
            {
                'name': 'Jay Shetty',
                'username': 'jayshetty',
                'platform': 'instagram',
                'category': 'motivation',
                'followers': 12000000,
                'engagement_rate': 4.8,
                'description': 'Ex monje, autor y presentador, especializado en mindfulness y desarrollo personal.',
                'price_per_post': 55000,
                'contact_email': 'contact@jayshetty.com',
                'instagram_url': 'https://www.instagram.com/jayshetty/',
                'is_available': True
            },
            {
                'name': 'Robin Sharma',
                'username': 'robinsharma',
                'platform': 'instagram',
                'category': 'motivation',
                'followers': 2000000,
                'engagement_rate': 3.9,
                'description': 'Autor y speaker motivacional, experto en liderazgo y excelencia personal.',
                'price_per_post': 30000,
                'contact_email': 'contact@robinsharma.com',
                'instagram_url': 'https://www.instagram.com/robinsharma/',
                'is_available': True
            },
            {
                'name': 'Lewis Howes',
                'username': 'lewishowes',
                'platform': 'instagram',
                'category': 'business',
                'followers': 4000000,
                'engagement_rate': 4.5,
                'description': 'Empresario, autor y podcaster, especializado en emprendimiento y desarrollo personal.',
                'price_per_post': 40000,
                'contact_email': 'contact@lewishowes.com',
                'instagram_url': 'https://www.instagram.com/lewishowes/',
                'is_available': True
            },
            {
                'name': 'Marie Forleo',
                'username': 'marieforleo',
                'platform': 'instagram',
                'category': 'business',
                'followers': 2500000,
                'engagement_rate': 4.7,
                'description': 'Empresaria y autora, experta en emprendimiento y marketing digital.',
                'price_per_post': 35000,
                'contact_email': 'contact@marieforleo.com',
                'instagram_url': 'https://www.instagram.com/marieforleo/',
                'is_available': True
            },
            {
                'name': 'Grant Cardone',
                'username': 'grantcardone',
                'platform': 'instagram',
                'category': 'business',
                'followers': 3000000,
                'engagement_rate': 3.8,
                'description': 'Empresario y autor, especializado en ventas y desarrollo de negocios.',
                'price_per_post': 45000,
                'contact_email': 'contact@grantcardone.com',
                'instagram_url': 'https://www.instagram.com/grantcardone/',
                'is_available': True
            },
            {
                'name': 'Rachel Hollis',
                'username': 'msrachelhollis',
                'platform': 'instagram',
                'category': 'lifestyle',
                'followers': 2000000,
                'engagement_rate': 4.2,
                'description': 'Autora y presentadora, especializada en desarrollo personal y estilo de vida.',
                'price_per_post': 30000,
                'contact_email': 'contact@rachelhollis.com',
                'instagram_url': 'https://www.instagram.com/msrachelhollis/',
                'is_available': True
            },
            {
                'name': 'Jen Sincero',
                'username': 'jensincero',
                'platform': 'instagram',
                'category': 'lifestyle',
                'followers': 1500000,
                'engagement_rate': 4.0,
                'description': 'Autora y coach, especializada en desarrollo personal y transformación de vida.',
                'price_per_post': 25000,
                'contact_email': 'contact@jensincero.com',
                'instagram_url': 'https://www.instagram.com/jensincero/',
                'is_available': True
            }
        ]
        
        # Crear influencers
        for data in influencers_data:
            try:
                influencer = Influencer.objects.create(**data)
                self.stdout.write(self.style.SUCCESS(f'Influencer creado: {data["name"]} con URL de Instagram: {data["instagram_url"]}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error al crear influencer {data["name"]}: {str(e)}')) 