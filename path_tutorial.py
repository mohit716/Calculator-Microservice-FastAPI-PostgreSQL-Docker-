# from fastapi import FastAPI
# app = FastAPI()

# below The value of the path parameter item_id will be passed to your function as the argument item_id.
# @app.get("/items/{item_id}")
# def read_item(item_id: str):
#     return {"item_id": item_id}



# test using below
# url:  http://127.0.0.1:8000/items/foo 




# Path parameters with types
# You can declare the type of a path parameter in the function, using standard Python type annotations:

from fastapi import FastAPI
app = FastAPI()
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


# Data conversion   
# Data conversion¶
# If you run this example and open your browser at http://127.0.0.1:8000/items/3, you will see a response of:


# {"item_id":3}