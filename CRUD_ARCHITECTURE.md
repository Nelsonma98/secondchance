# CRUD Architecture - Panel

## Estructura del Panel

El panel está organizado en capas para separar responsabilidades:

```
panel/
├── view_modules/          # Capa de vistas (maneja requests HTTP)
│   ├── auth.py
│   ├── dashboard.py
│   ├── category.py
│   ├── product.py
│   └── ad.py
├── services/              # Capa de lógica de negocio (CRUD operations)
│   ├── auth.py
│   ├── dashboard.py
│   ├── category.py
│   ├── product.py
│   └── ad.py
├── forms.py               # Validación de formularios
├── views.py               # Módulo que exporta todas las vistas
├── urls.py                # Rutas del panel
└── models.py              # (Vacío, modelos en shop/models.py)
```

## Flujo de Datos

```
HTTP Request
    ↓
panel/urls.py (router)
    ↓
panel/view_modules/*.py (view handler)
    ↓
panel/services/*.py (business logic + validation)
    ↓
shop/models.py (database operations)
    ↓
HTTP Response
```

## Ejemplo: Crear una Categoría

### 1. Usuario envía POST a `/panel/category/create/`
```html
<form method="POST" enctype="multipart/form-data">
    <input type="text" name="name" placeholder="Category name">
    <button type="submit">Create</button>
</form>
```

### 2. URL Router (`panel/urls.py`)
```python
path('category/create/', views.create_category, name='create_category'),
```

### 3. Vista Handler (`panel/view_modules/category.py`)
```python
@login_required
def create_category(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            service_create_category(name)  # Llama al servicio
            return redirect('categories_panel')
        except ValueError as e:
            return render(request, 'category/create-category.html', {'error': str(e)})
```

### 4. Servicio de Lógica (`panel/services/category.py`)
```python
def create_category(name):
    if not name or not name.strip():
        raise ValueError('Category name cannot be empty')
    
    category = Category.objects.create(name=name.strip())
    return category
```

### 5. Modelo (`shop/models.py`)
```python
class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
```

## Operaciones CRUD Disponibles

### Categories
- **Read**: `GET /panel/categories/` → Lista todas las categorías
- **Create**: `POST /panel/category/create/` → Crea una categoría
- **Update**: `POST /panel/category/edit/<id>/` → Actualiza una categoría
- **Delete**: `POST /panel/category/delete/<id>/` → Elimina una categoría

### Products
- **Read**: `GET /panel/products` → Lista todos los productos
- **Create**: `POST /panel/product/create/` → Crea un producto
- **Update**: `POST /panel/product/edit/<id>/` → Actualiza un producto
- **Delete**: `POST /panel/product/delete/<id>/` → Elimina un producto

### Ads
- **Read**: `GET /panel/ads` → Lista todos los anuncios
- **Create**: `POST /panel/ad/create/` → Crea un anuncio
- **Update**: `POST /panel/ad/edit/<id>/` → Actualiza un anuncio
- **Delete**: `POST /panel/ad/delete/<id>/` → Elimina un anuncio

## Ventajas de esta Estructura

1. **Separación de responsabilidades**: Cada capa tiene una función clara
2. **Escalabilidad**: Fácil agregar más servicios sin tocar vistas
3. **Testing**: Los servicios se pueden probar independientemente
4. **Validación centralizada**: La lógica de negocio está en `services/`
5. **Mantenimiento**: Cambios en la BD solo afectan a los servicios
6. **Reusabilidad**: Los servicios pueden usarse desde otras vistas o APIs

## Agregar Nueva Funcionalidad

### Ejemplo: Crear una nueva operación en Category

1. **Agregar función en `panel/services/category.py`**:
```python
def get_category_by_id(category_id):
    """Get a single category by ID."""
    try:
        return Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise ValueError('Category not found')
```

2. **Usar en `panel/view_modules/category.py`**:
```python
from panel.services.category import get_category_by_id

@login_required
def category_detail(request, category_id):
    try:
        category = get_category_by_id(category_id)
        return render(request, 'category/detail.html', {'category': category})
    except ValueError as e:
        return render(request, 'error.html', {'error': str(e)})
```

3. **Agregar ruta en `panel/urls.py`**:
```python
path('category/<int:category_id>/', views.category_detail, name='category_detail'),
```

## Próximos Pasos Recomendados

1. **Agregar formularios en templates** con validación frontend
2. **Implementar búsqueda y filtrado** en los servicios
3. **Agregar permisos** (solo admin puede crear categorías)
4. **Crear APIs REST** para el frontend (usando DRF)
5. **Agregar logs** para auditoría
