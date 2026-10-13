# 🛒 E-Commerce Modern Data Stack (Pipeline ELT)

## 📝 Descripción del Proyecto
Este proyecto implementa una arquitectura ELT (Extract, Load, Transform) completa, simulando el flujo de datos de un E-Commerce moderno. El sistema genera transacciones transaccionales simuladas, las ingesta en estado crudo en un Data Warehouse y aplica modelos de transformación estructurados por capas para finalmente disponibilizar la información en un dashboard de Inteligencia de Negocios (BI).

## 🚀 Stack Tecnológico
* **Generación y Extracción (EL):** Python (Pandas, Faker, SQLAlchemy).
* **Data Warehouse:** PostgreSQL.
* **Transformación y Modelado (T):** dbt (Data Build Tool) Core.
* **Capa de Visualización (BI):** Metabase.
* **Infraestructura y Orquestación:** Docker & Docker Compose.

## 🏗️ Arquitectura de Datos
1. **Ingesta (Raw):** Un script de Python genera un volumen de datos relacionales simulados (usuarios, productos y órdenes) y los carga directamente en un esquema `raw` dentro de PostgreSQL.
2. **Capa Staging (dbt):** Modelos SQL materializados como vistas que leen desde `raw`, estandarizan tipos de datos, limpian nulos y renombran columnas al inglés para mantener una convención de desarrollo estándar.
3. **Capa Marts (dbt):** Modelos materializados que cruzan las entidades base para construir una tabla de hechos (`fct_sales`) desnormalizada y optimizada para consultas analíticas.
4. **Capa Semántica y Visualización:** Metabase se conecta directamente al esquema analítico para renderizar métricas clave de negocio (KPIs) como el total de ventas por categoría y el rendimiento de productos.

## ⚙️ Instrucciones de Ejecución Local

### 1. Despliegue de Infraestructura
Se requiere tener Docker instalado. Ejecuta el siguiente comando para levantar los servicios de PostgreSQL y Metabase en una red privada:
```bash
docker compose up -d