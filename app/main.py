import uuid
import json
import random
import string
import datetime
import psycopg2
import streamlit as st




def execute(payload: dict, event: str=None):
    query = """
        CREATE SCHEMA IF NOT EXISTS dbt_raw_data;
        CREATE TABLE IF NOT EXISTS dbt_raw_data.app_events
        (JSON_DATA VARCHAR, _ELT_INSERT_TIMESTAMP TIMESTAMP DEFAULT NOW());
        INSERT INTO dbt_raw_data.app_events VALUES
        ( $${data}$$ )
        """
    conn = psycopg2.connect(
        database="dbtdb",
        user="dbtuser",
        password="pssd",
        host="postgres-dbt",
        port='5432'
    )
    
    cursor = conn.cursor()
    try:
        cursor.execute(query.format(data=json.dumps(payload, default= str)))
        conn.commit()
        st.write(f'Events ingested successfull for event: {event}')
    except (Exception, psycopg2.DatabaseError) as error:
        st.write(f'An error occurred: {error}')
        conn.rollback()
        cursor.close()


def login_events():
    st.write('Performing login activity...')
    payload = {
        "ID": uuid.uuid4(),
        "UserName":  ''.join(random.choice(string.ascii_letters) for i in range(5)),
        "EventCategory": "AppLog",
        "EventName" : "LoginEvent",
        "Message": "Logged in successfully",
        "Error": random.choice(["Invalid Credentials", ""]),
        "Datetime":  datetime.datetime.now().strftime('%d/%m/%Y')
    }
    execute(event='LoginEvent', payload=payload)


def register_events():
    st.write('Performing register activity...')

    payload = {
        "ID": uuid.uuid4(),
        "UserName":  ''.join(random.choice(string.ascii_letters) for i in range(5)),
        "EventCategory": "AppLog",
        "EventName" : "RegisterEvent",
        "Message": "Registered Successfully",
        "Error": "",
        "Datetime":  datetime.datetime.now().strftime('%d/%m/%Y')
    }
    execute(event='RegisterEvent', payload=payload)


def purchase_events():
    st.write('Performing Purchase activity...')

    payload = {
        "ID": uuid.uuid4(),
        "UserName":  ''.join(random.choice(string.ascii_letters) for i in range(5)),
        "EventCategory": "AppLog",
        "EventName" : "PurchaseEvent",
        "Message": "Item Purchased successfully",
        "Error": random.choice(["Payment Failed", ""]),
        "Datetime":  datetime.datetime.now().strftime('%d/%m/%Y')
    }
    execute(event='PurchaseEvent', payload=payload)


def generic_exception(event, err):
    st.write(f'exception occurred: {err}')

    payload= {
        "ID": uuid.uuid4(),
        "UserName":  ''.join(random.choice(string.ascii_letters) for i in range(5)),
        "EventCategory": "Generic_Exception",
        "EventName" : event,
        "Message": f"Events ingestion failed with error{err}",
        "Error": random.choice(["Payment Failed", ""]),
        "Datetime":  datetime.datetime.now().strftime('%d/%m/%Y')
    }
    execute(event='PurchaseEvent', payload=payload)
    

option = st.selectbox(
        'Activity to perform to create events',
        ('LOGIN', 'REGISTER', 'PURCHASE')
    )

button = st.button("Ingest Events")
if button:
    if option == 'LOGIN':
        try:
            login_events()
        except Exception as err:
            st.write(err)
            generic_exception('LoginEvent', err) 

    elif option == 'REGISTER':
        try:
            register_events()
        except Exception as err:
            st.write(err)
            generic_exception('RegisterEvent', err) 

    elif option == 'PURCHASE':
        try:
            purchase_events()
        except Exception as err:
            st.write(err)
            generic_exception('PurchaseEvent', err)
