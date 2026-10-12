select
    order_id,
    user_id,
    product_id,
    fecha_compra::timestamp as order_date,
    cantidad as quantity,
    monto_total::numeric as total_amount,
    estado as order_status
from {{ source('raw_ecommerce', 'orders') }}