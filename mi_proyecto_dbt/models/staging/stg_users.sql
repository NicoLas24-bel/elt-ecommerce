select
    user_id,
    nombre as full_name,
    email,
    ciudad as city,
    fecha_registro::date as registration_date
from {{ source('raw_ecommerce', 'users') }}