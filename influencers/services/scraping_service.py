from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.conf import settings
import re
import time

class ScrapingService:
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
        base_price = followers * 0.01  # $0.01 por seguidor
        engagement_multiplier = 1 + (engagement_rate / 100)  # Aumento por engagement
        return round(base_price * engagement_multiplier, 2)
    
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