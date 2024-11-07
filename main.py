from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Boo"}]


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/products/")
async def create_product(product: Product):
    return product


@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product, q: str | None = None):
    result = {"product_id": product_id, **product.dict()}
    if q:
        result["q"] = q
    return result


@app.get("/items")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}")
async def read_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item["q"] = q
    if not short:
        item["description"] = "This has long description"
    return item


@app.get("/models/{model_name")
async def get_models(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/file_path:path")
async def read_file(file_path: str):
    return {"file_path": file_path}
