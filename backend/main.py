from fastapi import FastAPI
from backend.db.database import init_db
from backend.routes import user
init_db()

app = FastAPI()
app.include_router(user.router)
@app.get("/")
def fresh():

    return {"hello":"world"}
