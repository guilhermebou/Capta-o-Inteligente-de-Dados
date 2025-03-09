from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
app = FastAPI()


@app.get("/")
def read_data():
   return {"hello": "asdas"}
