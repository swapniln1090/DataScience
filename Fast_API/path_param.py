# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 14:43:59 2024

@author: Swapnil N
Description : This is about Path Parameters
"""

from fastapi import FastAPI

#lets intstantiate FastApi

app = FastAPI()

@app.get("/item")
async def list_items():
    return "List Items from Path Param"

"""
In this as well we will run "uvicorn path_param:app"" in our env. it will give us ink like "http://127.0.0.1:8000".
As earlier in "fast_api_basic", if we just add / to our link (i.e. http://127.0.0.1:8000/) then it will give us error as "{"detail":"Not Found"}" 
This is because, our method has "/item" and not just "/". hence we need to use "http://127.0.0.1:8000/item"
"""

@app.get("/item/{item_id}")
async def id_items(item_id : int):
    return f"Id of Item : {item_id}"

"""
# to invoke this id_items we need to run "http://127.0.0.1:8000/item/1001". Here we can pass any item id instead of 1001.
# We can use pydantic function to restrict type passed as parameter. in this case we can add parameter to be int. This will only allow integer values to be passed as parameter
# If I try to enter something like "http://127.0.0.1:8000/item/hello" then I get error as "{"detail":[{"type":"int_parsing","loc":["path","item_id"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"hello"}]}"
# Infact when we go to swagger doc i.e. "http://127.0.0.1:8000/docs", we can try giving a string say "swap" as input and it will give error
"""

# Remember : The oder here maters. Like if I have next rout as "/item/me", and if I pass something like http://127.0.0.1:8000/item/me then it will consider me as string rather than the below function.

@app.get("/item/me")
async def get_current_user():
    return "I am the current user"

# So remember this has a sequetion execution. Hence if you want to allow a specific endpoint first before dynamic endpoint.
# hence we should put the endpoints accordingly
"""
# Make it this way if you wanna have proper and smooth execution. I am keeping above so we know this gives error or unexpected output

We should do as -

@app.get("/item/me")
async def get_current_user():
    return "I am the current user"

@app.get("/item/{item_id}")
async def id_items(item_id : int):
    return f"Id of Item : {item_id}"

"""

# Just we can add one more thing to restric our input or to create logic accordingly
from enum import Enum

class FoodSelect(str, Enum):
    fruits = 'fruits'
    vegitables = 'vegitables'
    cold_drinks = 'cold drinks'
print(FoodSelect.fruits)
@app.get("/food/{food_name}")
async def get_food(food_name: FoodSelect):
    
    if food_name == FoodSelect.fruits:
        return {"message": f"You are Fruit Lover and You have selected {food_name}"}
    if food_name == FoodSelect.vegitables:
        return {"message": f"You are Vegitable Lover and You have selected {food_name}"}
    if food_name in FoodSelect.cold_drinks:
        return {"message": f"You are Cold Drink Lover and You have selected {food_name}. This is not Healthy"}

# So here we have restricted the input to the values given in Enum. If I give any other values than "fruits', 'vegitables' or 'cold drinks'" like "http://127.0.0.1:8000/food/fanta" it gives error as {"detail":[{"type":"enum","loc":["path","food_name"],"msg":"Input should be 'fruits', 'vegitables' or 'cold drinks'","input":"fanta","ctx":{"expected":"'fruits', 'vegitables' or 'cold drinks'"}}]}



















