{{
  config(
    materialized='table'
  )
}}

with customers as (
    select * from {{ ref('stg_customers') }}
),

final as (
    select
        customer_id,
        customer_name,
        email,
        created_at,
        created_date,
        status,
        is_active,
        case 
            when is_active then 'Active Customer'
            else 'Inactive Customer'
        end as customer_type,
        case 
            when created_date >= current_date - interval '30 days' then 'New'
            when created_date >= current_date - interval '90 days' then 'Recent'
            else 'Established'
        end as customer_segment
    from customers
)

select * from final 