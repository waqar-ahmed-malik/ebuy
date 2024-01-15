{{ 
    config(
        materialized='incremental'
        )
}}

WITH SOURCE_EVENTS_DATA AS (
    SELECT 
        JSON_DATA::JSON->>'ID' as EVENT_ID,
        JSON_DATA::JSON->>'UserName' as EVENT_USERNAME,
        JSON_DATA::JSON->>'EventCategory' as EVENT_CATEGORY,
        JSON_DATA::JSON->>'EventName' as EVENT_NAME,
        JSON_DATA::JSON->>'Message' as EVENT_MESSAGE,
        JSON_DATA::JSON->>'Error' as EVENT_ERROR,
        JSON_DATA::JSON->>'Datetime' as EVENT_DATETIME,
        _ELT_INSERT_TIMESTAMP as EVENT_INSERT_TIMESTAMP,
        NOW() as EVENT_PARSED_TIMESTAMP 
    FROM {{ source('raw', 'app_events') }}

    {% if is_incremental() %}
        where _ELT_INSERT_TIMESTAMP > 
            (
                SELECT 
                    COALESCE(MAX(EVENT_PARSED_TIMESTAMP), '1000-01-01') 
                FROM 
                    {{ this }}
            )
    {% endif %}
)
    
, FINAL AS (
    SELECT *
    FROM SOURCE_EVENTS_DATA
)

SELECT * FROM FINAL