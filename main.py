from ast import List
from typing import Union, List

from fastapi import FastAPI
from pydantic import BaseModel
from models.models import ListModel, ListUpdateModel
from clases.firmamex import FirmamexServices
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json

app = FastAPI()

webid = "LspRxpD0ihLFwx7Y"
apikey = "17cbc02700b843e741e00a851dec67e4"

class Item(BaseModel):
    ticket  : str

@app.get("/")
def read_root():
    return {"test":"laracast"} 


@app.post("/checkworkflow")
def chek_workflow( items: List[Item] ):

    services = FirmamexServices(webid, apikey)

    response = services.workflow(items[0].ticket)

    return {"test":response} 

@app.post("/items")
def read_item( items: List[Item] ):
    
    services = FirmamexServices(webid, apikey)
    response = services.getReport(items[0].ticket)
    json_object = json.loads(response)
    return { "list": json_object}

@app.post("/document")
def read_item( items: List[Item] ):
    
    services = FirmamexServices(webid, apikey)
    response = services.report(items[0].ticket)
    json_object = json.loads(response)
    return { "list": json_object}


@app.delete("/document/delete")
def read_item( items: List[Item] ):
    action = {
        'ticket': items[0].ticket,
        'action': 'delete'
    }
    services = FirmamexServices(webid, apikey)
    response = services.deleteDocument(action)
    json_object = json.loads(response)
    return { "list": json_object}

@app.get('/send/whatsapp')
def send_mail():
    # Defining the Phone Number and Message
    phone_number = "5217225601533"
    message = "message"

    