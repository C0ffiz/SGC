# SGC — Condominium Management System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0.3-green?logo=django)](https://www.djangoproject.com/)
[![MySQL](https://img.shields.io/badge/Database-MySQL-orange?logo=mysql)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

A full-stack web application for residential condominium management, built with Django. Covers resident and unit management, financial control, asset tracking, space reservations, and more — across 21 modules with full CRUD operations.

---

## Features

### 🏢 Condominium & Residents
- Multi-condominium support via subdomain middleware
- Condominiums, blocks, and units management
- Residents and owners registration
- Vehicles, pets, and parking spots

### 👥 Operations
- Staff management
- Move-in/move-out scheduling
- Common area reservations
- Mail and deliveries tracking
- Incident reports with document uploads
- Benefits management

### 💰 Financial
- Accounts payable and receivable
- Bank account and cash register control
- Budget forecasting (revenue and expenses)
- Budget vs. actual comparison reports
- Financial chart visualizations
- Custom chart of accounts

### 🏛️ Asset Management
- Asset registry with categorization
- Administrative space management

### 🔐 Authentication & Access
- Custom authentication backend
- User accounts linked to specific condominiums
- Subdomain middleware for multi-tenancy
- Session-based access control

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.8+, Django 5.0.3 |
| Database | MySQL |
| Frontend | HTML5, CSS3, JavaScript, Bootstrap |
| Auth | Custom Django auth backend + middleware |
| Server | Django WSGI / ASGI |

---

## Project Structure

```
SGC/
├── App_SGC/                    # Main application
│   ├── models.py               # All data models
│   ├── views.py                # Views and business logic
│   ├── middleware.py           # Subdomain middleware
│   ├── auth_backends/          # Custom authentication backend
│   ├── templatetags/           # Custom template filters
│   ├── migrations/             # Database migrations
│   ├── management/commands/    # Custom management commands
│   │   ├── populate_db.py      # Seed database with test data
│   │   ├── reset_db.py         # Reset database
│   │   └── password_migration.py
│   └── templates/              # HTML templates (21 modules)
│       ├── login/
│       ├── usuarios/
│       ├── condominios/
│       ├── condominos/
│       ├── moradores/
│       ├── blocos/
│       ├── unidades/
│       ├── veiculos/
│       ├── colaboradores/
│       ├── garagens/
│       ├── mudancas/
│       ├── ocorrencias/
│       ├── correspondencias/
│       ├── espacos/
│       ├── espacosAdm/
│       ├── reservas/
│       ├── pets/
│       ├── patrimonio/
│       ├── tiposPatrimonio/
│       ├── beneficios/
│       └── [financial modules]/
│
├── Projeto_SGC/                # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── static/                     # CSS, JS, and static assets
├── documentos_ocorrencias/     # Incident document uploads
└── manage.py
```

---

## Installation

### Prerequisites

- Python 3.8+
- MySQL Server
- pip

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/C0ffiz/SGC.git
cd SGC
```

2. **Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install django==5.0.3
pip install mysqlclient
```

4. **Create the MySQL database**
```sql
CREATE DATABASE SGC CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. **Configure database credentials**

Edit `Projeto_SGC/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'SGC',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

6. **Run migrations**
```bash
python manage.py migrate
```

7. **Create a superuser**
```bash
python manage.py createsuperuser
```

8. **Seed the database with test data** *(optional)*
```bash
python manage.py populate_db
```

9. **Start the development server**
```bash
python manage.py runserver
```

10. **Access the app**

Open `http://localhost:8000` in your browser.

---

## Multi-Condominium Support

The system supports multiple condominiums through a custom subdomain middleware. Configure the allowed hosts in `settings.py`:

```python
ALLOWED_HOSTS = ['condominio-a.sgc.com', 'condominio-b.sgc.com', 'sgc.com', 'localhost']
```

---

## Security Notes

Before deploying to production:

- Replace the `SECRET_KEY` in `settings.py` with a secure value
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS` appropriately
- Use environment variables for sensitive credentials
- Enable HTTPS

---

## License

This project is licensed under the [MIT License](LICENSE).
