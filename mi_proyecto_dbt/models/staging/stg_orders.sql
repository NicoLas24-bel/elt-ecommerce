select
    order_id,
    user_id,
    product_id,
    order_date::timestamp as order_date,
    cuantity as quantity,
    total_price::numeric as total_amount,
    status as order_status
from {{ source('raw_ecommerce', 'orders') }}