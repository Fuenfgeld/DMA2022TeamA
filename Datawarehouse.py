# -*- coding: utf-8 -*-
"""ETL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/Fuenfgeld/DMA2022TeamA/blob/main/Datawarehouse.ipynb
"""

#Erstellen der Quelldatenbank 
import requests
exec(requests.get('https://raw.githubusercontent.com/Fuenfgeld/DMA2022TeamA/main/quelldatenbank.py').text)

# Initialisierung der Datawarehouse-Tabellen:
Datawh_Tabellen = {}

#Erstellen der Tabellen mit Schlüsseln
Datawh_Tabellen['Zentrum'] = """
  create table Zentrum(
    PATIENT_ID VARCHAR REFERENCES dimPATIENT(ID),
    ENCOUNTER_ID VARCHAR REFERENCES dimENCOUNTERS(ID),
    OBSERVATION_ID INTEGER REFERENCES dimOBSERVATIONS(ID),
    PROCEDURE_DATE VARCHAR REFERENCES dimPROCEDURE(DATE),
    PROCEDURE_CODE VARCHAR REFERENCES dimPROCEDURE(CODE),
    CONDITIONS_CODE VARCHAR REFERENCES dimCONDITIONS(CODE)
  );
"""

Datawh_Tabellen['dimObservations'] = """
  create table if not exists dimObservations(
    ID VARCHAR PRIMARY KEY,
    CODE VARCHAR,
    DESCRIPTION VARCHAR,
    VALUE VARCHAR,
    UNITS VARCHAR
  );
"""

Datawh_Tabellen['dimEncounters'] = """
  create table if not exists dimEncounters(
    ID VARCHAR PRIMARY KEY,
    START TIMESTAMP,
    STOP TIMESTAMP,
    ENCOUNTERCLASS VARCHAR,
    CODE VARCHAR,
    DESCRIPTION VARCHAR
  );
"""

Datawh_Tabellen['dimProcedures'] = """
  create table if not exists dimProcedures(
    DATE TIMESTAMP,
    PATIENT_ID VARCHAR,
    ENCOUNTER_ID VARCHAR,
    CODE VARCHAR,
    DESCRIPTION VARCHAR,
    PRIMARY KEY (DATE, PATIENT_ID, ENCOUNTER_ID, CODE)
  );
"""

Datawh_Tabellen['dimConditions'] = """
  create table if not exists dimConditions(
    PATIENT_ID VARCHAR,
    ENCOUNTER_ID,
    CODE VARCHAR,
    DESCRIPTION VARCHAR,
    PRIMARY KEY (PATIENT_ID, ENCOUNTER_ID, CODE)
  );
"""

Datawh_Tabellen['dimPatients'] = """
  create table if not exists dimPatients(
    ID VARCHAR PRIMARY KEY,
    DATASET_ORIGIN VARCHAR
  );
"""

#Schreiben der Tabellen in eine Datenbank 
import sqlite3
def connect_to_db(db_file):
    sqlite3_conn = None
    try:
        sqlite3_conn = sq.connect(db_file)
        return sqlite3_conn

    except Error as err:
        print(err)

        if sqlite3_conn is not None:
            sqlite3_conn.close()
  
conn_dwh = sqlite3.connect('Datawarehouse.db')
if conn_dwh is not None:
        cursor_dwh = conn_dwh.cursor()
        for name in Datawh_Tabellen.keys():
          print (name)
          cursor_dwh.execute(Datawh_Tabellen[name])

else:
        print('Connection to database failed')

#Einfügen der Werte in Zentrum:
Zentrum = pd.read_sql_query("""
SELECT t4.patient_id,
       t4.encounter_id,
       t4.observation_id,
       t4.procedure_date,
       t4.procedure_code,
       t5.code AS CONDITIONS_CODE
FROM   (SELECT t2.patient_id,
               t2.encounter_id,
               t2.observation_id,
               t3.date AS PROCEDURE_DATE,
               t3.code AS PROCEDURE_CODE
        FROM   (SELECT encounters.patient_id AS PATIENT_ID,
                       encounters.id         AS ENCOUNTER_ID,
                       t1.id                 AS OBSERVATION_ID               
                FROM   encounters
                       LEFT JOIN (SELECT id,
                                         patient_id,
                                         encounter_id
                                  FROM   observations
                                  WHERE  observations.code IN (
                                         "8480-6", "8462-4", "9279-1",
                                         "8867-4",
                                         "3569", "8310-5", "1975-2",
                                         "1920-8",
                                         "1742-6", "6768-6", "33914-3",
                                         "2885-2"
                                         ,
                                         "3094-0", "94531-1","2703-7", "2708-6")) t1
                              ON encounters.patient_id = t1.patient_id
                                 AND encounters.id = t1.encounter_id) t2
               LEFT JOIN (SELECT date,
                                 code,
                                 patient_id,
                                 encounter_id
                          FROM   procedures) t3
                      ON t2.patient_id = t3.patient_id
                         AND t2.encounter_id = t3.encounter_id) t4
       LEFT JOIN (SELECT patient_id,
                         encounter_id,
                         code
                  FROM   conditions
                  WHERE  code IN ( "840544004", "840539006" )) t5
              ON t4.patient_id = t5.patient_id
                 AND t4.encounter_id = t5.encounter_id 
;""", conn
  )
Zentrum.to_sql(name = 'Zentrum', con=conn_dwh, if_exists='append', index=False)
Zentrum.head(3)

#Einfügen der Werte in Observations
dimObservations = pd.read_sql_query("""
Select ID, CODE, DESCRIPTION, VALUE, UNITS from observations
where observations.code in ("8480-6","8462-4","9279-1","8867-4","3569","8310-5","1975-2","1920-8","1742-6","6768-6","33914-3","2885-2","3094-0","94531-1", "2703-7", "2708-6")
;""", conn
  )

dimObservations.to_sql(name = 'dimObservations', con=conn_dwh, if_exists='append', index=False)
dimObservations.head(3)

#Einfügen der Werte in Encounters
dimEncounters = pd.read_sql_query("""
Select ID, START, STOP, ENCOUNTERCLASS, CODE, DESCRIPTION from encounters
;""", conn
  )

dimEncounters.to_sql(name = 'dimEncounters', con=conn_dwh, if_exists='append', index=False)

dimEncounters.head(3)

#Einfügen der Werte in Procedures
dimProcedures = pd.read_sql_query("""
select DATE,PATIENT_ID, ENCOUNTER_ID, CODE, DESCRIPTION from procedures
;""", conn
  )

dimProcedures.to_sql(name = 'dimProcedures', con=conn_dwh, if_exists='append', index=False)

dimProcedures.head(3)

#Einfügen der Werte in Conditions
dimConditions = pd.read_sql_query("""
select PATIENT_ID, CODE, DESCRIPTION, ENCOUNTER_ID from conditions
;""", conn
  )

dimConditions.to_sql(name = 'dimConditions', con=conn_dwh, if_exists='append', index=False)

dimConditions.head(3)

#Einfügen der Werte in Patients
dimPatients = pd.read_sql_query("""
select ID, DATASET_ORIGIN FROM patients
;""", conn
  )

dimPatients.to_sql(name = 'dimPatients', con=conn_dwh, if_exists='append', index=False)

dimPatients.head(3)