\set agg_top_n 10


drop table if exists assoc_spending_grants;

create table assoc_spending_grants as
    select e.id as entity_id, g.id as transaction_id
    from grants_grant g
    inner join matchbox_entity e
        on to_tsvector('datacommons', g.recipient_name) @@ plainto_tsquery('datacommons', e.name)
    where
        e.type = 'organization';

create index assoc_spending_grants_entity_id on assoc_spending_grants (entity_id);
create index assoc_spending_grants_transaction_id on assoc_spending_grants (transaction_id);


drop table if exists assoc_spending_contracts;

create table assoc_spending_contracts as
    select e.id as entity_id, c.id as transaction_id
    from contracts_contract c
    inner join matchbox_entity e
        on to_tsvector('datacommons', c.vendor_name) @@ plainto_tsquery('datacommons', e.name)
    where
        e.type = 'organization';
        
create index assoc_spending_contracts as assoc_spending_contracts (entity_id);
create index assoc_spending_contracts as assoc_spending_contracts (transaction_id);


drop table if exists agg_spending_org;

create table agg_spending_org as
    with spending_to_org as (
        select entity_id as recipient_entity, recipient_name, 'g' as spending_type, 
                case when fiscal_year % 2 = 0 then fiscal_year else fiscal_year + 1 end as cycle,
                fiscal_year, agency_name, project_description as description, amount_total as amount
        from grants_grant
        inner join assoc_spending_grants on (id = transaction_id)
        
        union all
        
        select entity_id as recipient_entity, vendor_name as recipient_name, 'c' as spending_type,
                case when fiscal_year % 2 = 0 then fiscal_year else fiscal_year + 1 end as cycle,
                fiscal_year, agency_name, contract_description as description, obligated_amount as amount
        from contracts_contract
        inner join assoc_spending_contracts on (id = transaction_id)
    )
    
    select recipient_entity, recipient_name, spending_type, cycle, fiscal_year, agency_name, description, amount
    from (select *, rank() over (partition by recipient_entity, cycle order by amount desc) as rank from spending_to_org) x
    where rank <= :agg_top_n
    
    union all
    
    select recipient_entity, recipient_name, spending_type, -1 as cycle, fiscal_year, agency_name, description, amount
    from (select *, rank() over (partition by recipient_entity order by amount desc) as rank from spending_to_org) x
    where rank <= :agg_top_n;
    
create index agg_spending_org_idx on agg_spending_org (recipient_entity, cycle);
