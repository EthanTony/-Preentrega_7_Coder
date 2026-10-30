# Preentrega 7 - Repositorio base de Django

## Descripción

Este repositorio contiene la estructura inicial de un proyecto web para un blog
desarrollado con Django. Corresponde a la Preentrega 7 de Coderhouse y establece
la base técnica del proyecto: la configuración del proyecto `blog_project`, la
creación de la aplicación `posts` y los archivos necesarios para su instalación,
ejecución y control de versiones.

En esta entrega no se implementan modelos, vistas, templates, formularios ni
ninguna otra funcionalidad del blog. El alcance se limita a dejar un proyecto
Django limpio y funcional.

## Tecnologías

- Python 3.14
- Django 5.2.18 (LTS)
- Git
- GitHub

## Estructura del proyecto

```text
blog_django/
│
├── .venv/                  # Entorno virtual local (no se versiona)
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── blog_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── posts/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations/
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py
```

## Instalación

### 1. Clonar el repositorio

```powershell
git clone <URL_DEL_REPOSITORIO>
```

> El marcador `<URL_DEL_REPOSITORIO>` se reemplazará por la URL definitiva
> cuando el repositorio remoto esté publicado.

### 2. Acceder al directorio del proyecto

```powershell
cd blog_django
```

### 3. Crear el entorno virtual

Windows PowerShell:

```powershell
python -m venv .venv
```

Linux/macOS:

```bash
python3 -m venv .venv
```

### 4. Activar el entorno virtual

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

> Si PowerShell bloquea la activación por la política de ejecución, se puede
> habilitar temporalmente solo para la sesión actual con
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`. Esto no modifica
> la configuración global del sistema.

### 5. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

### 6. Ejecutar las migraciones

```powershell
python manage.py migrate
```

### 7. Iniciar el servidor de desarrollo

```powershell
python manage.py runserver
```

El servidor estará disponible en:

`http://127.0.0.1:8000/`

Para detenerlo, presionar `Ctrl + C`.

### Comandos completos para Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Comandos completos para Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Aplicación posts

`posts` es la aplicación destinada a alojar posteriormente los componentes
relacionados con las publicaciones del blog, como modelos, vistas, formularios y
templates.

En esta entrega solamente se crea y se registra la aplicación en
`INSTALLED_APPS` mediante `posts.apps.PostsConfig`. Todavía no se implementa
ninguna funcionalidad.
