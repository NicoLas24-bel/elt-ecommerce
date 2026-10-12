select
    product_id,
    name as product_name,
    category,
    price::numeric as price
from {{ source('raw_ecommerce', 'products') }}