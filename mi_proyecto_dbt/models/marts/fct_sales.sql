-- Usamos la función ref() para referenciar nuestros modelos limpios
with orders as (
    select * from {{ ref('stg_orders') }}
),

users as (
    select * from {{ ref('stg_users') }}
),

products as (
    select * from {{ ref('stg_products') }}
)

-- Unimos todo en una gran tabla de hechos (fact table)
select
    o.order_id,
    o.order_date,
    o.quantity,
    o.total_amount,
    o.order_status,
    
    -- Datos del cliente
    u.user_id,
    u.full_name as customer_name,
    u.city as customer_city,
    
    -- Datos del producto
    p.product_id,
    p.product_name,
    p.category as product_category,
    p.price as unit_price
    
from orders o
left join users u on o.user_id = u.user_id
left join products p on o.product_id = p.product_id
-- Solo queremos analizar ventas exitosas
where o.order_status = 'completada'