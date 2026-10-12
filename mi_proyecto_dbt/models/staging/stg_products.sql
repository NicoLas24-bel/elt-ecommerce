select
    product_id,
    nombre_producto as product_name,
    categoria as category,
    precio::numeric as price
from {{ source('raw_ecommerce', 'products') }}