from fastapi import FastAPI
app = FastAPI()
@app.post("post/add")-> float:
def add(a:float, b:float)->float:
    return a + b
@app.post("/subtract", parameters={"a": float, "b": float})
def subtract(a:float, b:float)->float:
    return a - b
@app.post("/multiply", parameters={"a": float, "b": float})
def multiply(a:float, b:float)->float:
    return a * b
@app.post("/divide", parameters={"a": float, "b": float})
def divide(a:float, b:float)->float:
    return a / b


