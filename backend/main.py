from fastapi import FastAPI
from backend.db.database import main
app = FastAPI()
@app.get("/")
def fresh():
    main()
    return {"hello":"world"}
