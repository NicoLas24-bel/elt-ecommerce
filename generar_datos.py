import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

# Inicializamos Faker (ejemplo: 'es_CL' para español de Chile)
fake = Faker('es_CL')

# Configuramos la cantidad de datos a generar

num_customers = 1000
num_products = 100
num_orders = 5000

print("1. Generando datos de clientes...")

# ---- Generar datos de clientes --------

users = []
for i in range(1, num_customers + 1):
    user = {
        'user_id': i,
        'name': fake.name(),
        'email': fake.email(),
        'city': fake.city(),
        'register_date': fake.date_between(start_date='-5y', end_date='today')
    }
    users.append(user)

df_users = pd.DataFrame(users)

# ---- Generar datos de productos --------

categories = ['Electrónica', 'Ropa', 'Hogar', 'Juguetes', 'Libros', 'Deportes']
products = []
for i in range(1, num_products + 1):
    product = {
        'product_id': i,
        'name': fake.word().capitalize() + ' ' + fake.word().capitalize(),
        'category': random.choice(categories),
        'price': round(random.uniform(10.0, 1000.0), 2)
    }
    products.append(product)

df_products = pd.DataFrame(products)


# --- Generar datos de órdenes --------
orders = []
estados = ['completada', 'completada', 'completada', 'cancelada', 'reembolsada']
for i in range(1, num_orders + 1):
    product = random.choice(products)
    cantidad = random.randint(1, 5)
    order = {
        'order_id': i,
        'user_id': random.randint(1, num_customers),
        'product_id': product['product_id'],
        'order_date': fake.date_time_between(start_date='-1y', end_date='now'),
        'cuantity': cantidad,
        'total_price': round(product['price'] * cantidad, 2),
        'status': random.choice(estados)
    }
    orders.append(order)

df_orders = pd.DataFrame(orders)


print("2. Conectando a PostgreSQL y creando esquema 'raw'...")
# Tu conexión local por el puerto 5433
engine = create_engine('postgresql+psycopg2://dbt_user:dbt_1464@localhost:5433/ecom_warehouse')

# Crear esquema 'raw' si no existe
# En ELT , cargamos los datos tal cual llegan en un esquema raw, sin transformaciones
with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
    conn.commit()

print("3. Cargando datos en PostgreSQL...")
# Cargar datos en PostgreSQL en el esquema 'raw'
df_users.to_sql('users', engine, schema='raw', if_exists='replace', index=False)
df_products.to_sql('products', engine, schema='raw', if_exists='replace', index=False)
df_orders.to_sql('orders', engine, schema='raw', if_exists='replace', index=False)

print("Datos generados y cargados en PostgreSQL con éxito.")