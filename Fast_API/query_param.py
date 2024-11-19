"""
Created on Sun Nov  16  2024

@author: Swapnil N
This is detailed Query Parameters for Fast API
Reference - Fast API docs and JVP Design(YTB)
"""

"""
Difference between Query Parameters and Path Parameters -

Path Parameters - Used to capture values embedded directly in the URL path. Included as part of the endpoint URL (e.g., /items/{item_id}).
Defined as part of the route path in the function's decorator.

Query Parameters - Used to pass optional or additional data in the query string of the URL. Appended to the URL after a ? and separated by & for multiple parameters (e.g., /items?name=book&price=20).
Defined as function parameters without being part of the route path.
So if we see path_param, we specify the parameter say "item_id", in @app.get("/item/{item_id}") and then also mention same parameter in function paramaters. 
However, in Query parameter, we do not specify in @app.get("/item"), but specify in function parameters.
"""
from fastapi import FastAPI
from typing import Optional

hold = FastAPI()

item_db = [{"item_name": "Bag"}, {"item_name": "Hat"}, {"item_name": "Shoe"}]


@hold.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    return item_db[skip : skip + limit]


# The below type of code can be used for LLM response, where we can take query from users and then this query could be passed to the LLM Pipeline.
@hold.get("/items/{item_id}")
async def get_item(
    item_id: str, q: Optional[str] = None
):  # Though here q has been kept optional, but if we see in Chat gpt, we need to pass some query, then only we can hit enter and get a response. Here we wanted to just check some options like "Optional".
    if q:  # Check if query q is not empty
        return {"item_id": item_id, "query": q}
    return {"item_id": item_id}


# We can also do something like below, if we want to say captuare UserId( could be login id or login email id), with query they pass. Consider your Chat gpt as an example


@hold.get("/users/{user_id}/items/{item_id}")
async def get_user_query(user_id: int, item_id: int, q: Optional[str] = None):
    if q:
        return {"User Id": user_id, "Item Id": item_id, "Query": q}
    return {"User Id": user_id, "Item Id": item_id}


# Say I have a query as "What is Fast API" and user id = 101, item_id = 222. Then how do we pass it?
# http://127.0.0.1:8000/users/111/items/222?q=What%20is%20Fast%20API
# URL Encoding -
# A space ( ) is encoded as %20. Hence, The string "What is Fast API" would be encoded as What%20is%20Fast%20API.


# To Run code - "uvicorn query_param:hold --reload"
