# Configuración de n8n
N8N_URL = 'http://localhost:5678'  # URL por defecto de n8n 

# Configuración de Instagram
import os
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME', '')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD', '') 