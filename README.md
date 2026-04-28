# MotoTaller — Sistema de Gestión

Aplicación web Django + PostgreSQL para taller de motos. Incluye sitio público y panel administrativo.

## Stack

- **Backend:** Django 5.2, Python 3.11+
- **Base de datos:** PostgreSQL
- **Frontend:** Tailwind CSS (CDN), HTML vanilla
- **PDFs:** WeasyPrint
- **Config:** python-decouple

## Estructura

```
apps/
  publico/   → Landing pública (servicios, contacto, ubicación)
  clientes/  → CRUD de clientes con validación de RUT chileno
  boletas/   → Boletas con ítems, IVA automático y descarga PDF
  caja/      → Apertura/cierre diario y movimientos en tiempo real
  finanzas/  → Dashboard con balance y gráficos mensuales
```

## Setup rápido

```bash
# 1. Clonar y entrar al proyecto
git clone <repo> && cd Motos-

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de PostgreSQL

# 4. Base de datos
createdb motos_db
python manage.py makemigrations
python manage.py migrate

# 5. Datos de ejemplo (opcional)
python manage.py loaddata apps/publico/fixtures/servicios.json
python manage.py loaddata apps/clientes/fixtures/clientes_demo.json

# 6. Superusuario
python manage.py createsuperuser

# 7. Servidor
python manage.py runserver
```

## URLs

| URL | Descripción |
|-----|-------------|
| `/` | Landing pública |
| `/login/` | Acceso al panel |
| `/dashboard/` | Panel principal con KPIs |
| `/clientes/` | Gestión de clientes |
| `/boletas/` | Boletas y PDFs |
| `/caja/` | Caja diaria |
| `/finanzas/` | Dashboard financiero |
| `/django-admin/` | Admin Django |

## Módulos

### Clientes
- Registro con nombre, RUT (validación mod. 11), teléfono, correo, dirección
- Búsqueda y paginación
- Historial de boletas por cliente

### Boletas
- Numeración correlativa automática
- Ítems de tipo servicio o repuesto
- Subtotal calculado automáticamente (JS en tiempo real)
- IVA 19% automático
- PDF descargable con WeasyPrint
- Estados: borrador → emitida → pagada / anulada

### Caja
- Una sesión por día (apertura/cierre)
- Movimientos: ingreso, egreso, retiro
- Saldo en tiempo real = apertura + ingresos - egresos
- Historial completo de cajas anteriores

### Finanzas
- Balance mensual y anual
- Gráfico de ingresos vs egresos últimos 6 meses
- Datos extraídos de los movimientos de caja
