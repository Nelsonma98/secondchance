# Second Chance - Marketplace de Productos de Segunda Mano

## 📋 Descripción

**Second Chance** es una plataforma web construida con Django que permite comprar y vender productos de segunda mano. La aplicación ofrece un sistema de categorización de productos, gestión de anuncios destacados y un panel administrativo para controlar todo el contenido.

## 🚀 Características Principales

- ✅ Catálogo dinámico de productos organizados por categorías
- 📸 Gestión de imágenes para productos y anuncios
- 📢 Sistema de anuncios destacados configurable
- 🎯 Panel administrativo completo
- 📱 API REST para el frontend
- 🐳 Despliegue con Docker y Docker Compose

## 📋 Requisitos Previos

- Python 3.8+
- Django 4.0.6
- MySQL 5.7+
- Docker y Docker Compose (opcional, para despliegue)

## 🔧 Instalación

### Opción 1: Instalación Local

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd Second-Chance/secondchance
   ```

2. **Crear un entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la base de datos**
   - Crear una base de datos MySQL
   - Actualizar las credenciales en `secondchance/settings.py`

5. **Ejecutar migraciones**
   ```bash
   python manage.py migrate
   ```

6. **Crear un superusuario**
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecutar el servidor**
   ```bash
   python manage.py runserver
   ```

### Opción 2: Despliegue con Docker

1. **Navegar a la carpeta Docker**
   ```bash
   cd Docker
   ```

2. **Levantar los contenedores**
   ```bash
   docker-compose up -d
   ```

## 📂 Estructura del Proyecto

```
secondchance/
├── shop/                 # Aplicación principal del marketplace
│   ├── models.py         # Modelos: Product, Category, Ad
│   ├── views.py          # Vistas de la aplicación
│   ├── admin.py          # Configuración del admin
│   └── migrations/       # Migraciones de BD
├── panel/                # Panel administrativo
│   ├── views.py          # Vistas del panel
│   └── admin.py          # Configuración del admin
├── secondchance/         # Configuración del proyecto
│   ├── settings.py       # Configuración de Django
│   ├── urls.py           # Rutas principales
│   ├── wsgi.py           # Configuración WSGI
│   └── asgi.py           # Configuración ASGI
├── images/               # Almacenamiento de archivos
│   ├── products/         # Imágenes de productos
│   └── ads/              # Imágenes de anuncios
├── manage.py             # Comando de gestión de Django
└── requirements.txt      # Dependencias del proyecto
```

## 📊 Modelos de Datos

### Category
- `name`: Nombre de la categoría
- `created_at`: Fecha de creación

### Product
- `name`: Nombre del producto
- `description`: Descripción detallada
- `price`: Precio en decimal
- `image`: Imagen del producto
- `contact_phone`: Teléfono de contacto del vendedor
- `category`: Referencia a la categoría
- `created_at`: Fecha de creación

### Ad
- `name`: Nombre del anuncio
- `order`: Orden de visualización
- `image`: Imagen del anuncio
- `created_at`: Fecha de creación

## 💻 Dependencias

```
Django==4.0.6
mysqlclient==2.2.8
Pillow==12.2.0
asgiref==3.11.1
sqlparse==0.5.5
typing_extensions==4.15.0
```

## 🔐 Configuración de Seguridad

⚠️ **Importante para Producción:**

1. Cambiar `DEBUG = False` en `settings.py`
2. Actualizar `SECRET_KEY` con un valor seguro
3. Configurar `ALLOWED_HOSTS` correctamente
4. Usar variables de entorno para credenciales sensibles
5. Configurar HTTPS

## 📖 Uso Básico

1. **Acceder al admin**: `http://localhost:8000/admin`
2. **Crear categorías**: Panel Admin → Shop → Categories
3. **Agregar productos**: Panel Admin → Shop → Products
4. **Configurar anuncios**: Panel Admin → Shop → Ads
5. **Gestionar contenido**: Panel Admin → Panel

## 🐳 Docker Compose

El archivo `docker-compose.yml` incluye:
- **Web**: Contenedor de la aplicación Django
- **Database**: Contenedor de MySQL

Para más detalles, ver `Docker/docker-compose.yml`

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el repositorio
2. Crea una rama con tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 📧 Soporte

Para reportar problemas o sugerencias, abre un issue en el repositorio.

---

**Desarrollado con ❤️ usando Django**
