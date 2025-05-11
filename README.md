# AdsInfluencers - Plataforma de Marketing de Influencers

AdsInfluencers es una plataforma web desarrollada en Django que conecta empresas con influencers para campañas de marketing. La plataforma permite buscar, gestionar y analizar campañas de marketing con influencers de manera eficiente.

## Características Principales

- Búsqueda avanzada de influencers por categoría, seguidores, engagement y ubicación
- Gestión de campañas de marketing
- Análisis de rendimiento de campañas
- Integración con Instagram y TikTok para scraping de datos
- Sistema de reseñas y calificaciones
- Panel de control con métricas clave
- API REST para integración con otros sistemas

## Requisitos del Sistema

- Python 3.8+
- PostgreSQL 12+
- Redis (para tareas asíncronas)
- Navegador web moderno

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/adsinfluencers.git
cd adsinfluencers
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. Aplicar migraciones:
```bash
python manage.py migrate
```

6. Crear superusuario:
```bash
python manage.py createsuperuser
```

7. Iniciar servidor de desarrollo:
```bash
python manage.py runserver
```

## Estructura del Proyecto

```
adsinfluencers/
├── config/                 # Configuración del proyecto
├── influencers/           # Aplicación principal
│   ├── models/           # Modelos de datos
│   ├── services/         # Lógica de negocio
│   ├── templates/        # Plantillas HTML
│   └── static/          # Archivos estáticos
├── static/              # Archivos estáticos globales
├── media/              # Archivos subidos por usuarios
└── requirements.txt    # Dependencias del proyecto
```

## Uso

1. Acceder a la plataforma en `http://localhost:8000`
2. Iniciar sesión con las credenciales de superusuario
3. Crear categorías de influencers
4. Agregar influencers manualmente o mediante scraping
5. Crear y gestionar campañas
6. Analizar resultados

## API

La API REST está disponible en `/api/v1/`. Documentación detallada en `/api/docs/`.

## Contribución

1. Fork el repositorio
2. Crear rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para soporte, por favor abrir un issue en el repositorio o contactar al equipo de desarrollo.

## Créditos

Desarrollado por [Tu Nombre/Equipo] - 2024