from fastapi import FastAPI
from backend.db.database import init_db
init_db()

app = FastAPI()
@app.get("/")
def fresh():

    return {"hello":"world"}
