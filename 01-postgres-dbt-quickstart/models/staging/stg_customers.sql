{{
  config(
    materialized='view'
  )
}}

with source as (
    select * from {{ ref('raw_customers') }}
),

staged as (
    select
        customer_id,
        customer_name,
        lower(email) as email,
        created_at,
        status,
        case 
            when status = 'active' then true 
            else false 
        end as is_active,
        date_trunc('day', created_at) as created_date
    from source
)

select * from staged 