from ast import List
from typing import Union, List

from fastapi import FastAPI
from pydantic import BaseModel
from models.models import ListModel, ListUpdateModel
from clases.firmamex import FirmamexServices
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json
import redis

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
    loop_firmas = []
    
    for i, list_item in enumerate(json_object['firmas']):
        loop_firmas.append({
            "signDate" : list_item['signDate'],
            "email"    : list_item['certificados'][0]['email']
        })
    
    response = {
        "firmas" : loop_firmas,
        "document" : json_object['document'],
        "documentStatus" : json_object['documentStatus'],
        "ticket" :json_object['ticket'],
        "originalName" : json_object['originalName'],
        "pendingSigners" : json_object['pendingSigners'],
    }
    
    r = redis.Redis(host='redis-cache', port=6379, db=0)
    r.set('firma',json.dumps(response))
    
    return response


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

    