"""
@author: Swapnil N
Reference - JVP Design & FAST API doc
Will use Pydantic function in this
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# The way we specify the below things, we won't use path parameters or query parameters. We pass

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float


@app.post("/items")
async def get_item(item: Item):
    item_dict = item.dict() # This is a default method that comes with Pydantic


# Run code as - "uvicorn request_body:app --reload"
