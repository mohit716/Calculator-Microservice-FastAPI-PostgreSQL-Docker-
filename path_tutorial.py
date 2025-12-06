from fastapi import FastAPI
app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: str):
    return {"item_id": item_id}



# test using below
# url:  http://127.0.0.1:8000/items/foo 