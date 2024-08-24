from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Union

app = FastAPI()

# uvicorn main:app --host 0.0.0.0 --port 8080 --reload


class Category(Enum):
    TOOLS = 'tools'
    CONSUMABLES = 'consumables'

class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category


items = {
    0: Item(name="Hammer", price=9.99, count=20, id=0, category=Category.TOOLS),
    1: Item(name="Small Hammer", price=5.99, count=10, id=1, category=Category.TOOLS),
    2: Item(name="Pliers", price=5.99, count=20, id=2, category=Category.TOOLS),
    3: Item(name="Nails", price=1.99, count=100, id=3, category=Category.CONSUMABLES),
}

# FastAPI handles JSON serialization and deserialization for us.
# We can simply use built-in python and Pydantic types, in this case dict[int, Item].

@app.get("/")
def index() -> list[str]:
    return ["Welcome to our ioStore API.", "Navigate to /docs to start querying using Swagger."]


@app.get("/items")
def query_items() -> dict[str, dict[int, Item]]:
    return {"items": items}


@app.get("/items/{item_id}")
def query_items_by_id(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item with {item_id=} was not found."
        )

    return items[item_id]


Selection = dict[str, str | int | float | Category | None]


# this endpoint url conflicts with GET /items if using /items?attr=
@app.get("/items-query")
def query_items_by_parameters(
        name: str | None = None,
        price: float | None = None,
        count: int | None = None,
        category: Category | None = None
) -> dict[str, Selection | list[Item]]:

    def check_item(item: Item) -> bool:
        return all(
            (
                name is None or item.name == name,
                price is None or item.price == price,
                count is None or item.count == count,
                category is None or item.category is category,
            )
        )

    selection = [item for item in items.values() if check_item(item)]

    return {
        "query": {"name": name, "price": price, "count": count, "category": category},
        "selection": selection
    }


@app.post("/items")
def add_item(item: Item) -> dict[str, Item]:

    if item.id in items:
        HTTPException(
            status_code=400, detail=f"Item with {item.id=} already exists."
        )

    items[item.id] = item
    return {"created_item": item}


# Fast API - Path and Query validations directly
@app.put("/items/{item_id}",
         responses={
             404: {"description": "Item not found"},
             400: {"description": "No arguments specified"}
         })
def update_item(
    item_id: int,
    name: str | None = None,
    price: float | None = None,
    count: int | None = None,
) -> dict[str, Item]:

    if item_id not in items:
        HTTPException(
            status_code=404, detail=f"Item with {item_id=} was not found."
        )

    if all(info is None for info in (name, price, count)):
        raise HTTPException(
            status_code=400, detail="No parameters provided for update."
        )

    item = items[item_id]

    if name is not None:
        item.name = name

    if price is not None:
        item.price = price

    if count is not None:
        item.count = count

    return {"updated_item": item}


@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> dict[str, Item]:
    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item with {item_id=} is already deleted."
        )

    item = items.pop(item_id)

    return {"deleted_item": item}


@app.patch("/items/{item_id}",
           responses={404: {"description": "Item not found"}})
def patch_item(item_id: int, count: int | None = None) -> dict[str, Item]:
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    if count is not None:
        items[item_id].count = count

    return {"patched_item": items[item_id]}
