# Plataforma de Marketing con Influencers

Esta plataforma web permite a las empresas encontrar y colaborar con influencers para sus campañas de marketing. Incluye funcionalidades de registro, búsqueda de influencers, creación de campañas y automatización de procesos.

## Características Principales

- Registro y autenticación de empresas
- Base de datos de influencers con información detallada
- Sistema de búsqueda y filtrado de influencers
- Creación y gestión de campañas de marketing
- Integración con Selenium para scraping de datos
- Automatización de procesos con n8n

## Requisitos del Sistema

- Python 3.8 o superior
- Django 4.2
- PostgreSQL (opcional, se puede usar SQLite para desarrollo)
- Selenium
- n8n (para automatización)

## Instalación

1. Clonar el repositorio:
```bash
git clone [url-del-repositorio]
cd adsinfluencersproject
```

2. Crear y activar un entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la base de datos:
```bash
python manage.py migrate
```

5. Crear un superusuario:
```bash
python manage.py createsuperuser
```

6. Ejecutar el servidor de desarrollo:
```bash
python manage.py runserver
```

## Configuración de n8n

1. Instalar n8n:
```bash
npm install n8n -g
```

2. Iniciar n8n:
```bash
n8n start
```

3. Configurar los flujos de automatización en la interfaz web de n8n (http://localhost:5678)

## Uso

1. Acceder a la plataforma en http://localhost:8000
2. Registrarse como empresa
3. Buscar influencers por categoría o palabra clave
4. Crear campañas y asignar influencers
5. Gestionar las campañas desde el panel de control

## Estructura del Proyecto

```
adsinfluencersproject/
├── config/                 # Configuración principal de Django
├── influencers/            # Aplicación principal de influencers
├── accounts/              # Gestión de usuarios y autenticación
├── templates/             # Plantillas HTML
├── static/                # Archivos estáticos (CSS, JS, imágenes)
└── manage.py              # Script de gestión de Django
```

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.