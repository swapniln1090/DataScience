# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 14:22:43 2024

@author: Swapnil N
This is the Basic Of Fast API

"""

from fastapi import FastAPI

# lets intstantiate FastApi

app = FastAPI()


# set up a rout which would be used in link to access
@app.get("/")  # this is decorator
async def root():
    return "Hello World!!! Nice to see you learning FastAPI :) "


"""
Note : Now to run this, we can go to anaconda env and then navigate to particular path where this file is and the run below command 
"uvicorn <python file name>:<variable instatntiated for FastApi>  where in this case it is "uvicorn fast_api_basic:app" 
--> After executing above command, you get a link which could be "http://127.0.0.1:8000".
--> Copy this link and add rout what we have added i.e. "/" to link and run it in browser i.e. "http://127.0.0.1:8000/".
--> You should receive message that is given in in return as "Hello World"
--> By default port is 8000 but we can set the port as "uvicorn fast_api_basic:app --port=<port you want like 3000 or 8001 etc>"

Now if I make any changes in this file, say I changed the message, I won't be able to just refresh and see the changes in Browser. I always have to hit Ctrl + C and then terminate in my env and again run the command "uvicorn fast_api_basic:app"
To avoid this we can use "uvicorn fast_api_basic:app --reload"
"""


# Lets try with post request


@app.post("/")
async def post_req():
    return "Hello World from Post request"


"""
We cannot submit a post request from browser as we can do in "get" request. 
Now to check for this, Fast API gives us very beutifull UI where we need to do "/docs" infront of our link here "http://127.0.0.1:8000"
Hence we do "http://127.0.0.1:8000/docs" --> This opens Swagger documentation and gives us flexibility and we don't need to install Postman or other things
"""

# On a similar level, we can use other request as well such as put


@app.put("/")
async def put():
    return "Hello World from Put request"


# Just For our knowledge -
"""
POST Request - The POST method is used to create a new resource on the server. It is used when you want to submit data to the server to create a new resource, such as adding a new user, creating a new post, or sending data to a form submission.
GET Request - The GET method is used to retrieve or fetch data from the server. This method is used when you want to read or view information from a server without making any changes to the existing data or state of the resource.
PUT Request - The PUT method is used to update an existing resource or create a resource if it does not already exist. It is commonly used to update an existing resource with new data. If the resource is not found, it might create a new resource depending on the implementation.

"""
