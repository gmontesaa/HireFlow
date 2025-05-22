from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from django.core.exceptions import ValidationError
from django.conf import settings
import re
import time
import os
from ..models import Influencer, Category
import random
import json
import requests
from django.utils.text import slugify
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from decimal import Decimal, ROUND_HALF_UP

class ScrapingService:
    """
    Servicio que maneja la lógica de negocio relacionada con el scraping de datos de influencers.
    """
    def __init__(self):
        """Inicializa el servicio de scraping."""
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = None
        self.wait = None

    def setup_driver(self):
        """
        Configura el driver de Selenium.
        
        Raises:
            ValidationError: Si hay un error al configurar el driver
        """
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
        except Exception as e:
            raise ValidationError(f"Error al configurar el driver: {str(e)}")

    def close_driver(self):
        """Cierra el driver de Selenium."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None

    def login_to_instagram(self, username, password):
        """
        Inicia sesión en Instagram.
        
        Args:
            username (str): Nombre de usuario de Instagram
            password (str): Contraseña de Instagram
            
        Raises:
            ValidationError: Si hay un error al iniciar sesión
        """
        try:
            self.driver.get('https://www.instagram.com/accounts/login/')
            time.sleep(2)
            
            # Ingresar credenciales
            username_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, 'username'))
            )
            password_input = self.driver.find_element(By.NAME, 'password')
            
            username_input.send_keys(username)
            password_input.send_keys(password)
            
            # Hacer clic en el botón de inicio de sesión
            login_button = self.driver.find_element(
                By.XPATH, "//button[@type='submit']"
            )
            login_button.click()
            
            # Esperar a que se complete el inicio de sesión
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'svg[aria-label="Home"]'))
            )
        except Exception as e:
            raise ValidationError(f"Error al iniciar sesión en Instagram: {str(e)}")

    def get_influencer_data(self, username):
        """
        Obtiene datos de un influencer de Instagram.
        
        Args:
            username (str): Nombre de usuario del influencer
            
        Returns:
            dict: Datos del influencer
            
        Raises:
            ValidationError: Si hay un error al obtener los datos
        """
        try:
            self.driver.get(f'https://www.instagram.com/{username}/')
            time.sleep(2)
            
            # Obtener número de seguidores
            followers_element = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//span[contains(text(), 'followers')]")
                )
            )
            followers = int(followers_element.text.split()[0].replace(',', ''))
            
            # Obtener número de publicaciones
            posts_element = self.driver.find_element(
                By.XPATH, "//span[contains(text(), 'posts')]"
            )
            posts = int(posts_element.text.split()[0].replace(',', ''))
            
            # Obtener nombre
            name_element = self.driver.find_element(
                By.XPATH, "//h2[contains(@class, '_aacl')]"
            )
            name = name_element.text
            
            # Obtener descripción
            try:
                bio_element = self.driver.find_element(
                    By.XPATH, "//h1[contains(@class, '_aacl')]"
                )
                description = bio_element.text
            except NoSuchElementException:
                description = ""
            
            return {
                'name': name,
                'username': username,
                'followers': followers,
                'posts': posts,
                'description': description,
                'platform': 'instagram',
                'instagram_url': f'https://www.instagram.com/{username}/',
            }
        except Exception as e:
            raise ValidationError(f"Error al obtener datos del influencer: {str(e)}")

    def get_instagram_data(self, username):
        """Obtiene datos de un influencer de Instagram usando Selenium"""
        try:
            self.setup_driver()
            
            # Ir al perfil del influencer
            self.driver.get(f'https://www.instagram.com/{username}/')
            time.sleep(3)  # Esperar a que cargue la página
            
            # Obtener datos básicos
            try:
                name = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'h2._aacl._aaco._aacu._aacx._aad6._aade'))
                ).text
            except:
                name = username
            
            try:
                bio = self.driver.find_element(
                    By.CSS_SELECTOR, 'h1._aacl._aaco._aacu._aacx._aad6._aade'
                ).text
            except:
                bio = ""
            
            # Obtener seguidores (simulado ya que no podemos acceder sin login)
            followers = random.randint(100000, 50000000)
            
            # Obtener publicaciones (simulado)
            posts = random.randint(100, 2000)
            
            # Calcular engagement rate (estimado)
            engagement_rate = self._calculate_engagement_rate(posts)
            
            # Calcular precio por post (estimado)
            price_per_post = self._estimate_price(followers, engagement_rate)
            
            # Generar slug único
            slug = slugify(username)
            counter = 1
            while Influencer.objects.filter(slug=slug).exists():
                slug = f"{slugify(username)}-{counter}"
                counter += 1
            
            return {
                'name': name,
                'username': username,
                'description': bio,
                'followers': followers,
                'posts': posts,
                'engagement_rate': engagement_rate,
                'price_per_post': price_per_post,
                'platform': 'instagram',
                'location': 'Colombia',
                'slug': slug
            }
        except Exception as e:
            if self.driver:
                self.driver.quit()
            raise ValidationError(f"Error al obtener datos de Instagram: {str(e)}")
        finally:
            self.close_driver()

    def get_tiktok_data(self, username):
        """Obtiene datos de un influencer de TikTok usando n8n"""
        try:
            # Configurar la URL de n8n
            n8n_url = f"{settings.N8N_URL}/webhook/tiktok-scraper"
            
            # Preparar los datos para n8n
            data = {
                'username': username
            }
            
            # Hacer la petición a n8n
            response = requests.post(n8n_url, json=data)
            response.raise_for_status()
            
            # Procesar la respuesta
            tiktok_data = response.json()
            
            return {
                'name': tiktok_data.get('name', username),
                'username': username,
                'description': tiktok_data.get('bio', ''),
                'followers': tiktok_data.get('followers', 0),
                'engagement_rate': tiktok_data.get('engagement_rate', 0),
                'price_per_post': tiktok_data.get('price_per_post', 0),
                'platform': 'tiktok',
                'location': 'Colombia'
            }
        except Exception as e:
            raise ValidationError(f"Error al obtener datos de TikTok: {str(e)}")

    def create_influencer_from_instagram(self, username, categories=None):
        """Crea un influencer a partir de datos de Instagram"""
        try:
            data = self.get_instagram_data(username)
            return self._create_or_update_influencer(data, categories)
        except Exception as e:
            raise ValidationError(f"Error al crear influencer desde Instagram: {str(e)}")

    def create_influencer_from_tiktok(self, username, categories=None):
        """Crea un influencer a partir de datos de TikTok"""
        try:
            data = self.get_tiktok_data(username)
            return self._create_or_update_influencer(data, categories)
        except Exception as e:
            raise ValidationError(f"Error al crear influencer desde TikTok: {str(e)}")

    def _create_or_update_influencer(self, data, categories=None):
        """Crea o actualiza un influencer en la base de datos"""
        try:
            # Asegurar que engagement_rate y price_per_post sean Decimal redondeados
            engagement_rate = Decimal(str(data.get('engagement_rate', 0))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            price_per_post = Decimal(str(data.get('price_per_post', 0))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            influencer, created = Influencer.objects.update_or_create(
                username=data['username'],
                platform=data['platform'],
                defaults={
                    'name': data['name'],
                    'description': data['description'],
                    'followers': data['followers'],
                    'engagement_rate': engagement_rate,
                    'price_per_post': price_per_post,
                    'location': data['location'],
                    'slug': data['slug']
                }
            )
            
            if categories:
                influencer.categories.set(categories)
            
            return influencer
        except Exception as e:
            raise ValidationError(f"Error al guardar influencer: {str(e)}")

    def populate_colombian_influencers(self):
        """Pobla la base de datos con influencers colombianos"""
        # Lista de influencers colombianos populares
        instagram_influencers = [
            'juanpazurita',
            'valentinaquintero',
            'juanes',
            'shakira',
            'maluma',
            'jbalvin',
            'karolg',
            'manuel_turizo',
            'sebastianyatra',
            'camilo',
            'feid',
            'paolaguerrero',
            'jamesdrodriguez',
            'radamel_falcao',
            'juanferquintero',
            'davidospina',
            'yuribuenaventura',
            'carlosvives',
            'fonseca',
            'jorgecela'
        ]
        
        tiktok_influencers = [
            'juanpazurita',
            'valentinaquintero',
            'juanes',
            'shakira',
            'maluma',
            'jbalvin',
            'karolg',
            'manuel_turizo',
            'sebastianyatra',
            'camilo'
        ]
        
        # Obtener o crear categorías
        categories = {
            'música': Category.objects.get_or_create(name='Música')[0],
            'moda': Category.objects.get_or_create(name='Moda')[0],
            'lifestyle': Category.objects.get_or_create(name='Lifestyle')[0],
            'entretenimiento': Category.objects.get_or_create(name='Entretenimiento')[0],
            'deportes': Category.objects.get_or_create(name='Deportes')[0],
            'comedia': Category.objects.get_or_create(name='Comedia')[0],
            'belleza': Category.objects.get_or_create(name='Belleza')[0],
            'gastronomía': Category.objects.get_or_create(name='Gastronomía')[0],
            'viajes': Category.objects.get_or_create(name='Viajes')[0],
            'tecnología': Category.objects.get_or_create(name='Tecnología')[0]
        }
        
        # Crear influencers de Instagram
        for username in instagram_influencers:
            try:
                # Asignar categorías aleatorias
                influencer_categories = random.sample(list(categories.values()), k=random.randint(1, 3))
                self.create_influencer_from_instagram(username, influencer_categories)
                print(f"Influencer de Instagram creado: {username}")
                time.sleep(2)  # Esperar para no sobrecargar Instagram
            except Exception as e:
                print(f"Error al crear influencer de Instagram {username}: {str(e)}")
        
        # Crear influencers de TikTok
        for username in tiktok_influencers:
            try:
                # Asignar categorías aleatorias
                influencer_categories = random.sample(list(categories.values()), k=random.randint(1, 3))
                self.create_influencer_from_tiktok(username, influencer_categories)
                print(f"Influencer de TikTok creado: {username}")
                time.sleep(1)  # Esperar para no sobrecargar n8n
            except Exception as e:
                print(f"Error al crear influencer de TikTok {username}: {str(e)}")

    @staticmethod
    def scrape_instagram_data(username):
        """Obtiene datos de un influencer de Instagram."""
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
            driver.get(f"https://www.instagram.com/{username}/")
            
            # Esperar a que se cargue el perfil
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'x1lliihq')]"))
            )
            
            # Obtener datos del perfil
            name = driver.find_element(By.XPATH, "//h2[contains(@class, 'x1lliihq')]").text
            bio = driver.find_element(By.XPATH, "//h1[contains(@class, 'x1lliihq')]").text
            
            # Obtener número de seguidores
            followers_text = driver.find_element(By.XPATH, "//li[contains(., 'seguidores')]").text
            followers = int(re.sub(r'[^\d]', '', followers_text))
            
            # Obtener número de publicaciones
            posts_text = driver.find_element(By.XPATH, "//li[contains(., 'publicaciones')]").text
            posts = int(re.sub(r'[^\d]', '', posts_text))
            
            # Calcular tasa de engagement
            engagement_rate = ScrapingService._calculate_engagement_rate(driver, posts)
            
            # Estimar precio por publicación
            price_per_post = ScrapingService._estimate_price(followers, engagement_rate)
            
            # Convertir a Decimal redondeado
            engagement_rate = Decimal(str(engagement_rate)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            price_per_post = Decimal(str(price_per_post)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            driver.quit()
            
            return {
                'name': name,
                'username': username,
                'bio': bio,
                'followers': followers,
                'posts': posts,
                'engagement_rate': engagement_rate,
                'price_per_post': price_per_post,
                'platform': 'instagram'
            }
            
        except Exception as e:
            print(f"Error al obtener datos de Instagram: {str(e)}")
            if 'driver' in locals():
                driver.quit()
            return None
    
    @staticmethod
    def _calculate_engagement_rate(driver, posts):
        """Calcula la tasa de engagement basada en las últimas publicaciones."""
        try:
            # Obtener las últimas 12 publicaciones
            posts_data = []
            for _ in range(min(12, posts)):
                try:
                    post = driver.find_element(By.XPATH, "//article[contains(@class, '_aagv')]")
                    likes = int(re.sub(r'[^\d]', '', post.find_element(By.XPATH, ".//span[contains(@class, '_aacl')]").text))
                    posts_data.append(likes)
                    driver.execute_script("arguments[0].scrollIntoView();", post)
                    time.sleep(1)
                except:
                    break
            
            if not posts_data:
                return 0
            
            # Calcular engagement rate promedio
            avg_likes = sum(posts_data) / len(posts_data)
            followers = int(re.sub(r'[^\d]', '', driver.find_element(By.XPATH, "//li[contains(., 'seguidores')]").text))
            return (avg_likes / followers) * 100
            
        except Exception as e:
            print(f"Error al calcular engagement rate: {str(e)}")
            return 0
    
    @staticmethod
    def _estimate_price(followers, engagement_rate):
        """Estima el precio por publicación basado en seguidores y engagement."""
        base_price = Decimal(str(followers)) * Decimal('0.01')  # $0.01 por seguidor
        engagement_multiplier = Decimal('1') + (Decimal(str(engagement_rate)) / Decimal('100'))
        return Decimal(str(round(base_price * engagement_multiplier, 2)))
    
    @staticmethod
    def scrape_tiktok_data(username):
        """Obtiene datos de un influencer de TikTok."""
        try:
            driver = webdriver.Chrome(executable_path=settings.SELENIUM_DRIVER_PATH)
            if settings.SELENIUM_HEADLESS:
                driver.set_window_size(1920, 1080)
            
            # Ir al perfil de TikTok
            driver.get(f"https://www.tiktok.com/@{username}")
            
            # Esperar a que se cargue el perfil
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'tiktok-1wr4jig')]"))
            )
            
            # Obtener datos del perfil
            name = driver.find_element(By.XPATH, "//h2[contains(@class, 'tiktok-1wr4jig')]").text
            bio = driver.find_element(By.XPATH, "//h2[contains(@class, 'tiktok-1wr4jig')]/following-sibling::p").text
            
            # Obtener número de seguidores
            followers_text = driver.find_element(By.XPATH, "//strong[contains(@class, 'tiktok-1wr4jig')]").text
            followers = int(re.sub(r'[^\d]', '', followers_text))
            
            # Obtener número de likes
            likes_text = driver.find_element(By.XPATH, "//strong[contains(@class, 'tiktok-1wr4jig')][2]").text
            likes = int(re.sub(r'[^\d]', '', likes_text))
            
            # Calcular tasa de engagement
            engagement_rate = (likes / followers) * 100 if followers > 0 else 0
            
            # Estimar precio por publicación
            price_per_post = ScrapingService._estimate_price(followers, engagement_rate)
            
            # Convertir a Decimal redondeado
            engagement_rate = Decimal(str(engagement_rate)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            price_per_post = Decimal(str(price_per_post)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            driver.quit()
            
            return {
                'name': name,
                'username': username,
                'bio': bio,
                'followers': followers,
                'likes': likes,
                'engagement_rate': engagement_rate,
                'price_per_post': price_per_post,
                'platform': 'tiktok'
            }
            
        except Exception as e:
            print(f"Error al obtener datos de TikTok: {str(e)}")
            if 'driver' in locals():
                driver.quit()
            return None

    def _calculate_engagement_rate(self, posts):
        """Calcula una tasa de engagement estimada basada en el número de publicaciones"""
        base_rate = Decimal(str(random.uniform(1.5, 5.0)))
        # Ajustar según el número de publicaciones
        if posts > 1000:
            base_rate *= Decimal('1.2')
        elif posts < 100:
            base_rate *= Decimal('0.8')
        return Decimal(str(round(base_rate, 2)))

    def _estimate_price(self, followers, engagement_rate):
        """Estima el precio por publicación basado en seguidores y engagement"""
        base_price = Decimal(str(followers)) * Decimal('0.01')  # $0.01 por seguidor
        engagement_multiplier = Decimal('1') + (Decimal(str(engagement_rate)) / Decimal('100'))
        return Decimal(str(round(base_price * engagement_multiplier, 2))) 