{{ 
    config(
        materialized='table'
        )
}}

WITH EVENTS_DATA_INDICATOR AS (
    SELECT 
        USERNAME,
        CASE
            WHEN COALESCE(LOGIN_COUNT, 0) > 0 THEN 'HAS_LOGGED_IN'
            WHEN COALESCE(PURCHASE_COUNT, 0) > 0 THEN 'HAS_PURCHASES'
            WHEN COALESCE(PURCHASE_COUNT, 0) = 0 AND COALESCE(LOGIN_COUNT, 0) > 0 THEN 'HAS_LOGGED_IN_BUT_NO_PUECHASES'
        END AS TYPE
    FROM 
        {{ source('dwh', 'user_metrics') }}
)

, FINAL AS (
    SELECT *
    FROM EVENTS_DATA_INDICATOR
)

SELECT * FROM FINAL