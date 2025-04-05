from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar en modo headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)

def scrape_instagram_data(username):
    driver = setup_driver()
    try:
        driver.get(f'https://www.instagram.com/{username}/')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span._ac2a"))
        )
        followers = driver.find_element(By.CSS_SELECTOR, "span._ac2a").text
        return {
            'followers': followers,
            'engagement_rate': 0.0  # Esto se calculará con n8n
        }
    finally:
        driver.quit()

def scrape_youtube_data(channel_id):
    driver = setup_driver()
    try:
        driver.get(f'https://www.youtube.com/channel/{channel_id}')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#subscriber-count"))
        )
        subscribers = driver.find_element(By.CSS_SELECTOR, "#subscriber-count").text
        return {
            'subscribers': subscribers,
            'engagement_rate': 0.0  # Esto se calculará con n8n
        }
    finally:
        driver.quit() 