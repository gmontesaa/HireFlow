from django.core.management.base import BaseCommand
from influencers.models import Category

class Command(BaseCommand):
    help = 'Crea las categorías iniciales'

    def handle(self, *args, **kwargs):
        categories = [
            {'name': 'Moda', 'description': 'Influencers especializados en moda y tendencias'},
            {'name': 'Belleza', 'description': 'Influencers de belleza, maquillaje y cuidado personal'},
            {'name': 'Fitness', 'description': 'Influencers de ejercicio, salud y bienestar'},
            {'name': 'Comida', 'description': 'Influencers de gastronomía y cocina'},
            {'name': 'Viajes', 'description': 'Influencers de viajes y aventuras'},
            {'name': 'Tecnología', 'description': 'Influencers de tecnología y gadgets'},
            {'name': 'Estilo de Vida', 'description': 'Influencers de lifestyle y vida cotidiana'},
            {'name': 'Gaming', 'description': 'Influencers de videojuegos y streaming'},
            {'name': 'Negocios', 'description': 'Influencers de emprendimiento y negocios'},
            {'name': 'Educación', 'description': 'Influencers educativos y de desarrollo personal'},
        ]

        for category_data in categories:
            Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            self.stdout.write(
                self.style.SUCCESS(f'Categoría "{category_data["name"]}" creada exitosamente')
            ) 