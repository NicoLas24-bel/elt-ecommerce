# 🛒 E-Commerce Modern Data Stack (Pipeline ELT)

## 📝 Descripción del Proyecto
Este proyecto implementa una arquitectura ELT (Extract, Load, Transform) completa, simulando el flujo de datos de un E-Commerce moderno. El sistema genera transacciones simuladas, las ingesta en estado crudo en un Data Warehouse y aplica modelos de transformación estructurados por capas para finalmente disponibilizar la información en un dashboard de Inteligencia de Negocios (BI).

---

## 🚀 Stack Tecnológico

| Capa | Herramienta |
|---|---|
| Generación y Extracción (EL) | Python · Pandas · Faker · SQLAlchemy |
| Data Warehouse | PostgreSQL 15 |
| Transformación y Modelado (T) | dbt Core (`dbt-postgres`) |
| Capa de Visualización (BI) | Metabase |
| Infraestructura y Orquestación | Docker & Docker Compose |

---

## 🏗️ Arquitectura de Datos

```
generar_datos.py
      │
      ▼
 PostgreSQL (esquema: raw)
  ├── raw.users
  ├── raw.products
  └── raw.orders
      │
      ▼  dbt run
 PostgreSQL (esquema: staging)
  ├── stg_users    (vista)
  ├── stg_products (vista)
  └── stg_orders   (vista)
      │
      ▼  dbt run
 PostgreSQL (esquema: marts)
  └── fct_sales    (tabla)
      │
      ▼
   Metabase → Dashboards / KPIs
```

1. **Ingesta (Raw):** `generar_datos.py` crea 1.000 usuarios, 100 productos y 5.000 órdenes simuladas con Faker y los carga en el esquema `raw` de PostgreSQL.
2. **Staging (dbt):** Modelos SQL materializados como **vistas** que leen desde `raw`, estandarizan tipos, limpian nulos y renombran columnas.
3. **Marts (dbt):** Modelo `fct_sales` materializado como **tabla**, que cruza las entidades para construir una tabla de hechos desnormalizada y lista para análisis.
4. **Visualización:** Metabase se conecta al esquema `marts` para renderizar KPIs de negocio.

---

## 📋 Prerrequisitos

Antes de comenzar, asegurate de tener instalado:

- [Docker](https://docs.docker.com/get-docker/) y Docker Compose
- Python **3.9+**
- `pip` y soporte para entornos virtuales (`venv`)

---

## ⚙️ Instrucciones de Ejecución Local (paso a paso)

### 1. Clonar el repositorio

```bash
git clone https://github.com/NicoLas24-bel/elt-ecommerce.git
cd elt-ecommerce
```

### 2. Crear y activar el entorno virtual de Python

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar las dependencias de Python

```bash
pip install -r requirements.txt
```

> **Dependencias instaladas:** `faker`, `pandas`, `sqlalchemy`, `psycopg2-binary`, `dbt-postgres`

### 4. Levantar la infraestructura con Docker

```bash
docker compose up -d
```

Esto levanta dos contenedores en la red `elt_network`:
- **`elt_postgres`** → PostgreSQL en el puerto `5433`
- **`elt_metabase`** → Metabase en el puerto `3000`

Verificá que ambos estén corriendo:

```bash
docker compose ps
```

### 5. Generar e ingestar los datos crudos (Extract & Load)

```bash
python generar_datos.py
```

Esto crea el esquema `raw` en PostgreSQL y carga las tablas `users`, `products` y `orders`.

Salida esperada:
```
1. Generando datos de clientes...
2. Conectando a PostgreSQL y creando esquema 'raw'...
3. Cargando datos en PostgreSQL...
Datos generados y cargados en PostgreSQL con éxito.
```

### 6. Configurar el perfil de dbt

dbt necesita un archivo `profiles.yml` para saber cómo conectarse a la base de datos. Este archivo **no se versiona** (está en `.gitignore`) por razones de seguridad. Debés crearlo manualmente en tu máquina.

```bash
mkdir -p ~/.dbt
```

Luego creá/editá el archivo `~/.dbt/profiles.yml` con el siguiente contenido:

```yaml
mi_proyecto_dbt:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      port: 5433
      user: dbt_user
      password: dbt_1464
      dbname: ecom_warehouse
      schema: staging
      threads: 1
```

### 7. Ejecutar los modelos de transformación con dbt (Transform)

Ingresá al directorio del proyecto dbt:

```bash
cd mi_proyecto_dbt
```

Verificá la conexión a la base de datos:

```bash
dbt debug
```

Ejecutá todos los modelos:

```bash
dbt run
```

Esto materializa:
- `staging.stg_users`, `staging.stg_products`, `staging.stg_orders` → como **vistas**
- `marts.fct_sales` → como **tabla**

*(Opcional)* Ejecutá los tests de calidad de datos:

```bash
dbt test
```

### 8. Acceder a Metabase (Visualización BI)

Abrí tu navegador y accedé a: **[http://localhost:3000](http://localhost:3000)**

En el primer acceso, Metabase te pedirá configurar una cuenta de administrador. Luego añadí una nueva base de datos con los siguientes datos:

| Campo | Valor |
|---|---|
| Tipo | PostgreSQL |
| Host | `localhost` |
| Puerto | `5433` |
| Base de datos | `ecom_warehouse` |
| Usuario | `dbt_user` |
| Contraseña | `dbt_1464` |

Una vez conectada, explorá el esquema `marts` para crear dashboards sobre `fct_sales`.

---

## 🔌 Credenciales de Conexión

| Servicio | Host | Puerto | Base de datos | Usuario | Contraseña |
|---|---|---|---|---|---|
| PostgreSQL | `localhost` | `5433` | `ecom_warehouse` | `dbt_user` | `dbt_1464` |
| Metabase UI | `localhost` | `3000` | — | — | — |

---

## 🗂️ Estructura del Proyecto

```
elt_ecommerce/
├── docker-compose.yml        # Define servicios de PostgreSQL y Metabase
├── generar_datos.py          # Script EL: genera y carga datos en raw
├── requirements.txt          # Dependencias de Python
├── mi_proyecto_dbt/          # Proyecto dbt (capa Transform)
│   ├── dbt_project.yml       # Configuración del proyecto dbt
│   └── models/
│       ├── staging/          # Modelos de limpieza y estandarización
│       │   ├── sources.yml
│       │   ├── stg_users.sql
│       │   ├── stg_products.sql
│       │   └── stg_orders.sql
│       └── marts/            # Modelos analíticos finales
│           └── fct_sales.sql
└── README.md
```

---

## 🛑 Detener el entorno

```bash
docker compose down
```

Para detener y **eliminar los volúmenes** (borra todos los datos de PostgreSQL):

```bash
docker compose down -v