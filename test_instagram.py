from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

def random_sleep(min_seconds=1, max_seconds=3):
    time.sleep(random.uniform(min_seconds, max_seconds))

def simulate_typing(element, text):
    for char in text:
        element.send_keys(char)
        random_sleep(0.1, 0.3)

def test_instagram_login():
    # Credenciales directas (solo para pruebas)
    username = "geronimo_m115"
    password = "Geronimo200519"
    
    print(f"Usuario configurado: {username}")
    
    driver = None
    try:
        print("Iniciando prueba de inicio de sesión...")
        
        # Configurar opciones de Chrome
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Configuraciones adicionales
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        print("Configurando Chrome driver...")
        driver = webdriver.Chrome(options=chrome_options)
        
        # Ocultar que estamos usando WebDriver
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.116 Safari/537.36'
        })
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Establecer dimensiones de ventana realistas
        driver.set_window_size(1366, 768)
        
        print("Navegando a Instagram...")
        driver.get('https://www.instagram.com/accounts/login/')
        random_sleep(2, 4)
        
        print("Buscando campos de inicio de sesión...")
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_input = driver.find_element(By.NAME, "password")
        
        # Simular movimiento del mouse
        actions = ActionChains(driver)
        actions.move_to_element(username_input)
        actions.click()
        actions.perform()
        random_sleep(0.5, 1)
        
        print("Ingresando credenciales...")
        simulate_typing(username_input, username)
        random_sleep(0.5, 1.5)
        
        actions.move_to_element(password_input)
        actions.click()
        actions.perform()
        random_sleep(0.5, 1)
        
        simulate_typing(password_input, password)
        random_sleep(0.5, 1.5)
        
        print("Haciendo clic en el botón de inicio de sesión...")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        actions.move_to_element(login_button)
        actions.click()
        actions.perform()
        
        print("Esperando respuesta...")
        random_sleep(4, 6)
        
        # Verificar si hay mensaje de error
        try:
            error_message = driver.find_element(By.ID, "slfErrorAlert")
            print(f"Error de inicio de sesión: {error_message.text}")
        except NoSuchElementException:
            print("No se encontró mensaje de error, verificando si el inicio de sesión fue exitoso...")
            try:
                # Verificar si estamos en la página principal
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//nav"))
                )
                print("¡Inicio de sesión exitoso!")
                
                # Esperar un poco más para asegurarnos de que todo cargó
                random_sleep(3, 5)
                
                # Intentar navegar al perfil
                print("Navegando al perfil...")
                profile_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/geronimo_m115/')]"))
                )
                actions.move_to_element(profile_button)
                actions.click()
                actions.perform()
                
            except TimeoutException:
                print("No se pudo confirmar el inicio de sesión exitoso")
        
    except Exception as e:
        print(f"Error durante la prueba: {str(e)}")
        print(f"Tipo de error: {type(e).__name__}")
    finally:
        if driver:
            print("Cerrando el navegador...")
            random_sleep(1, 2)
            driver.quit()

if __name__ == "__main__":
    test_instagram_login() 