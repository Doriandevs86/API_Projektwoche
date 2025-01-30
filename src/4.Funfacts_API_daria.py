from getpass import getpass
import psycopg2
import os
import uvicorn
from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel, Field


pw = input('Bitte gib dein Passwort ein:')

def connect_to_db():
    connection = psycopg2.connect(
        host='localhost',
        port=5432,
        user='postgres',
        password=pw,
        dbname='funfact_db'
    )
    return connection


#Header für die API und eine kurze Beschreibung
app = FastAPI(
    title='Fun Facts App',
    summary='Eine API zum Auffinden interessanter Fakten'
)

class Fact(BaseModel):
    title: str = Field(default='Enter fact')
    status: str = Field(default='Nicht gesehen')


# Begrüßung der User
@app.get('/', status_code=status.HTTP_200_OK, tags=['Welcome'])
def greet_user():
     return {'message': 'Hallo Benutzer! Willkommen bei der App „Fun Facts“!'}


# alle Fakten anzeigen
@app.get('/facts', status_code=status.HTTP_200_OK, tags=['Get data'])
def get_all_facts(conn=Depends(connect_to_db)):
    select_query = 'SELECT * FROM facts;'
    cursor = conn.cursor()
    cursor.execute(select_query)
    facts = cursor.fetchall()
    facts_dicts = []

    for fact in facts:
        fact_dicts = {'fact_id': fact[0], 'facts': fact[1], 'status': fact[2]}
        facts_dicts.append(fact_dicts)

    return facts_dicts

# Fakten nach Status filtern
@app.get('/filter', status_code=status.HTTP_200_OK, tags=['Get data'])
def filter_by_status(status: str, conn=Depends(connect_to_db)):

    filter_query = 'SELECT * FROM facts WHERE status = %s'

    tuple = (status, )
    cursor = conn.cursor()
    cursor.execute(filter_query, tuple)
    facts = cursor.fetchall()

    facts_dicts = []

    for fact in facts:
       fact_dicts = {'fact_id': fact[0], 'facts': fact[1], 'status': fact[2]}
       facts_dicts.append(fact_dicts)
    return facts_dicts

# Pfad mit Pfadparameter
@app.get('/facts/{fact_id}/', status_code=status.HTTP_200_OK, tags=['Get data'])
def get_fact(fact_id: int, conn=Depends(connect_to_db)):

    select_query = 'SELECT * FROM facts WHERE fact_id = %s;'

    cursor = conn.cursor()
    cursor.execute(select_query, (fact_id, ))
    facts = cursor.fetchall()

    for fact in facts:
        fact_dict = {'fact_id': fact[0], 'facts': fact[1], 'status': fact[2]}
        if fact_dict['fact_id'] == fact_id:
            return fact_dict



@app.post('/facts/', status_code=status.HTTP_201_CREATED, tags=['Controller'])
def post_new_fact(fact: Fact, conn=Depends(connect_to_db)):
    insertion_query = '''INSERT INTO facts (facts, status)
                         VALUES (%s, %s);'''
    fact_tuple = (fact.facts, fact.status)

    cursor = conn.cursor()
    cursor.execute(insertion_query, fact_tuple)
    conn.commit()
    cursor.close()
    conn.close()



@app.patch('/facts/update', status_code=status.HTTP_204_NO_CONTENT, tags=['Controller'])
def update_status(fact_id: str, conn=Depends(connect_to_db)):
    update_stmt = '''
        UPDATE facts 
        SET status = CASE 
            WHEN status = 'nicht gesehen' THEN 'gesehen' 
            WHEN status = 'gesehen' THEN 'nicht gesehen' 
            ELSE status
        END
        WHERE fact_id = %s;
    '''
    update_tuple = (fact_id,)

    cursor = conn.cursor()
    cursor.execute(update_stmt, update_tuple)
    conn.commit()
    cursor.close()
    conn.close()



@app.delete('/facts/delete/{fact_id}/', status_code=status.HTTP_204_NO_CONTENT, tags=['Controller'])
def delete_fact(fact_id: int, conn=Depends(connect_to_db)):
    delete_stmt = 'DELETE FROM facts WHERE fact_id = %s;'
    fact_tuple = (fact_id, )
    cursor = conn.cursor()
    cursor.execute(delete_stmt, fact_tuple)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)


