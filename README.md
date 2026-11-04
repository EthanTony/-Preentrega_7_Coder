# Blog Django

## Descripción

Blog web desarrollado con Django como proyecto final del curso de Python. La
aplicación permite a las personas registrarse, iniciar sesión y publicar
contenido con texto e imágenes opcionales. Incluye un listado público de
publicaciones, búsqueda por título y contenido, y gestión completa de cada
publicación por parte de su autor o del personal del sitio.

## Tecnologías

- Python 3.14.7
- Django 5.2.18 (LTS)
- SQLite
- Pillow 13.0.0
- python-decouple 3.8
- Bootstrap 5.3.3 (CDN)
- HTML5, CSS3 y JavaScript
- Git y GitHub

## Funcionalidades

- Listado público de publicaciones con paginación.
- Vista de detalle de cada publicación.
- Creación, edición y eliminación de publicaciones.
- Carga opcional de imágenes para las publicaciones.
- Publicaciones sin imagen con visualización controlada.
- Registro de usuarios mediante `UserCreationForm`.
- Inicio y cierre de sesión (el cierre de sesión se realiza por `POST`).
- Restricción de creación, edición y eliminación según autenticación y autoría.
- El autor de una publicación o un miembro del staff puede editarla o eliminarla.
- Búsqueda por título y contenido con `Q` e `icontains`.
- Mensaje cuando la búsqueda no encuentra coincidencias.
- Navegación y acciones que cambian según el usuario autenticado.
- Panel de administración con el modelo `Post` registrado.
- Interfaz responsiva con Bootstrap 5 y estilos propios.
- Mensajes de confirmación y error.

## Requisitos previos

- Python 3.14 (versión probada: 3.14.7).
- Git.
- PowerShell en Windows o una terminal en Linux/macOS.

## Estructura del proyecto

```text
blog_django/
├── .env.example
├── .gitignore
├── README.md
├── manage.py
├── requirements.txt
├── blog_project/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── posts/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations/
│   │   └── 0001_initial.py
│   ├── models.py
│   ├── templates/posts/
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── static/css/styles.css
└── templates/
    ├── 403.html
    ├── base.html
    ├── partials/
    └── registration/
```

## Instalación

### 1. Clonar el repositorio

```powershell
git clone https://github.com/EthanTony/-Preentrega_7_Coder
cd blog_django
```

### 2. Crear y activar el entorno virtual

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

> Si PowerShell bloquea la activación por la política de ejecución, se puede
> habilitar temporalmente solo para la sesión actual con
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.

### 3. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

## Configuración de variables de entorno

El proyecto lee `SECRET_KEY`, `DEBUG` y `ALLOWED_HOSTS` desde un archivo `.env`
utilizando `python-decouple`.

1. Copiar el archivo de ejemplo:

   Windows PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

   Linux/macOS:

   ```bash
   cp .env.example .env
   ```

2. Generar una `SECRET_KEY` nueva:

   ```powershell
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. Editar `.env` y reemplazar el valor de `SECRET_KEY` por la clave generada:

   ```env
   SECRET_KEY=tu-clave-generada
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   ```

> El archivo `.env` contiene credenciales locales y está excluido de Git.
> Nunca se debe publicar. El archivo `.env.example` sí se versiona y no contiene
> secretos reales.

## Migraciones

Aplicar las migraciones de Django y de la aplicación `posts`:

```powershell
python manage.py migrate
```

Comprobar que no existan cambios de modelo pendientes:

```powershell
python manage.py makemigrations --check --dry-run
```

## Crear un superusuario

Para acceder al panel de administración:

```powershell
python manage.py createsuperuser
```

Luego iniciar sesión en `http://127.0.0.1:8000/admin/`.

## Ejecutar el servidor

```powershell
python manage.py runserver
```

La aplicación estará disponible en:

- Blog: `http://127.0.0.1:8000/`
- Administración: `http://127.0.0.1:8000/admin/`<
- Login: `http://127.0.0.1:8000/accounts/login/`
- Registro: `http://127.0.0.1:8000/accounts/register/`

Durante `DEBUG=True`, Django sirve los archivos multimedia subidos desde
`MEDIA_ROOT`. En producción se debe configurar un servidor web o de archivos
para servir `MEDIA_ROOT` y `STATIC_ROOT`.

## Ejecutar las pruebas

```powershell
python manage.py check
python manage.py test
```

Las pruebas cubren modelos, listado, detalle, búsqueda, creación, edición,
eliminación, permisos de autoría, autenticación, imágenes y publicaciones sin
imagen.

## Rutas principales


| Ruta | Descripción |
|---|---|
| `/` | Listado de publicaciones |
| `/posts/new/` | Crear publicación (requiere login) |
| `/posts/<id>/` | Detalle de publicación |
| `/posts/<id>/edit/` | Editar publicación (autor o staff) |
| `/posts/<id>/delete/` | Eliminar publicación (autor o staff) |
| `/accounts/register/` | Registro de usuario |
| `/accounts/login/` | Inicio de sesión |
| `/accounts/logout/` | Cierre de sesión por POST |
| `/admin/` | Panel de administración |

## Comandos completos para Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Editar .env con una SECRET_KEY nueva
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Comandos completos para Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Editar .env con una SECRET_KEY nueva
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Autor

**Bruno Antonio Aguilar Hernández**

Proyecto final del curso de Python.
