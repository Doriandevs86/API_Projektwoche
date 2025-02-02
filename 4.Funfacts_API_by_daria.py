import uvicorn
import psycopg2
import random
import pyautogui

from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel, Field



''' Connection '''

pw = pyautogui.password('Bitte gib dein Passwort ein:', title= 'Password-Abfrage')

def connect_to_db():
    connection = psycopg2.connect(
        host='localhost',
        port=5432,
        user='postgres',
        password=pw,
        dbname='funfact_db'
    )
    return connection


''' API - Endpunkte '''

#Header für die API und eine kurze Beschreibung
app = FastAPI(
    title='Fun Facts App',
    summary='Eine API zum Auffinden interessanter Fakten'
)


#Basemodel
class Fact(BaseModel):
    facts: str = Field(default='Enter fact')
    status: str = Field(default='nicht gesehen')


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
    select_query = 'SELECT * FROM facts WHERE status = %s;'
    cursor = conn.cursor()
    cursor.execute(select_query, (status,))
    facts = cursor.fetchall()

    if not facts:
        raise HTTPException(status_code=404, detail="Keine Fakten mit diesem Status gefunden.")

    facts_dicts = []
    for fact in facts:
        fact_dict = {'fact_id': fact[0], 'facts': fact[1], 'status': fact[2]}
        facts_dicts.append(fact_dict)

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


# Neuen fakt hinzufügen
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


@app.patch('/facts/update', status_code=status.HTTP_200_OK, tags=['Controller'])
def update_status(fact_id: int, conn=Depends(connect_to_db)):
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

    # Führen Sie die Update-Abfrage aus
    try:
        cursor.execute(update_stmt, update_tuple)
        conn.commit()
        print(f"Updated fact with id {fact_id}.")
    except Exception as e:
        conn.rollback()
        print(f"Error updating fact: {e}")
        raise HTTPException(status_code=500, detail="Error updating the fact.")

    # Abfrage des aktualisierten Fakts
    select_query = 'SELECT * FROM facts WHERE fact_id = %s;'
    cursor.execute(select_query, (fact_id,))
    updated_fact = cursor.fetchone()

    cursor.close()

    # Überprüfen, ob das Fakt gefunden wurde
    if updated_fact is None:
        print(f"No fact found with id {fact_id}.")
        raise HTTPException(status_code=404, detail="Fact not found.")

    # Debugging-Ausgabe der Werte
    print(f"Fact fetched: {updated_fact}")

    return {"fact_id": updated_fact[0], "facts": updated_fact[1], "status": updated_fact[2]}


# Zufälligen Fakt zurückgeben
@app.get('/facts/random', status_code=status.HTTP_200_OK, tags=['Get Data'])

def get_random_fact(conn=Depends(connect_to_db)):
    select_query = 'SELECT * FROM facts;'
    cursor = conn.cursor()
    cursor.execute(select_query)
    facts = cursor.fetchall()

    if not facts:
        raise HTTPException(status_code=404, detail="Keine Fun Facts gefunden.")

    random_fact = random.choice(facts)
    fact_dict = {'fact_id': random_fact[0], 'facts': random_fact[1], 'status': random_fact[2]}

    return fact_dict


# Einen Fakt löschen
@app.delete('/facts/delete/{fact_id}/', status_code=status.HTTP_204_NO_CONTENT, tags=['Controller'])

def delete_fact(fact_id: int, conn=Depends(connect_to_db)):
    delete_stmt = 'DELETE FROM facts WHERE fact_id = %s;'
    fact_tuple = (fact_id, )
    cursor = conn.cursor()
    cursor.execute(delete_stmt, fact_tuple)
    conn.commit()
    cursor.close()


# Autostart
if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)


