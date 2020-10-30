Create
        OR replace view ironia_id_single_currency AS
SELECT ironia_id
FROM 
    (SELECT ironia_id,
         count(*) AS cuenta
    FROM 
        (SELECT DISTINCT ironia_id,
         currency
        FROM ironia_data)
        GROUP BY  ironia_id)
    WHERE cuenta = 1; 

CREATE OR REPLACE VIEW ironia_id_date as
SELECT ironia_id
FROM 
    (SELECT ironia_id,
         max(date) AS max_date,
         min(date) AS min_date
    FROM ironia_data
    GROUP BY  ironia_id)
WHERE min_date <= '2010-01-01'
        AND max_date >= '2020-10-01';


create
        OR replace view ironia_id_selected_currencies AS
SELECT ironia_id
FROM 
    (SELECT DISTINCT ironia_id,
         currency
    FROM ironia_data)
WHERE currency in('EUR', 'USD', 'GBP'); 


create or replace view ironia_selected as
SELECT ironia_id
FROM ironia_id_date
WHERE ironia_id IN 
    (SELECT ironia_id
    FROM ironia_id_selected_currencies)
        AND ironia_id IN 
    (SELECT ironia_id
    FROM ironia_id_single_currency);


 create
        OR replace view ironia_data_filtered AS
SELECT ironia_id,
         date,
         nav
FROM ironia_data
WHERE ironia_id IN 
    (SELECT ironia_id
    FROM ironia_selected)
        AND date >= '2010-01-01'; 


create
        OR replace view ironia_selected_100 AS
SELECT ironia_id
FROM ironia_selected
ORDER BY  ironia_id ASC limit 100;

create
        OR replace view ironia_name_selected_100 AS
SELECT DISTINCT ironia_id,
         name
FROM ironia_data
WHERE ironia_id IN 
    (SELECT ironia_id
    FROM ironia_selected_100); 