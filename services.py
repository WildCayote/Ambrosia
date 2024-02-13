from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


import models  
from security import JWT
from databaseService import  PaymentTypes 

router = APIRouter(
    tags = ["services"]
)

templates = Jinja2Templates(directory="./menu/menu")

router.mount("/static" , StaticFiles(directory="./menu/menu") , name="static")



#getting the services we give with their prices and descriptions
@router.get("/services")
def getServices():
    services = PaymentTypes.getPaymentTypes()
    response = []
    if services:
        for service in services:
            response.append(
                {
                    "id" : service[0],
                    "description" : service[1],
                    "price" : service[2]
                }
            )
        return {
            "success" : True,
            "services" : response
        }
    
    else:
        return{
            "success" : False,
            "message" : services
        }


#change the price of a service
@router.post("/services/update/price")
def updatePrice(payload : models.UpdateServicePrice):
    token = JWT.verify(token=payload.token)
    if token['valid']:
        updatedService = PaymentTypes.changePrice(id=payload.id , price=payload.price)
        if updatedService == True:
            return{
                "success" : True,
                "message" : "Price changed successfuly"
            }
        else:
            return{
                "success" : False,
                "message" : updatedService
            }

    else:
        return{
            "success" : False,
            "message" : token['error']
        }


#change the description of a service
@router.post("/services/update/description")
def updateDescription(payload : models.UpdateServiceDescription):
    token = JWT.verify(token=payload.token)
    if token['valid']:
        updatedService = PaymentTypes.changeDescription(id=payload.id , description=payload.description)
        if updatedService == True:
            return{
                "success" : True,
                "message" : "Description changed successfuly"
            }
        else:
            return{
                "success" : False,
                "message" : updatedService
            }

    else:
        return{
            "success" : False,
            "message" : token['error']
        }
