select
    user_id,
    name as full_name,
    email,
    city,  
    register_date::date as registration_date
from {{ source('raw_ecommerce', 'users') }}